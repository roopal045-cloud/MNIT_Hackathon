# data/search_filter_test.py - searches only inside ONE scheme.
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

sys.stdout.reconfigure(encoding="utf-8")  # fixes the Devanagari print error

DB_PATH = Path(__file__).parent / "processed" / "chroma"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
collection = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")

TESTS = [
    ("pmkisan", "पीएम किसान योजना में साल में कितने रुपये मिलते हैं?"),
    ("pmkisan", "पीएम किसान योजनेत वर्षाला किती रुपये मिळतात?"),
    ("pmfby", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"),
]

for scheme, question in TESTS:
    vec = model.encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=vec, n_results=3, where={"scheme": scheme})
    print("=" * 60)
    print("SCHEME:", scheme, "| QUESTION:", question)
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        print("  score", round(1 - dist, 2), "| page", meta["page"], "| has 6000:", "6000" in doc or "6,000" in doc, "| has 72:", "72" in doc)