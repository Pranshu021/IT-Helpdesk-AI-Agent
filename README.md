# LangGraph Helpdesk Agent — Video 1

A deliberately small AI IT Helpdesk Agent for learning the basics of LangGraph.

## Concepts covered

- State
- Nodes
- Edges
- Conditional edges
- START / END
- Tool calling
- ToolNode
- Agent → Tools → Agent loop

## Project structure

```text
langgraph-helpdesk/
├── main.py
├── graph.py
├── tools.py
├── state.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the API key

Copy `.env.example` to `.env`:

```text
OPENAI_API_KEY=your_openai_api_key_here
```

Then replace the placeholder with your OpenAI API key.

### 4. Run

```bash
python main.py
```

## Try these prompts

```text
My VPN isn't connecting.
```

```text
What's the status of INC-1001?
```

```text
Create a ticket because my Wi-Fi keeps disconnecting.
```

```text
What can you help me with?
```

## Graph

```text
                         ┌───────────────┐
                         │               │
                         ▼               │
START → AGENT → Conditional Edge → TOOLS
          │                         │
          │                         │
          └────────────→ END        │
                                    │
                                    └──→ AGENT
```

The project intentionally uses hardcoded knowledge-base and ticket data. Later videos can progressively replace these pieces with databases, RAG, memory, human-in-the-loop, MCP, and other advanced LangGraph features.
