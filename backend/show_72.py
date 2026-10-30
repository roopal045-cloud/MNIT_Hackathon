# backend/show_72.py - top 8 chunks; for each, shows the words around "72 hours" if present.
import sys

from app.services.rag import search

sys.stdout.reconfigure(encoding="utf-8")

QUESTIONS = [
    "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?",
    "शेतात पाणी साचून पिकाचे नुकसान झाले, विमा कंपनीला किती तासांत कळवावे?",
    "गारपीट झाल्यावर शेतकऱ्याने किती तासांत नुकसानीची माहिती द्यावी?",
]

for q in QUESTIONS:
    r = search(q, n=8)
    print("=" * 60)
    print("Q", QUESTIONS.index(q) + 1)
    for i, c in enumerate(r["chunks"], start=1):
        t = c["text"]
        pos = t.find("72 hours")
        if pos < 0:
            pos = t.find("72 Hours")
        around = t[max(0, pos - 100):pos + 60] if pos >= 0 else "-"
        print(" ", i, "page", c["page"], "score", c["score"], "| around 72 hours:", around)