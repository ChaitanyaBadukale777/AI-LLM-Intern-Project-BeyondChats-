# persona_generator.py  – OpenRouter version with free‑model fallback
import os, time, requests
from dotenv import load_dotenv
load_dotenv()

# **Put at least one model you know you can call here.**
PRIMARY_MODEL   = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
FALLBACK_MODEL  = "mistralai/mistral-7b-instruct"    # free on OpenRouter
API_KEY         = os.getenv("OPENROUTER_API_KEY")

ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    # OpenRouter asks for a referrer / title for analytics
    "HTTP-Referer": "https://github.com/yourusername/reddit-persona",
    "X-Title":      "Reddit Persona Extractor"
}

# persona_generator.py  – only the helper function needs to change
def _call_openrouter(model: str, prompt: str):
    body = {"model": model,
            "messages": [{"role": "user", "content": prompt}]}

    r = requests.post(ENDPOINT, headers=HEADERS, json=body, timeout=90)

    if r.status_code == 200:
        reply_text = r.json()["choices"][0]["message"]["content"]
        return reply_text, None                    # <‑‑ always 2 values
    else:
        return None, f"{r.status_code} – {r.text}" # <‑‑ always 2 values


def generate_persona(posts, comments):
    if not API_KEY:
        return "[ERROR] Set OPENROUTER_API_KEY in .env"

    # Build the big prompt (‑‑ you already have truncate / limits elsewhere)
    blocks = []
    for i,p in enumerate(posts,1):
        blocks.append(f"Post #{i}\nTitle: {p['title']}\nBody: {p['body']}\nURL: https://reddit.com{p['url']}")
    for i,c in enumerate(comments,1):
        blocks.append(f"Comment #{i}\n{c['body']}\nURL: https://reddit.com{c['url']}")
    # prompt = (
    #     "Create a detailed **User Persona** from the Reddit content below. "
    #     "Include fictional Name, Age range, Occupation, Interests, Political Leaning (if visible), "
    #     "Tech‑savviness, Communication Style, plus any extra insights. "
    #     "Cite the Post/Comment number that supports each attribute.\n\n" +
    #     "\n\n".join(blocks)
    # )
    
    prompt = (
    "Using the following Reddit posts and comments, create a comprehensive **User Persona** in the format below:\n\n"
    "1. **Name** (fictional)\n"
    "2. **Age** (estimated or range)\n"
    "3. **Occupation**\n"
    "4. **Status** (e.g., relationship/marital status)\n"
    "5. **Location** (if detectable)\n"
    "6. **User Archetype** (e.g., The Creator, The Explorer, etc.)\n"
    "7. **Tier** (e.g., Early Adopter, Tech Enthusiast, etc.)\n\n"
    "**Personality Traits:** (e.g., Introvert–Extrovert, Practical–Spontaneous)\n"
    "**Motivations:** List key motivations like convenience, wellness, speed, etc. with relative emphasis.\n"
    "**Behavior & Habits:** Bullet points describing routine behaviors, habits, and patterns based on the Reddit data.\n"
    "**Frustrations:** What bothers this user? Extract pain points from their content.\n"
    "**Goals & Needs:** List their short-term or long-term needs/goals.\n\n"
    "**IMPORTANT:**\n"
    "- Support each attribute with Post or Comment numbers (e.g., 'Source: Comment #3').\n"
    "- Use only Reddit content below to infer these insights.\n\n"
    + "\n\n".join(blocks)
    )


    # 1️⃣ Try the primary model
    reply, err = _call_openrouter(PRIMARY_MODEL, prompt)
    if reply:
        return reply
    print(f"[WARN] Primary model failed: {err}")

    # 2️⃣ Retry once after short wait
    time.sleep(5)
    reply, err = _call_openrouter(PRIMARY_MODEL, prompt)
    if reply:
        return reply
    print(f"[WARN] Primary retry failed: {err}")

    # 3️⃣ Fallback to a free model
    print(f"[INFO] Switching to free model {FALLBACK_MODEL} …")
    reply, err = _call_openrouter(FALLBACK_MODEL, prompt)
    if reply:
        return reply
    return f"[ERROR] OpenRouter failed on all attempts: {err}"
