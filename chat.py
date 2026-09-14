import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# This list holds the full conversation so far
messages = []

print("Chatbot ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # Add the user's message to the conversation history
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="openrouter/free",
        max_tokens=300,
        messages=messages,
    )

    reply = response.choices[0].message.content

    # Add the assistant's reply to history too, so it remembers what IT said
    messages.append({"role": "assistant", "content": reply})

    print(f"AI: {reply}\n")