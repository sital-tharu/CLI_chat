import os
from openai import OpenAI
from dotenv import load_dotenv


# Loads the GOOGLE_API_KEY from your .env file
load_dotenv()

# Connect to Google's API using the OpenAI-compatible endpoint
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)



# --- Helper Functions ---

def add_user_message(messages, text):
    messages.append({"role": "user", "content": text})

def add_assistant_message(messages, text):
    messages.append({"role": "assistant", "content": text})

def chat(messages):
    response = client.chat.completions.create(
        model="gemini-2.5-flash-lite-preview-06-17",  # free model
        messages=messages,
        temperature=0.2,  # lower = more focused answers
        stream=True,      # prints words as they arrive, feels faster
    )

    print("\nAI: ", end="", flush=True)
    full_response = ""

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is not None:
            print(content, end="", flush=True)
            full_response += content

    print("\n")
    return full_response

# --- Main Chatbot Loop ---

print("=" * 45)
print("  Welcome to the Gemini Chatbot!")
print("  Type 'quit' or 'exit' to stop.")
print("=" * 45 + "\n")


# System prompt = instructions for how the AI should behave
messages = [
    {
        "role": "system",
        "content": "You are a Python software developer expert. Give accurate, concise, and practical answers."
    }
]

while True:
    user_text = input("You: ")

    if user_text.strip() == "":
        continue  # ignore empty Enter presses

    if user_text.lower() in ['quit', 'exit']:
        print("Ending chat. Goodbye!")
        break

    add_user_message(messages, user_text)

    try:
        generated_text = chat(messages)
        add_assistant_message(messages, generated_text)

    except Exception as e:
        print(f"\nError: {e}\n")
        # Remove the failed message so the user can try again
        if messages and messages[-1]['role'] == 'user':
            messages.pop()