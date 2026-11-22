"""Extract commitment sentences from a report PDF and save them to a CSV.

Usage: python scripts/extract_commitments.py data/reports/some_report.pdf
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from commitments import is_commitment  # noqa: E402
from extract import pdf_to_sentences  # noqa: E402

pdf_path = sys.argv[1]
sentences = pdf_to_sentences(pdf_path)
commitments = [(page, s) for page, s in sentences if is_commitment(s)]

print(f"{len(sentences)} sentences extracted, {len(commitments)} look like commitments:\n")
for page, s in commitments:
    print(f"  [p.{page}] {s}")

out = Path("outputs") / f"{Path(pdf_path).stem}_commitments.csv"
out.parent.mkdir(exist_ok=True)
with open(out, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["page", "sentence"])
    writer.writerows(commitments)
print(f"\nSaved to {out}")
