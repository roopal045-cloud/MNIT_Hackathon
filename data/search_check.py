# data/search_check.py - plain-English check (no Devanagari in the output).
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "processed" / "chroma"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
col = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")


def pages_with(scheme, words):
    got = col.get(where={"scheme": scheme}, include=["documents", "metadatas"])
    pages = set()
    for doc, meta in zip(got["documents"], got["metadatas"]):
        if any(w in doc for w in words):
            pages.add(meta["page"])
    return sorted(pages)


print("PART 1: which pages contain the key facts?")
print("  pmkisan pages with 6000 or 6,000:", pages_with("pmkisan", ["6000", "6,000"]))
print("  pmfby pages with '72 hours':", pages_with("pmfby", ["72 hours", "72 Hours"]))
print("  pmmvy pages with 5000 or 5,000:", pages_with("pmmvy", ["5000", "5,000"]))

TESTS = [
    ("pmkisan", "HI", "पीएम किसान योजना में साल में कितने रुपये मिलते हैं?", ["6000", "6,000"]),
    ("pmkisan", "MR", "पीएम किसान योजनेत वर्षाला किती रुपये मिळतात?", ["6000", "6,000"]),
    ("pmfby", "MR", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?", ["72 hours", "72 Hours"]),
    ("pmfby", "HI", "फसल खराब होने पर कितने घंटे में सूचना देनी है?", ["72 hours", "72 Hours"]),
]

print()
print("PART 2: best 5 results inside one scheme (page numbers, and does the fact appear?)")
for scheme, lang, question, words in TESTS:
    vec = model.encode([question], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=vec, n_results=5, where={"scheme": scheme})
    hits = []
    for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
        hits.append(str(meta["page"]) + (" YES" if any(w in doc for w in words) else " no"))
    print("  ", scheme, lang, "->", ", ".join(hits))