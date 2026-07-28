# Synthetic Data Strategy — Realistic Plan

> After reviewing the full pipeline (Phase 1: 6 scripts, Phase 2: 7 scripts + p2lib, 17 architecture docs, interactive demo), here's the honest assessment.

---

## The Dependency Chain

I traced every file-reads-file link in the pipeline. Here's the actual chain:

```
Dev-D406-Dataset.json (source manifest)
  │
  ├─► 01_build_inventory.py ──► companies_inventory.csv, metadata.csv
  │
  ├─► 01_5_xml_normalization.py ──► data/normalized/*.xml
  │                                     │
  │                                     ├─► 02_gl_account_extraction.py ──► company_gl_accounts.csv
  │                                     │                                   company_gl_catalog.json
  │                                     │
  │                                     └─► 03_invoice_line_extraction.py ──► invoice_lines_all_companies.csv
  │                                                                           product_account_mapping.csv
  │
  └─── 03_5_dataset_intelligence.py ◄── (reads invoice_lines + gl_accounts)
       │                                ──► intelligence/*.csv (ADS, consistency, quality)
       │
       └─► 04_architecture_decision.py ──► architecture_decision.md
                                            decision_matrix.csv, feature_selection.csv

Phase 2 picks up HERE:
  │
  ├─► p2_01_build_kb.py ◄── product_account_mapping.csv + product_ambiguity.csv
  │   ──► kb/product_kb.csv, kb/global_product_kb.csv
  │
  ├─► p2_02_classify_eval.py ◄── invoice_lines_all_companies.csv + product_kb.csv
  │   ──► classification_eval.csv, tier_distribution.csv, per_company_accuracy.csv
  │
  ├─► p2_03_extract.py ◄── Receipts Examples/*.jpg (real photos)
  │   ──► textract_raw/*.json
  │
  ├─► p2_05_end_to_end.py ◄── textract_raw/*.json + product_kb.csv + global_product_kb.csv
  │   ──► e2e_receipts.csv, e2e_classification.csv
  │
  ├─► p2_06_llm_tail.py ◄── e2e_classification.csv + Groq API
  │   ──► llm_tail_proposals.csv
  │
  └─► p2_07_demo_data.py ◄── various Phase 2 CSVs
      ──► demo stats
```

**Bottom line:** Everything traces back to two roots:
1. `Dev-D406-Dataset.json` → the 1,020 XMLs → all Phase 1 outputs
2. `Receipts Examples/*.jpg` → Textract → all Phase 2 receipt outputs

Replace those two roots with synthetic equivalents, and the entire pipeline reproduces.

---

## Three Approaches Considered

### Option A: Git Branch + Manual Scrub
Create a branch, manually replace company names and product names in the CSVs, re-run scripts 03.5 and 04.

**Problem:** You have 90 MB of invoice lines. Manual scrubbing is error-prone, slow, and you'd still need to verify every row. One missed CUI or company name and you've leaked confidential data. Also, the XMLs in `data/normalized/` are 1,020 real files — you can't scrub those.

**Verdict:** ❌ Too risky, too tedious.

### Option B: Fork the Repo, Strip Data, Rebuild
Fork to a new repo, delete all `data/`, write synthetic data by hand, re-run everything.

**Problem:** You'd need to write 296,648 synthetic invoice lines by hand (or write a generator anyway). And you lose git history, which is part of the engineering story.

**Verdict:** ❌ Half-measure. You'd end up writing a generator regardless.

### Option C: Synthetic Data Generator Script ✅
Write **one script** (`scripts/00_generate_synthetic.py`) that produces statistically-equivalent synthetic data at the root of the pipeline. Then every downstream script runs unchanged.

**This is the right approach.** Here's why:

1. **Scripts don't change.** The pipeline logic (your methodology) stays bit-for-bit identical.
2. **One new file.** The generator is the only new code.
3. **Proves the methodology is data-agnostic.** If the same scripts produce the same *kind* of results on synthetic data, that's a stronger research claim than "it worked on our private dataset."
4. **Git branch is clean.** `research` branch has: same scripts, one new generator, zero confidential data.

---

## What the Synthetic Generator Needs to Produce

The generator replaces the real data *at the pipeline entry points*. Here's exactly what it needs to create:

### Tier 1: Source Replacement (replaces real XMLs)

Instead of generating 1,020 fake XMLs and re-running Scripts 01–03 (which would require faking the D406 schema), we skip straight to producing the **CSV outputs** that Scripts 01–03 would have produced. This is simpler and equivalent — the scripts are proven; what matters for research is the downstream analysis.

| File to Generate | What It Contains | Statistical Properties to Preserve |
|---|---|---|
| `companies_inventory.csv` | 169 fake companies with fake CUIs, fake names, fake CAEN codes | Same count, same column schema |
| `company_gl_accounts.csv` | ~154K GL account records | Same distribution: avg 766/company, min 2, max 14,806 |
| `invoice_lines_all_companies.csv` | ~296K lines | Same ADS distribution (91.2% deterministic), same direction split (73.9/26.1), same VAT rates, same missing-data pattern |
| `product_account_mapping.csv` | ~76K (company, product, account) tuples | Same frequency distribution, same ambiguity profile |
| `company_gl_catalog.json` | O(1) lookup | Derived from gl_accounts.csv |

### Tier 2: Receipt Replacement (replaces real photos)

For receipts, we can't generate fake photos (Textract needs real images). Two options:

**Option A:** Use publicly available receipt images (there are open datasets — SROIE, CORD, etc.) and run Textract on those.
**Option B:** Skip p2_03 entirely and hand-write 5–10 fake `textract_raw/*.json` files that mimic the Textract output schema. The structuring code (`p2lib/structure.py`) only reads JSON, not images.

**Recommendation:** Option B. It's faster, costs $0, and proves the pipeline works on any Textract output.

### Tier 3: What Stays Identical (Zero Changes)

| Component | Why It Doesn't Change |
|---|---|
| All 6 Phase 1 scripts (logic) | They ARE the methodology |
| All Phase 2 scripts (p2_01 through p2_07) | They ARE the methodology |
| p2lib/ (cascade, structure, normalize, AI adapter) | Core library, data-agnostic |
| architecture/ (17 design docs) | No data in these |
| config/settings.py | Configuration, not data |
| utils/ | Utilities, not data |
| prerun_check.py | Validation logic |
| reports/*.md, docs/*.md | Can regenerate from synthetic runs |

---

## The Execution Plan

### Step 1: Create the `research` Branch
```
git checkout -b research
```
One branch. Clean separation. `main` = confidential work project. `research` = publishable methodology.

### Step 2: Write `scripts/00_generate_synthetic.py`
This is the key new file. It:
1. Reads the **statistical profiles** from the real data (distributions, not values)
2. Generates synthetic companies, products, accounts, invoice lines
3. Preserves: ADS distribution, cross-company consistency (~0.695), VAT stability (94.5%), direction split, company size skew
4. Writes to the same file paths as Phase 1 outputs

**This script runs on `main` (reads real stats) and produces files that go on `research` (synthetic data).**

### Step 3: Delete Confidential Data from `research` Branch
```
# On research branch:
rm -rf data/normalized/          # Real XMLs
rm -rf data/downloads/           # Real downloads
rm -rf data/source_of_truth/     # Real manifest
rm -rf Receipts\ Examples/       # Real receipt photos
rm data/outputs/phase2/textract_raw/*   # Real OCR output
rm data/outputs/phase2/llm_cache/*      # Real LLM responses
```

Replace with synthetic equivalents from Step 2.

### Step 4: Re-run Scripts 03.5 → 04 → Phase 2
On the `research` branch, with synthetic data in place:
```
python scripts/03_5_dataset_intelligence.py    # Recompute ADS, consistency
python scripts/04_architecture_decision.py     # Recompute decisions
python scripts/phase2/p2_01_build_kb.py        # Rebuild KB
python scripts/phase2/p2_02_classify_eval.py   # Re-evaluate cascade
```

The results should be **statistically similar** (not identical — that's the point) to the real run.

### Step 5: Write a `METHODOLOGY.md`
Describes: what the generator preserves (distributions), what it doesn't (identities), and why the pipeline results are valid on synthetic data.

### Step 6: Verify and Commit
- Grep the entire `research` branch for any leaked company names, CUIs, or real product names
- Ensure all scripts still run end-to-end
- Commit. This branch is your publishable artifact.

---

## What You Get at the End

```
research branch
├── scripts/
│   ├── 00_generate_synthetic.py    ← NEW (only new file)
│   ├── 01_build_inventory.py       ← UNCHANGED
│   ├── 01_5_xml_normalization.py   ← SKIPPED (no real XMLs to process)
│   ├── 02_gl_account_extraction.py ← SKIPPED (generator produces its output)
│   ├── 03_invoice_line_extraction.py ← SKIPPED (generator produces its output)
│   ├── 03_5_dataset_intelligence.py  ← RUNS on synthetic data
│   ├── 04_architecture_decision.py   ← RUNS on synthetic data
│   └── phase2/                       ← ALL RUN on synthetic data
├── architecture/                     ← UNCHANGED (no data here)
├── docs/                             ← UNCHANGED
├── METHODOLOGY.md                    ← NEW
├── data/outputs/                     ← SYNTHETIC (regenerated)
└── (no normalized/, no source_of_truth/, no Receipts Examples/)
```

**The scripts are the methodology. The data is synthetic. The results validate the methodology.**

---

## Why NOT a Separate Repo

A branch is better because:
1. Git history shows the evolution (Phase 1 → Phase 2 → research branch)
2. You can cherry-pick fixes between `main` and `research`
3. The `.gitignore` already handles `.env` and API keys
4. One repo, two audiences: `main` for your employer, `research` for academia

---

## Realistic Timeline

| Step | Effort | Notes |
|------|--------|-------|
| Write synthetic generator | 1–2 days | The hardest part: getting the statistical distributions right |
| Strip confidential data | 30 min | Just deletions |
| Re-run pipeline | 1 hour | Scripts are fast on 300K rows |
| Verify no leaks | 1 hour | Grep for known company names/CUIs |
| Write METHODOLOGY.md | 2–3 hours | Formalizes what the generator preserves |
| **Total** | **~2–3 days** | |

---

## One Honest Caveat

> Scripts 01, 01.5, 02, and 03 won't *run* on the research branch (no real XMLs to parse). They'll be present as **source code** demonstrating the methodology, but the synthetic generator replaces their *output*, not their *input*.
>
> This is fine for research — you're publishing the pipeline design and the analysis methodology, not an XML parser. But if a reviewer asks "can I run your full pipeline end-to-end?", the answer is: "Scripts 03.5 through Phase 2, yes. Scripts 01–03 require a D406 dataset which we cannot distribute, but the generator produces equivalent intermediate outputs."
>
> This is exactly how medical AI papers work. "Our pipeline processes chest X-rays. We can't give you the X-rays, but here's the pipeline and synthetic outputs that let you validate the downstream analysis."
