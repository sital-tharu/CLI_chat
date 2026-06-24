# Gemini CLI Python Developer Chatbot 🐍🤖

Welcome to your first AI project! This repository contains a production-ready, interactive command-line interface (CLI) chatbot powered by Google's **Gemini 3.1 Flash** model. It utilizes the OpenAI-compatible endpoint provided by Google AI Studio, combining the simplicity of the OpenAI SDK with the speed and efficiency of the Gemini API.

The chatbot is specifically configured as an expert Python software developer, optimized to deliver accurate, concise, and highly practical coding answers.

---

## 🚀 Key Features

* **OpenAI SDK Integration**: Leverages the familiar `openai` library to connect directly to Google's generative language endpoints (`https://generativelanguage.googleapis.com/v1beta/openai/`).
* **Real-time Streaming (`stream=True`)**: Renders responses chunk-by-chunk as they arrive, providing an ultra-responsive user experience.
* **Persistent Conversation History**: Tracks user and assistant interactions sequentially so the model retains full context during a multi-turn chat session.
* **Resilient Error Handling**: Safely handles connection or API errors by rolling back the message history, ensuring the loop remains active for retry attempts.
* **Deterministic Configuration**: Employs a low temperature (`temperature=0.2`) to focus responses on concrete coding logic rather than creative variations.

---

## 🛠️ Prerequisites

Before running the application, ensure you have the following installed:
* **Python 3.8 or higher**
* A Google AI Studio API Key. Get yours from [Google AI Studio](https://aistudio.google.com/).

---

## ⚙️ Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone or Create the Project Directory
```bash
mkdir gemini-python-chatbot
cd gemini-python-chatbot
```

### 2. Install Dependencies
Install the required packages using `pip`:
```bash
pip install openai python-dotenv
```

### 3. Configure Environment Variables
Create a file named `.env` in the root directory of your project and paste your Gemini API key inside it:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

---

## 🎯 How It Works: Code Architecture

The script maps perfectly to structural conversational concepts in modern LLM applications:

1. **System Prompt Alignment**: Sets the AI persona at initialization (`"You are a Python software developer expert. Give accurate, concise, and practical answers."`).
2. **Context Appending**: Helper functions `add_user_message()` and `add_assistant_message()` structure interactions into standard API role payloads (`system`, `user`, `assistant`).
3. **Chunk Consumption Loop**: The streaming engine catches delta packets in a generator pattern:
   ```python
   for chunk in response:
       content = chunk.choices[0].delta.content
       if content is not None:
           print(content, end="", flush=True)
   ```

---

## 🖥️ Usage

Execute the main Python file to start chatting:

```bash
python main.py
```

### Interaction Example:
```text
=============================================
  Welcome to the Gemini Chatbot!
  Type 'quit' or 'exit' to stop.
=============================================

You: How do I read a file line by line in Python?

AI: Use a context manager `with open()` and iterate over the file object:

```python
with open('file.txt', 'r') as file:
    for line in file:
        print(line.strip())
```
This is memory-efficient because it reads one line at a time.

You: quit
Ending chat. Goodbye!
```

---


