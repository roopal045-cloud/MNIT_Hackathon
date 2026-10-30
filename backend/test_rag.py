# backend/test_rag.py - checks that search() finds the right chunks.
from app.services.rag import search

TESTS = [
    ("MR cotton, hours to report", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?", ["72 hours", "72 Hours"]),
    ("HI crop loss, how to claim", "बारिश से फसल खराब हो गई तो बीमा का दावा कैसे करें?", ["72 hours", "72 Hours", "claim"]),
    ("HI PM-Kisan, money per year", "पीएम किसान योजना में साल में कितने रुपये मिलते हैं?", ["6000", "6,000"]),
    ("MR PMMVY, pregnancy money", "गर्भवती महिलेला मातृ वंदना योजनेत किती पैसे मिळतात?", ["5000", "5,000"]),
]

for label, question, words in TESTS:
    r = search(question)
    best = r["chunks"][0]
    found = any(w in c["text"] for c in r["chunks"] for w in words)
    print(label)
    print("   scheme:", r["scheme"], "| best page:", best["page"], "| best score:", best["score"],
          "| key fact in top 3:", found)