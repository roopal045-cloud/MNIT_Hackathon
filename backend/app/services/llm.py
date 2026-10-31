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
    "Keep every number, date and amount exactly as in the SOURCE, written in digits, "
    "but write units and time words (hours, days, rupees, instalments) in the requested "
    "language, for example 72 तास, 15 दिवस, 6000 रुपये. Never leave English words in the answer. "
    "If the SOURCE contains a rule that helps answer the QUESTION, state that rule in simple words, "
    "even if the question uses a general word like rain and the SOURCE names a specific cause such as "
    "hailstorm or inundation. Only if the SOURCE has nothing relevant, reply with exactly NOT_FOUND. "
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


def word_answer(question, source_text, language, role="farmer"):
    # Returns a short answer in "hi" or "mr", or None if Gemini fails
    # or the source does not contain the answer.
    # If Google is busy (503), we retry, then try a backup model.
    import time

    client = _get_client()
    if client is None or not question or not source_text:
        return None
    lang_name = "Marathi" if language == "mr" else "Hindi"
    prompt = (
        "Language: " + lang_name + "\n\n"
        "SOURCE:\n" + source_text + "\n\n"
        "QUESTION:\n" + question
    )
    if role == "asha":
        prompt += "\n\nFORMAT: The reader is an ASHA health worker. Answer in 2 or 3 very short lines. One short sentence per line. Put each sentence on its own line. No bullet symbols."
    backup = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash")
    attempts = [MODEL, MODEL, MODEL, backup]
    text = ""
    for i, model_name in enumerate(attempts):
        try:
            resp = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(system_instruction=SYSTEM, temperature=0.2),
            )
            text = (resp.text or "").strip()
            break
        except Exception as e:
            print("[llm] failed (" + model_name + "):", str(e)[:120])
            time.sleep(2)
    if not text or NOT_FOUND in text:
        return None
    return text
