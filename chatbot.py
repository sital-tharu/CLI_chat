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

