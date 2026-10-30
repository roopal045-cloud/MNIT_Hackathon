# backend/show_chunks.py - prints the 3 chunks the search finds (first 450 characters each).
import sys

from app.services.rag import search

sys.stdout.reconfigure(encoding="utf-8")

QUESTION = "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"
r = search(QUESTION, n=3)
for i, c in enumerate(r["chunks"], start=1):
    print("=" * 60)
    print("CHUNK", i, "| page", c["page"], "| score", c["score"])
    print(c["text"][:450])