import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

def call_api(prompt, options, context):
    messages = [
        {
            "role": "system",
            "content": "You are a Python software developer expert. Give accurate, concise, and practical answers. If asked about anything unrelated to Python or programming, politely decline and redirect the user to Python topics."
        },
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        temperature=0.2,
    )

    return {"output": response.choices[0].message.content}
