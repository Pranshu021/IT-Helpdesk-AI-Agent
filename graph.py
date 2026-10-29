import re
from typing import Literal

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel

from state import AgentState
from tools import (
    create_ticket,
    estimate_ticket_priority,
    get_ticket_status,
    search_knowledge_base,
)


load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)


class NextAction(BaseModel):
    """The next action selected by the helpdesk controller."""

    action: Literal[
        "lookup",
        "ticket_status",
        "priority",
        "create_ticket",
        "finish",
        "out_of_scope"
    ]
    reason: str


planner = llm.with_structured_output(NextAction)


def decide_next_action(state: AgentState):
    """Choose the next useful action, or finish when the goal is met."""

    user_request = state["messages"][0].content
    print(f"Observations made so far - {state.get("observations")}")
    print("Deciding Next action ....")

    prompt = f"""
    You are controlling a small IT helpdesk workflow.

    User request:
    {user_request}

    Completed actions:
    {state.get("completed_steps", [])}

    Observations gathered so far:
    {state.get("observations", [])}

    Choose exactly one next action:
    - lookup: find troubleshooting information
    - ticket_status: check an existing ticket
    - priority: Use after lookup. Estimate the issue priority
    - create_ticket: create a demo support ticket only if user explicitly asks for it or when resolution wasn't found in knowledge base during lookup
    - finish: enough information has been gathered
    - out_of_scope: if the question is generic and outside IT troubleshooting scope

    Rules:
    - Do not repeat a completed action unless it is necessary.
    - Use lookup for troubleshooting questions. If the lookup is already present in observations and Resolution is not found in Knowledge base. Create a ticket and Finish
    - Use ticket_status only when the user mentions an existing ticket. If ticket is not found - Finish
    - Use priority after lookup to set the priority of IT issue.
    - Only choose create_ticket when the user explicitly asks to create,
    open, raise, report a new ticket or if a resolution was not found in knowledge base
    - Choose finish when the request has been handled.
    - This is a demo. Do not claim that a real support system was changed.
"""

    decision = planner.invoke(prompt)
    print(f"Next action is - {decision.action}")
    return {"next_action": decision.action}


def execute_next_action(state: AgentState):
    """Execute the controller's selected helpdesk action."""

    user_request = state["messages"][0].content
    action = state["next_action"]
    print(f"Executing action - {action}")

    if action == "lookup":
        result = search_knowledge_base.invoke({"query": user_request})
        print(f"Result of lookup - {result}")
    elif action == "priority":
        result = estimate_ticket_priority.invoke({"issue": user_request})
        print(f"Priority of issue has been set to {result}")
    elif action == "ticket_status":
        match = re.search(r"INC-\d+", user_request, re.IGNORECASE)
        ticket_id = match.group(0).upper() if match else "UNKNOWN"
        result = get_ticket_status.invoke({"ticket_id": ticket_id})
    elif action == "create_ticket":
        issue_priority = estimate_ticket_priority.invoke({"issue": user_request})
        result = create_ticket.invoke({"issue": user_request, "priority": issue_priority})
    elif action == "out_of_scope":
        result = "Query not related to IT Troubleshooting. Finish"
    else:
        result = "No action was executed."

    return {
        "observations": [
            *state.get("observations", []),
            f"{action}: {result}",
        ],
        "completed_steps": [
            *state.get("completed_steps", []),
            action,
        ],
        "iterations": state.get("iterations", 0) + 1,
    }


def generate_response(state: AgentState):
    """Turn the loop's observations into the final user-facing answer."""

    user_request = state["messages"][0].content
    observations = "\n".join(state.get("observations", []))

    prompt = f"""
You are a friendly IT helpdesk assistant.

User request:
{user_request}

Information gathered during the workflow:
{observations}

Give a concise final answer using only the information above.
If the user_request is not relevant to IT Troubleshooting reply exactly - 'Unable to process request. Queries related to IT troubleshooting are only allowed.'
Do not claim that a real ticket was created or that a real system was changed.
If a requested Ticket ID was not found, DO NOT create a new ticket automatically.
Mention demo behavior when ticket creation or priority estimation was used.
"""

    response = llm.invoke(prompt)
    return {"response": response.content}


def route_after_decision(state: AgentState):
    """Route to another action or finish the agentic loop."""

    if state["next_action"] == "finish":
        return "finish"

    return "execute"


graph_builder = StateGraph(AgentState)
graph_builder.add_node("decide", decide_next_action)
graph_builder.add_node("execute", execute_next_action)
graph_builder.add_node("respond", generate_response)

graph_builder.add_edge(START, "decide")
graph_builder.add_conditional_edges(
    "decide",
    route_after_decision,
    {
        "execute": "execute",
        "finish": "respond",
    },
)
graph_builder.add_edge("execute", "decide")
graph_builder.add_edge("respond", END)
 
graph = graph_builder.compile()
