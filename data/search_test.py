# data/search_test.py - asks test questions and shows the 3 best chunks for each.
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "processed" / "chroma"
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
collection = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")

QUESTIONS = [
    ("mr", "पावसामुळे कापसाचे नुकसान झाले तर किती तासांत कळवावे?"),
    ("hi", "बारिश से फसल खराब हो गई तो बीमा का दावा कैसे करें?"),
    ("hi", "पीएम किसान योजना में साल में कितने रुपये मिलते हैं?"),
    ("mr", "गर्भवती महिलेला मातृ वंदना योजनेत किती पैसे मिळतात?"),
]

for lang, question in QUESTIONS:
    vec = model.encode([question], normalize_embeddings=True).tolist()
    res = collection.query(query_embeddings=vec, n_results=3)
    print("=" * 70)
    print("QUESTION:", question)
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        print("  score", round(1 - dist, 2), "|", meta["scheme"], "| page", meta["page"])
        print("    ", doc[:160])