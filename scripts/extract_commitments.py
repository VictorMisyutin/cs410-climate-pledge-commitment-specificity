import csv
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from commitments import is_commitment
from extract import pdf_to_sentences


def find_pdfs(args):
    pdfs = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            pdfs += sorted(p.glob("*.pdf"))
        else:
            pdfs += [Path(m) for m in sorted(glob.glob(arg)) if m.lower().endswith(".pdf")]
    return pdfs


pdfs = find_pdfs(sys.argv[1:])
if not pdfs:
    sys.exit("No PDFs found. Usage: python scripts/extract_commitments.py data/reports")

out_dir = Path("outputs")
out_dir.mkdir(exist_ok=True)

for pdf_path in pdfs:
    sentences = pdf_to_sentences(pdf_path)
    commitments = [(page, s) for page, s in sentences if is_commitment(s)]

    print(f"\n=== {pdf_path.name} ===")
    print(f"{len(sentences)} sentences extracted, {len(commitments)} look like commitments:\n")
    
    for page, s in commitments:
        print(f"  [p.{page}] {s}")

    out = out_dir / f"{pdf_path.stem}_commitments.csv"
    
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["page", "sentence"])
        writer.writerows(commitments)
    
    print(f"\nSaved to {out}")
    
    
    