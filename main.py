from graph import graph


def main():
    print("AI IT Helpdesk Agent - Multi-step Workflow")
    print("--------------------")
    print("Type 'exit' or 'quit' to quit\n")

    while True:
        user_input = input("\nHow can I help you?\nYou: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = graph.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ],
                "category": "",
                "tool_result": "",
                "response": ""
            }
        )

        print(f"\nCategory: {result['category']}")
        print(f"Workflow result: {result['tool_result']}\n")
        print(f"Agent: {result['response']}\n")


if __name__ == "__main__":
    main()
