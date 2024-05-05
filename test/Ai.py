from g4f.client import Client
import json

# Initialize the g4f client
client = Client()

# Function to handle the conversation with memory
def handle_conversation():
    # Load or initialize the conversation history
    try:
        with open('conversation_history.json', 'r') as file:
            conversation_history = json.load(file)
    except FileNotFoundError:
        conversation_history = []

    # Start the conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("AI: Goodbye! It was nice chatting with you.")
            break

        # Add user input to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Send the conversation history to the AI and get a response
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )

        # Get the AI's response
        ai_response = chat_completion.choices[0].message.content or ""
        print(f"AI: {ai_response}")

        # Add AI response to the conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})

        # Save the updated conversation history
        with open('conversation_history.json', 'w') as file:
            json.dump(conversation_history, file)

# Run the conversation handler
handle_conversation()
