"""Look at the ClimateBERT climate_specificity dataset before building anything.

Usage: python scripts/explore_dataset.py
"""

from datasets import load_dataset

ds = load_dataset("climatebert/climate_specificity")
print(ds)

for split in ["train", "test"]:
    df = ds[split].to_pandas()
    counts = df["label"].value_counts().to_dict()
    lengths = df["text"].str.split().str.len()
    print(f"\n{split}: {len(df)} examples")
    print(f"  labels: {counts}   (0 = non-specific, 1 = specific)")
    print(f"  words per example: mean {lengths.mean():.0f}, min {lengths.min()}, max {lengths.max()}")

train = ds["train"].to_pandas()
for label, name in [(1, "SPECIFIC"), (0, "NON-SPECIFIC")]:
    print(f"\n--- 3 {name} examples ---")
    for text in train[train["label"] == label]["text"].head(3):
        print(" *", text[:300].replace("\n", " "), "...\n")

# Note for later: these examples are whole paragraphs, but my tool will
# classify single sentences, so I need to check how well that transfers.
