# utils.py

import os

def save_to_file(username, persona_text):
    """Save persona text to a file."""
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", f"{username}_persona.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"[INFO] Persona saved to {filepath}")
