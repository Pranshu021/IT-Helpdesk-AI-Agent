from langchain_core.tools import tool


@tool
def search_knowledge_base(query: str) -> str:
    """Search the IT knowledge base for troubleshooting information."""

    knowledge_base = {
        "vpn": (
            "If the VPN is not connecting, restart the VPN client, "
            "check your internet connection, and try reconnecting."
        ),
        "wifi": (
            "If Wi-Fi is not working, restart the network adapter "
            "and reconnect to the network."
        ),
        "docker": (
            "If Docker is not starting, restart Docker Desktop "
            "and make sure virtualization is enabled."
        ),
    }

    query = query.strip().lower()

    for keyword, answer in knowledge_base.items():
        if keyword in query:
            return answer

    return "not_found"


@tool
def get_ticket_status(ticket_id: str) -> str:
    """Get the current status of an IT support ticket."""

    tickets = {
        "INC-1001": {
            "status": "In Progress",
            "issue": "VPN authentication failure",
        },
        "INC-1002": {
            "status": "Resolved",
            "issue": "Docker installation problem",
        },
    }

    ticket = tickets.get(ticket_id.upper())

    if not ticket:
        return f"Ticket {ticket_id} was not found."

    return (
        f"Ticket {ticket_id}: "
        f"Status = {ticket['status']}, "
        f"Issue = {ticket['issue']}"
    )


@tool
def create_ticket(issue: str) -> str:
    """Create a new IT support ticket."""

    return (
        f"Support ticket created successfully for issue: '{issue}'. "
        "Ticket ID: INC-1003"
    )


tools = [
    search_knowledge_base,
    get_ticket_status,
    create_ticket,
]
