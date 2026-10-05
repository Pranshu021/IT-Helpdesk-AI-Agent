from graph import graph


def main():
    print("AI IT Helpdesk Agent")
    print("--------------------")

    user_input = input("\nHow can I help you? ")

    result = graph.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        }
    )

    final_message = result["messages"][-1]

    print("\nAgent:")
    print(final_message.content)


if __name__ == "__main__":
    main()
