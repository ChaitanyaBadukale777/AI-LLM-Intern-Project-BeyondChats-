# persona_generator.py

import google.generativeai as genai

# Set your Gemini API Key
genai.configure(api_key="AIzaSyCFW2lZRH8mpnRQNJXU-P4oRrb3t8Rilog")

def generate_persona(posts, comments):
    """Uses Gemini to generate persona from Reddit content."""

    content = ""
    sources = []

    for idx, post in enumerate(posts):
        text = (
            f"Post #{idx+1}:\n"
            f"Title: {post['title']}\n"
            f"Body: {post['body']}\n"
            f"URL: https://reddit.com{post['url']}\n"
        )
        content += text + "\n"
        sources.append(f"Post #{idx+1} - https://reddit.com{post['url']}")

    for idx, comment in enumerate(comments):
        text = (
            f"Comment #{idx+1}:\n"
            f"{comment['body']}\n"
            f"URL: https://reddit.com{comment['url']}\n"
        )
        content += text + "\n"
        sources.append(f"Comment #{idx+1} - https://reddit.com{comment['url']}")

    # Prompt for Gemini model
    prompt = (
        "Based on the following Reddit posts and comments, create a detailed User Persona "
        "including Name (fictional), Age range, Occupation, Interests, Political Leaning (if detectable), "
        "Tech-savviness, Communication Style, and any other insights. For each attribute, provide the source "
        "Post or Comment number that supports it.\n\n" + content
    )

    # Initialize Gemini model
    model = genai.GenerativeModel("gemini-pro")

    # Generate response
    response = model.generate_content(prompt)

    return response.text
