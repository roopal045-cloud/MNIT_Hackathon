# backend/test_llm_debug.py - shows exactly what Gemini sent back.
import sys

from app.services import llm
from app.services.rag import search

sys.stdout.reconfigure(encoding="utf-8")

QUESTION = "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"

r = search(QUESTION, n=3)
for c in r["chunks"]:
    print("chunk page", c["page"], "| score", c["score"], "| contains '72 hours':", "72 hours" in c["text"] or "72 Hours" in c["text"])

source_text = "\n\n".join(c["text"] for c in r["chunks"])
prompt = "Language: Marathi\n\nSOURCE:\n" + source_text + "\n\nQUESTION:\n" + QUESTION

client = llm._get_client()
resp = client.models.generate_content(
    model=llm.MODEL,
    contents=prompt,
    config=llm.types.GenerateContentConfig(system_instruction=llm.SYSTEM, temperature=0.2),
)
print("RAW REPLY:", repr(resp.text))
try:
    print("finish reason:", resp.candidates[0].finish_reason)
except Exception as e:
    print("finish reason: not available", e)
print("prompt feedback:", getattr(resp, "prompt_feedback", None))