from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import AgentState
from tools import tools
from tools import search_knowledge_base, get_ticket_status, create_ticket
import re

load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def classify_request(state: AgentState):
    """Classify the user's request into one workflow category."""
    user_request = state["messages"][-1].content

    prompt = f"""
    Classify this IT helpdesk request into exactly one category:
    - knowledge: IT related troubleshooting or IT how-to question
    - ticket_status: asks about an existing ticket's status
    - create_ticket: asks to report an issue or create a support ticket
    - general: anything else

    Return only the category name, with no punctuation.

    Request: {user_request}
    """
    result = llm.invoke(prompt).content.strip().lower()
    allowed = {"knowledge", "ticket_status", "create_ticket", "general"}

    category = result if result in allowed else "general"
    return {"category": category}

def route_request(state: AgentState):
    """ Choose the processing node based on the classification result. """
    return state["category"]

def process_knowledge_request(state: AgentState):
    request = state["messages"][-1].content
    result = search_knowledge_base.invoke({"query": request})
    print("Result here -- ", result)
    return {"tool_result": result}

def solution_or_ticket(state: AgentState):
    solution = state["tool_result"]
    if solution == "not_found":
        return "solution_not_found"
    
    return "solution_found"

def process_ticket_status(state: AgentState):
    """ To process the ticket or fetch the ticket based on user request """
    user_request = state["messages"][-1].content
    match = re.search(r"INC-\d+", user_request, re.IGNORECASE)
    ticket_id = match.group(0).upper() if match else "UNKNOWN"
    result = get_ticket_status.invoke({"ticket_id": ticket_id})
    return {"tool_result": result}


def process_create_ticket(state: AgentState):
    """ To create a ticket based on IT issue """
    user_request = state["messages"][-1].content
    result = create_ticket.invoke({"issue": user_request})
    return {"tool_result": result}

def process_general_request(state: AgentState):
    return {
        "tool_result": (
            "This assistant can troubleshoot common VPN, Wifi, and Docker issues. Check a demo ticket status or create a demo support ticket"
        )
    }

def generate_response(state: AgentState):
    """ Turn the selected workflow's result into a user-friendly answer """
    
    user_request = state["messages"][-1].content
    prompt = f"""
    You are a friendly IT helpdesk assistant.
    Answer the user's request using the workflow below.
    Do not claim that a real ticket was created, this is just a tutorial demo
    Be concise and do not invent any details
    
    User request: {user_request}
    Request category: {state['category']}
    Workflow result: {state['tool_result']}
    """
    
    response = llm_with_tools.invoke(prompt).content
    return {"response": response}
    
    
tool_node = ToolNode(tools)

graph_builder = StateGraph(AgentState)

graph_builder.add_node("classify_request", classify_request)
graph_builder.add_node("process_knowledge", process_knowledge_request)
graph_builder.add_node("check_ticket_status", process_ticket_status)
graph_builder.add_node("create_ticket", process_create_ticket)
graph_builder.add_node("handle_general", process_general_request)
graph_builder.add_node("generate_response", generate_response)


graph_builder.add_edge(START, "classify_request")

graph_builder.add_conditional_edges(
    "classify_request",
    route_request,
    {
        "knowledge": "process_knowledge",
        "ticket_status": "check_ticket_status",
        "create_ticket": "create_ticket",
        "general": "handle_general"
    }
)

graph_builder.add_conditional_edges(
    "process_knowledge",
    solution_or_ticket,
    {
        "solution_not_found": "create_ticket",
        "solution_found": "generate_response"
    }
)

graph_builder.add_edge("process_knowledge", "generate_response")
graph_builder.add_edge("check_ticket_status", "generate_response")
graph_builder.add_edge("create_ticket", "generate_response")
graph_builder.add_edge("handle_general", "generate_response")
graph_builder.add_edge("generate_response", END)

graph = graph_builder.compile()
