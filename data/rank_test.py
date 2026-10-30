# data/rank_test.py - where does the chunk with "72 hours" rank for different questions?
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "processed" / "chroma"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
col = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")

TESTS = [
    ("MR", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"),
    ("HI", "फसल खराब होने पर कितने घंटे में सूचना देनी है?"),
    ("EN", "Within how many hours must the farmer report crop loss from hailstorm or flooding?"),
    ("EN2", "immediate intimation within 72 hours by the insured farmer"),
]

for name, q in TESTS:
    vec = model.encode([q], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=vec, n_results=40, where={"scheme": "pmfby"})
    rank = None
    for i, doc in enumerate(res["documents"][0], start=1):
        if "72 hours" in doc or "72 Hours" in doc:
            rank = i
            break
    print(name, "-> first chunk with '72 hours' is at rank:", rank if rank else "not in top 40")