# backend/test_key.py - shows WHY Gemini returned nothing. Never prints the key.
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")

env_path = Path(__file__).resolve().parent / ".env"
print(".env file exists:", env_path.exists())
load_dotenv(env_path)

key = os.getenv("GEMINI_API_KEY")
print("key found:", bool(key), "| length:", len(key) if key else 0, "| still the placeholder:", key == "your_key_here")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
print("model used:", model)

if key and key != "your_key_here":
    from google import genai

    client = genai.Client(api_key=key)
    try:
        resp = client.models.generate_content(model=model, contents="Reply with exactly one word: hello")
        print("GEMINI WORKS. Reply:", (resp.text or "").strip())
    except Exception as e:
        print("GEMINI ERROR:", str(e)[:300])