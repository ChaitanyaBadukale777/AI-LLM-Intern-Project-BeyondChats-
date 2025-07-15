# persona_generator.py — OpenRouter version using only fallback model

import os, requests
from dotenv import load_dotenv
load_dotenv()

MODEL     = "mistralai/mistral-7b-instruct"  # Free OpenRouter model
API_KEY   = os.getenv("OPENROUTER_API_KEY")

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/yourusername/reddit-persona",  # Optional
    "X-Title":      "Reddit Persona Extractor"
}

# 🧠 Function to call OpenRouter API
def _call_openrouter(model: str, prompt: str):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        r = requests.post(ENDPOINT, headers=HEADERS, json=body, timeout=90)
        if r.status_code == 200:
            reply_text = r.json()["choices"][0]["message"]["content"]
            return reply_text, None
        else:
            return None, f"{r.status_code} – {r.text}"
    except Exception as e:
        return None, str(e)


# ✅ Main function for generating the persona
def generate_persona(username, posts, comments):
    if not API_KEY:
        return "[ERROR] OPENROUTER_API_KEY is not set in your .env file"

    # Build content blocks from posts/comments
    blocks = []

    for idx, post in enumerate(posts, 1):
        blocks.append(
            f"Post #{idx}:\n"
            f"Title: {post['title']}\n"
            f"Body: {post['body']}\n"
            f"URL: https://reddit.com{post['url']}"
        )

    for idx, comment in enumerate(comments, 1):
        blocks.append(
            f"Comment #{idx}:\n"
            f"{comment['body']}\n"
            f"URL: https://reddit.com{comment['url']}"
        )

    content = "\n\n".join(blocks)

    # Build final prompt
    prompt = (
    f"You are an AI assistant. Based ONLY on the following real Reddit posts and comments by u/{username}, "
    "create a structured and professional User Persona.\n\n"
    "Include:\n"
    f"- Username: u/{username}\n"
    "- Age range (if inferable)\n"
    "- Occupation (if mentioned)\n"
    "- Interests\n"
    "- Political Leaning (if detectable)\n"
    "- Tech‑savviness\n"
    "- Communication Style\n"
    "- Relevant traits, frustrations, goals, and motivations\n\n"
    "Do not invent any information and avoid mentioning any reference numbers or links.\n\n"
        + content
    )

    print(f"[INFO] Generating persona using model: {MODEL}")
    reply, err = _call_openrouter(MODEL, prompt)

    if reply:
        return reply
    else:
        return f"[ERROR] OpenRouter API error: {err}"
    
