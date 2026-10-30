# data/rank_test2.py - tests a stronger embedding model WITHOUT changing the database.
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "processed" / "chroma"
col = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")
model = SentenceTransformer("intfloat/multilingual-e5-base")

TESTS = [
    ("pmfby", ["72 hours", "72 Hours"], "MR", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"),
    ("pmfby", ["72 hours", "72 Hours"], "HI", "फसल खराब होने पर कितने घंटे में सूचना देनी है?"),
    ("pmfby", ["72 hours", "72 Hours"], "EN", "Within how many hours must the farmer report crop loss from hailstorm or flooding?"),
    ("pmkisan", ["6000", "6,000"], "HI", "पीएम किसान योजना में साल में कितने रुपये मिलते हैं?"),
    ("pmkisan", ["6000", "6,000"], "MR", "पीएम किसान योजनेत वर्षाला किती रुपये मिळतात?"),
]

cache = {}
for scheme, words, lang, question in TESTS:
    if scheme not in cache:
        got = col.get(where={"scheme": scheme}, include=["documents"])
        docs = got["documents"]
        vecs = model.encode(["passage: " + d for d in docs], batch_size=16, normalize_embeddings=True)
        cache[scheme] = (docs, vecs)
    docs, vecs = cache[scheme]
    q = model.encode(["query: " + question], normalize_embeddings=True)[0]
    scores = vecs @ q
    order = sorted(range(len(docs)), key=lambda i: -scores[i])
    rank = None
    for r, i in enumerate(order, start=1):
        if any(w in docs[i] for w in words):
            rank = r
            break
    print(scheme, lang, "-> first chunk with the key fact is at rank:", rank)