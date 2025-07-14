from dotenv import load_dotenv
load_dotenv()

from reddit_scraper import extract_username, scrape_user_data
from persona_generator import generate_persona
from utils import save_to_file

def main():
    profile_url = input("Enter Reddit user profile URL: ").strip()
    username = extract_username(profile_url)
    print(f"[INFO] Scraping data for u/{username}...")

    posts, comments = scrape_user_data(username)
    print(f"[INFO] Fetched {len(posts)} posts and {len(comments)} comments.")

    print("[INFO] Generating user persona using GPT...")
    persona_text = generate_persona(username, posts, comments)  # ✅ Pass username

    save_to_file(username, persona_text)

if __name__ == "__main__":
    main()
