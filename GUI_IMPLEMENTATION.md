# GUI Implementation

This document explains how we added a Gradio web UI to the existing CLI chatbot.

---

## What We Built

The original app (`chatbot.py`) was a terminal chatbot — you typed questions and got answers in the terminal. We added `gui.py`, which runs the same chatbot in a browser at `http://localhost:7860` with a proper chat interface, message bubbles, and real-time streaming.

---

## Tech Stack

| Tool | Role |
|------|------|
| [Gradio 6.x](https://www.gradio.app/) | Web UI framework for the chat interface |
| OpenAI SDK | Talks to Google Gemini via OpenAI-compatible endpoint |
| python-dotenv | Loads `GOOGLE_API_KEY` from `.env` |

---

## How It Works

### 1. Client Setup

We reuse the exact same Gemini API client from `chatbot.py`:

```python
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
```

The OpenAI SDK points to Google's OpenAI-compatible endpoint, so we can use familiar OpenAI syntax while running on Gemini.

### 2. System Prompt

Defined once as a module-level constant:

```python
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a Python software developer expert. "
        "Give accurate, concise, and practical answers. "
        "If asked about anything unrelated to Python or programming, "
        "politely decline and redirect the user to Python topics."
    ),
}
```

### 3. The `respond()` Function

This is the core function. Gradio calls it every time the user sends a message:

```python
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
```

**How Gradio passes data to this function:**
- `message` — the new user message as a plain string
- `history` — all previous turns as a list of `{"role": "user"/"assistant", "content": "..."}` dicts (Gradio 6.x default format, which matches the OpenAI SDK format exactly — no conversion needed)

**How streaming works:**
- We call the Gemini API with `stream=True`
- Each chunk contains a small piece of the response
- We accumulate chunks into `partial` and `yield` it after each chunk
- Gradio re-renders the chat bubble on every yield, creating the live typing effect

### 4. Gradio Interface

```python
demo = gr.ChatInterface(
    fn=respond,
    title="Python Dev Chatbot",
    description="Ask me anything about Python and programming. Powered by Google Gemini.",
)
```

`gr.ChatInterface` is Gradio's highest-level chat component. It automatically provides:
- Chat message bubbles (user on the right, bot on the left)
- Input box and Send button
- Clear button
- Per-browser-tab session history (each tab gets its own independent conversation)

### 5. Launch

```python
if __name__ == "__main__":
    demo.launch()
```

Starts a local web server at `http://127.0.0.1:7860`.

---

## Why We Did Not Import `chatbot.py`

`chatbot.py` runs a `while True:` loop at module level, so importing it would immediately block. `gui.py` is self-contained and duplicates only the 5-line client setup — an intentional and correct choice.

---

## Bug Fixed During Implementation

When first running the app we hit:

```
TypeError: ChatInterface.__init__() got an unexpected keyword argument 'type'
```

The original code had `type="messages"` in `ChatInterface(...)`. This argument existed in Gradio 4.x but was **removed in Gradio 6.x**, where the messages dict format is now the default. Removing the argument fixed the issue.

---

## Installation

```bash
pip install gradio openai python-dotenv
```

---

## Running the GUI

```bash
python gui.py
```

Then open `http://localhost:7860` in your browser.

---

## Git History (GUI branch)

| Commit | Description |
|--------|-------------|
| `64385a5` | Add gui.py: imports, Gemini client setup, and system prompt |
| `c198e88` | Add respond() streaming function to gui.py |
| `dde42e8` | Add Gradio ChatInterface and launch entry point to gui.py |
| `ac2b807` | Fix ChatInterface: remove type parameter incompatible with Gradio 6.x |
