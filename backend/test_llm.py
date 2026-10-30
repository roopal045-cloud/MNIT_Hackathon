# backend/test_llm.py - search the documents, then let Gemini word the answer.
import sys

from app.services.llm import word_answer
from app.services.rag import search

sys.stdout.reconfigure(encoding="utf-8")

QUESTION = "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"
LANG = "mr"

r = search(QUESTION, n=3)
source_text = "\n\n".join(c["text"] for c in r["chunks"])
best = r["chunks"][0]
print("Scheme:", r["scheme"], "| best chunk:", best["doc"], "page", best["page"])

answer = word_answer(QUESTION, source_text, LANG)
if answer is None:
    print("GEMINI RETURNED NOTHING (key, model name, or NOT_FOUND). Check the lines above for [llm] failed.")
else:
    print("ANSWER:", answer)
    print("Contains 72:", "72" in answer or "७२" in answer)