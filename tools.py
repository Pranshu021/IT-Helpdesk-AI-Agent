from langchain_core.tools import tool


@tool
def search_knowledge_base(query: str) -> list[str] | str:
    """Search the IT knowledge base for troubleshooting information."""

    knowledge_base = {
        "vpn": {
            "description": "Issue with VPN. VPN is not working or not connecting",
            "resolutions": [
                "If the VPN is not connecting, restart the VPN client",
                "Check your internet connection, and try reconnecting.",
                "Check if you are connecting to the correct URL in VPN Client",
            ],
        },
        "wifi": {
            "description": "Wifi is not working, and unable to connect to internet",
            "resolutions": [
                "If Wi-Fi is not working, restart the network adapter and reconnect to the network."
            ],
        },
        "docker": {
            "description": "Docker is not working. Docker is not starting. Unable to run Containers in Docker",
            "resolutions": [
                "If Docker is not starting, restart Docker Desktop",
                "Check if Virtualization is enabled",
                "Check if ample memory and CPU resources are available to run docker",
            ],
        },
    }

    query = query.strip().lower()

    for keyword, information in knowledge_base.items():
        if keyword in query:
            return information["resolutions"]

    return "Resolution not found in Knowledge Base. Create a new Ticket"


@tool
def get_ticket_status(ticket_id: str) -> str:
    """Get the current status of an IT support ticket."""

    tickets = {
        "INC-1001": {
            "status": "In Progress",
            "issue": "VPN authentication failure",
            "priority": "MEDIUM",
        },
        "INC-1002": {
            "status": "Resolved",
            "issue": "Docker installation problem",
            "priority": "MEDIUM",
        },
        "INC-1003": {
            "status": "In Progress",
            "issue": "Microsoft Teams Outage",
            "priority": "HIGH",
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
def create_ticket(issue: str, priority: str) -> str:
    """Create a new IT support ticket."""

    return (
        f"Support ticket created successfully for issue: '{issue}' with priority {priority}"
        "Ticket ID: INC-1003"
    )


@tool
def estimate_ticket_priority(issue: str) -> str:
    """Estimate the priority of an IT issue for ticket triage."""

    issue = issue.lower()

    high_priority_words = (
        "outage",
        "production",
        "security",
        "data loss",
        "everyone",
        "entire team",
    )
    medium_priority_words = (
        "vpn",
        "cannot login",
        "authentication",
        "email",
        "docker",
        "windows",
        "password",
    )

    if any(word in issue for word in high_priority_words):
        return "HIGH"

    if any(word in issue for word in medium_priority_words):
        return "MEDIUM"

    return "LOW"


tools = [
    search_knowledge_base,
    get_ticket_status,
    create_ticket,
    estimate_ticket_priority,
]
