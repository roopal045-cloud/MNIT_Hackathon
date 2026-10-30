# data/check_pdfs.py - checks that each PDF in data/raw has readable text.
from pathlib import Path
from pypdf import PdfReader

RAW = Path(__file__).parent / "raw"

for pdf in sorted(RAW.glob("*.pdf")):
    reader = PdfReader(str(pdf))
    pages = len(reader.pages)
    counts = []
    for page in reader.pages:
        counts.append(len(page.extract_text() or ""))
    empty = sum(1 for c in counts if c < 50)
    print("FILE:", pdf.name)
    print("  pages:", pages, "| total characters:", sum(counts), "| pages with almost no text:", empty)
    mid = reader.pages[pages // 2].extract_text() or ""
    print("  sample from middle page:", mid[:150].replace("\n", " "))
    print()