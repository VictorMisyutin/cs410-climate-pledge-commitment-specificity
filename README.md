# Climate Pledge Specificity Checker

CS410 Text Information Systems course project, by Victor Misyutin (vmisy).

A tool that extracts climate commitments from company sustainability reports,
classifies each one as **specific** (checkable numbers/dates) or **vague**,
explains why, and gives each company an overall specificity score.

## Status: early progress

| Step | Status |
|---|---|
| Repo setup | ✅ done |
| Explore the ClimateBERT `climate_specificity` dataset | ✅ script written (`scripts/explore_dataset.py`) |
| Extract sentences from report PDFs | ✅ first version (`src/extract.py`) |
| Filter for commitment sentences | ✅ first rule-based version (`src/commitments.py`) |
| Collect real sustainability reports | ⏳ next |
| Train specific/vague classifier | ⬜ todo |
| Explanations for each label | ⬜ todo |
| Company-level score | ⬜ todo |
| Simple UI for non-programmers | ⬜ todo |
| Evaluation (ClimateBERT test set + ~200 manually labelled sentences) | ⬜ todo |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage so far

```bash
python scripts/explore_dataset.py                       # dataset size, label balance, examples
python scripts/make_sample_report.py data/reports/sample.pdf   # fake report for testing
python scripts/extract_commitments.py data/reports/sample.pdf  # commitment sentences -> outputs/*.csv
pytest                                                  # basic tests
```

## Data

[climatebert/climate_specificity](https://huggingface.co/datasets/climatebert/climate_specificity):
1,000 train / 320 test paragraphs labelled specific / non-specific (CC BY-NC-SA 4.0).
Note that the labels are for paragraphs, while this tool works on sentences.
