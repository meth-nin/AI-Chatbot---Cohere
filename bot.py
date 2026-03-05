import cohere
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

    system_message = (
        "You are a helpful Toyota car assistant. "
        "Recommend Toyota cars to user's specification. "
        "Always respond in a friendly and informative manner. "
        "Don't answer questions that are not related to Toyota cars. "
        "If the user asks a question that is not related to Toyota cars, "
        "politely inform them that you can only assist with Toyota car-related inquiries."
    )

    #convo history
    messages = [
        {"role": "system", "content": system_message}
    ]

    print("Welcome to Toyota!! How can I assist you today?? Type 'exit' to quit.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("Goodbye!!")
            break

        #add user message
        messages.append({"role": "user", "content": message})

        response = co.chat_stream(
            model="command-a-03-2025",
            messages=messages,
            temperature=0.25,
            max_tokens=300,
            frequency_penalty=0.4
        )

        bot_reply = ""

        print("Assistant: ", end="")

        for event in response:
            if event.type == "content-delta":
                text = event.delta.message.content.text
                bot_reply += text
                print(text, end="")

        print("\n")

        #bot reply
        messages.append({"role": "assistant", "content": bot_reply})

        #memory limit
        if len(messages) > 20:
            messages = [messages[0]] + messages[-19:]

    #chat history
    print("\nChat History:\n")
    for msg in messages:
        print(msg, "\n")


if __name__ == "__main__":
    main()