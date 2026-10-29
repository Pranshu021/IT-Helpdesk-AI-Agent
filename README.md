# LangGraph Helpdesk Agent - Video 4

A deliberately small AI IT Helpdesk Agent for learning LangGraph agentic loops.

## Concepts covered

- State
- Nodes and conditional edges
- START / END
- Local helpdesk tools
- An explicit agentic loop: decide -> execute -> observe -> decide
- Structured model output for choosing the next action
- Recursion limits for loop safety

## Setup

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Run the demo:

```bash
python main.py
```

## Video 4: Agentic Loop

The controller repeatedly chooses the next useful helpdesk action based on
the user's goal, completed steps, and observations gathered so far:

```text
START -> decide -> execute -> decide -> execute -> respond -> END
                       ^          |
                       |__________|
```

The loop can use the local knowledge base, check a demo ticket, estimate a
ticket priority, or create a demo ticket. The model chooses when to continue
and when enough information has been gathered to finish.

This is intentionally separate from the ReAct tool-call loop introduced in
the previous video. Here, the graph state explicitly tracks progress and the
controller selects the next workflow action.

## Try these prompts

```text
My VPN is not connecting. Look up troubleshooting advice and estimate the ticket priority.
```

```text
Check INC-1001 and tell me whether it needs escalation.
```

```text
Create a ticket because my Wi-Fi keeps disconnecting and estimate its priority.
```

All ticket data and troubleshooting information are local demo data. Ticket
creation does not change a real support system, and priority estimation is a
simple keyword-based demo policy rather than a production SLA calculation.
