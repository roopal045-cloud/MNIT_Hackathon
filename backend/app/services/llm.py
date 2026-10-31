# backend/app/services/llm.py - empty for now, filled in during Phase 1
# backend/app/services/llm.py
# Gemini is used ONLY to word an answer from source text we give it.
# It never decides eligibility and never answers from its own memory.

import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# backend/.env (git-ignored)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
NOT_FOUND = "NOT_FOUND"

SYSTEM = (
    "You help rural citizens in India. Answer ONLY from the SOURCE text given. "
    "Use very simple words and at most 3 short sentences. "
    "Copy every number, date and amount exactly as written in the SOURCE. "
    "If the SOURCE does not answer the question, reply with exactly NOT_FOUND. "
    "Never give a medical diagnosis. Never give a pesticide dosage. "
    "Reply only in the requested language."
)

_client = None


def _get_client():
    global _client
    if _client is None:
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            return None
        _client = genai.Client(api_key=key)
    return _client


def word_answer(question, source_text, language):
    # Returns a short answer in "hi" or "mr", or None if Gemini fails
    # or the source does not contain the answer.
    client = _get_client()
    if client is None or not question or not source_text:
        return None
    lang_name = "Marathi" if language == "mr" else "Hindi"
    prompt = (
        "Language: " + lang_name + "\n\n"
        "SOURCE:\n" + source_text + "\n\n"
        "QUESTION:\n" + question
    )
    try:
        resp = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(system_instruction=SYSTEM, temperature=0.2),
        )
        text = (resp.text or "").strip()
    except Exception as e:
        print("[llm] failed:", e)
        return None
    if not text or NOT_FOUND in text:
        return None
    return text
