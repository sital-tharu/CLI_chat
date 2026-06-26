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
