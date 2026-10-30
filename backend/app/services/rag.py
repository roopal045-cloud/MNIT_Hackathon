# backend/app/services/rag.py
# Finds the best text chunks for a question from data/processed/chroma.
# Used by /ask. Gemini (llm.py) only words what is found here.

from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# services -> app -> backend -> project root
DB_PATH = Path(__file__).resolve().parents[3] / "data" / "processed" / "chroma"
MODEL_NAME = "intfloat/multilingual-e5-base"  # same model as data/ingest.py

# Words that tell us which scheme a question is about (Hindi, Marathi, English).
SCHEME_WORDS = {
    "pmkisan": ["किसान सम्मान", "सम्मान निधि", "सन्मान निधी", "पीएम किसान", "पीएम-किसान",
                "pm kisan", "pm-kisan", "pmkisan", "6000", "६०००", "6,000"],
    "pmmvy": ["मातृ वंदना", "मातृ वन्दना", "गर्भवती", "गरोदर", "प्रसूत", "प्रसव",
              "pmmvy", "matru", "pregnan", "maternity"],
    "pmfby": ["फसल बीमा", "पीक विमा", "फसल", "पीक", "बीमा", "विमा", "नुकसान", "खराब",
              "बारिश", "बारीश", "पाऊस", "पावसा", "ओला", "गारपीट", "कपास", "कापूस", "दावा",
              "pmfby", "crop", "insurance", "claim", "hailstorm", "flood"],
}
# PM-Kisan and PMMVY are checked before PMFBY because PMFBY words are very general.
CHECK_ORDER = ["pmkisan", "pmmvy", "pmfby"]

_model = None
_collection = None


def _load():
    # Load the model and the database only once, the first time they are needed.
    global _model, _collection
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
        _collection = chromadb.PersistentClient(path=str(DB_PATH)).get_collection("dhara_docs")
    return _model, _collection


def guess_scheme(question):
    # Returns "pmkisan", "pmmvy", "pmfby", or None if we cannot tell.
    q = (question or "").lower()
    for scheme in CHECK_ORDER:
        if any(w in q for w in SCHEME_WORDS[scheme]):
            return scheme
    return None


def _adjust(text):
    # Small nudge so PMFBY standing-crop (localized calamity) text ranks above post-harvest text.
    t = text.lower()
    bonus = 0.0
    if "21.5" in t or "localized" in t or "localised" in t:
        bonus += 0.05
    if "post harvest" in t or "post-harvest" in t or "21.4" in t:
        bonus -= 0.05
    return bonus


def search(question, n=3):
    # Returns {"scheme": ..., "chunks": [{"text", "doc", "page", "scheme", "score"}]}
    # score is between 0 and 1 (higher is closer). The first chunk is the best.
    if not question or not question.strip():
        return {"scheme": None, "chunks": []}
    model, collection = _load()
    scheme = guess_scheme(question)
    vec = model.encode(["query: " + question], normalize_embeddings=True).tolist()
    kwargs = {"query_embeddings": vec, "n_results": max(n * 3, 8)}
    if scheme:
        kwargs["where"] = {"scheme": scheme}
    res = collection.query(**kwargs)
    chunks = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        score = 1 - dist
        if meta["scheme"] == "pmfby":
            score += _adjust(doc)
        chunks.append({
            "text": doc,
            "doc": meta["doc"],
            "page": meta["page"],
            "scheme": meta["scheme"],
            "score": round(score, 3),
        })
    chunks.sort(key=lambda c: -c["score"])
    return {"scheme": scheme, "chunks": chunks[:n]}