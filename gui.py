import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a Python software developer expert. "
        "Give accurate, concise, and practical answers. "
        "If asked about anything unrelated to Python or programming, "
        "politely decline and redirect the user to Python topics."
    ),
}


def respond(message, history):
    messages = [SYSTEM_PROMPT] + history + [{"role": "user", "content": message}]

    stream = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        temperature=0.2,
        stream=True,
    )

    partial = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            partial += content
            yield partial
