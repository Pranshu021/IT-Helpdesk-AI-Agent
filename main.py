from langgraph.errors import GraphRecursionError

from graph import graph


def main():
    print("AI IT Helpdesk Agent - Agentic Loop")
    print("--------------------")
    print("Type 'exit' or 'quit' to quit\n")

    while True:
        user_input = input("\nHow can I help you?\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        try:
            result = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ],
                    "observations": [],
                    "completed_steps": [],
                    "next_action": "",
                    "iterations": 0,
                    "response": "",
                },
                config={"recursion_limit": 10},
            )

            print(f"\nAgent: {result['response']}\n")
        except GraphRecursionError:
            print(
                "\nAgent: I could not complete the request within "
                "the allowed number of steps.\n"
            )


if __name__ == "__main__":
    main()
