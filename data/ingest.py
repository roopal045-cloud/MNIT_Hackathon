# data/ingest.py - cuts the PDFs in data/raw into chunks and loads them into ChromaDB.
# Every chunk keeps: document name, PDF viewer page number, scheme.
import re
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).parent
RAW = HERE / "raw"
DB_PATH = HERE / "processed" / "chroma"

MODEL_NAME = "intfloat/multilingual-e5-base"  # understands Hindi, Marathi, English
CHUNK_SIZE = 900
OVERLAP = 150
MIN_CHARS = 80

# keywords = only keep pages that contain one of these words (None = keep all pages)
DOCS = {
    "Revised_Operational_Guidelines.pdf": {"scheme": "pmfby", "keywords": None},
    "RevisedPM-KISANOperationalGuidelines(English).pdf": {"scheme": "pmkisan", "keywords": None},
    "Mission_Shakti_Guidelines.pdf": {"scheme": "pmmvy", "keywords": ["pmmvy", "matru vandana"]},
}


def clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def chunks_of(text):
    out = []
    start = 0
    while start < len(text):
        piece = text[start:start + CHUNK_SIZE].strip()
        if len(piece) >= MIN_CHARS:
            out.append(piece)
        start += CHUNK_SIZE - OVERLAP
    return out


ids, texts, metas = [], [], []

for filename, info in DOCS.items():
    path = RAW / filename
    if not path.exists():
        print("MISSING FILE, skipped:", filename)
        continue
    reader = PdfReader(str(path))
    kept_pages = 0
    count_before = len(texts)
    for page_number, page in enumerate(reader.pages, start=1):
        page_text = clean(page.extract_text())
        if info["keywords"] and not any(k in page_text.lower() for k in info["keywords"]):
            continue
        kept_pages += 1
        for n, piece in enumerate(chunks_of(page_text), start=1):
            ids.append(info["scheme"] + "-p" + str(page_number) + "-c" + str(n))
            texts.append(piece)
            metas.append({"doc": filename, "page": page_number, "scheme": info["scheme"]})
    print(filename, "-> pages kept:", kept_pages, "| chunks:", len(texts) - count_before)

print("Total chunks:", len(texts))
print("Loading embedding model (first time it downloads about 470 MB, please wait)...")
model = SentenceTransformer(MODEL_NAME)
vectors = model.encode(["passage: " + t for t in texts], batch_size=16, show_progress_bar=True, normalize_embeddings=True)

DB_PATH.mkdir(parents=True, exist_ok=True)
client = chromadb.PersistentClient(path=str(DB_PATH))
try:
    client.delete_collection("dhara_docs")
except Exception:
    pass
collection = client.create_collection("dhara_docs", metadata={"hnsw:space": "cosine"})

for i in range(0, len(texts), 500):
    collection.add(
        ids=ids[i:i + 500],
        documents=texts[i:i + 500],
        metadatas=metas[i:i + 500],
        embeddings=vectors[i:i + 500].tolist(),
    )

print("DONE. Stored", collection.count(), "chunks in", DB_PATH)