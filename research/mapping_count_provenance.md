# Provenance Investigation — "76,843 vs ~55,394" mapping count

> Follow-up to Research Audit finding A2. Investigation only; no source files were modified as
> part of this document (script executions performed for A3 are logged separately in
> `determinism_provenance.md` and did not touch mapping-count artifacts).

## The claim under investigation

`ROADMAP.md` (Phase A task) and `STATE.md` (Resume prompt) both assert that there is an unresolved
discrepancy between a mapping count of **76,843** and "a different mapping count (**~55,394** seen
in older docs)". This document performs the complete provenance search the audit specified and
reports the result.

## What 76,843 is and where it comes from

**Fully traceable.** `reports/phase1_final_report.md` §6 ("Product-to-Account Mapping") states:

> "The product account mapping table contains **76,843 unique (company, product, account)** tuples,
> representing the ground truth for how each company classifies each product."

This is a production-run output of `scripts/03_invoice_line_extraction.py` writing
`product_account_mapping.csv` from the confidential D406 corpus (296,648 invoice lines, 169
companies). The figure is repeated identically and consistently in:
- `TECHNICAL_REPORT.md` §2.1
- `README.md`'s results table
- `architecture/DECISIONS.md` ADR-003 ("The D406 corpus (76,843 (company, product, account)
  mappings) is the only training data that exists on day one")
- `architecture/DECISIONS.md` ADR-004

No other document in this repository states a conflicting value for this specific quantity
("distinct (company, product, account) tuples from the full production corpus"). **76,843 is
internally consistent across every citation in this repository.**

## Complete provenance search for ~55,394

Per the audit task, the following searches were run and are reproducible:

| # | Search | Command (conceptually) | Result |
|---|---|---|---|
| 1 | Current working tree, all tracked+untracked text files | `grep -rn "55,394\|55394"` over the repo root | Zero matches in any file **except** `STATE.md` and `ROADMAP.md`'s own sentences describing this open question |
| 2 | Full reachable git history, all commits, content search | `git log --all -p \| grep "55,394\|55394"` across all 8 commits on `main` | Zero matches |
| 3 | Tags / other branches | `git tag -l`, `git branch -a` | No tags exist; only branch is `main` (plus its `origin/main` remote-tracking ref) — nothing to search beyond what #2 already covered |
| 4 | Deleted files, across all history | `git log --diff-filter=D --summary --all` | Only two files were ever deleted in this repo's history: `CONTINUATION_PROMPT.md` and `REFINED_REPORT.md` (removed in commit `3e895c4`, per `STATE.md`'s own record: "internal-only, not part of the public package"). Both deleted files' full historical content is included in search #2 (`git log --all -p` covers deletions too) — neither contained the figure. |
| 5 | Commit messages | `git log --all --format="%h %s"` | No commit message mentions "mapping," "55,394," or "55394" |
| 6 | Dangling / unreachable git objects (reflog, orphaned amends) | `git fsck --unreachable --no-reflogs`, then `git cat-file -p <obj>` on every result | One dangling commit found (`80cb69a`, the pre-amend version of the initial commit) plus its associated dangling blob/trees. Inspected directly: the amend that superseded it (`80cb69a` → `81fb74e`) only removed a pre-anonymization draft of `docs/demo/index.html` (825 lines, purely front-end HTML/CSS/JS for the interactive demo) — no numeric mapping-count content, and no match for `55,394`/`55394` in any dangling object. |
| 7 | Reflog (all refs) | `git reflog show --all` | Confirms the repository's complete history: 8 real commits + 1 pre-amend dangling commit, nothing else. This repository was created fresh on 2026-07-28 (per `STATE.md`'s own record) specifically so it would never contain the private client repo's commit history — so there is no "earlier version of this repo" to search further back than its own initial commit. |

**Result: `~55,394` does not exist anywhere in this repository — not in any tracked file, any
untracked file, any commit (reachable or unreachable), any deleted file, any commit message, any
tag, or any branch.**

## Hypotheses considered and explicitly not adopted

The audit instructions require determining whether 55,394 is a different metric definition, an
earlier dataset version, a private/removed artifact, or an unsupported number — **without
inferring the answer**. The following candidate arithmetic relationships were checked against the
authoritative production figures in `data_verification_audit.md` and `phase1_final_report.md`, to
see whether any *legitimate, derivable* quantity happens to equal ~55,394. **None of them land on
55,394, and none is presented as a conclusion — they are recorded only to show the check was made:**

- 76,843 × 73.9% (production PURCHASE-direction share) ≈ 56,779 — close in magnitude, not equal.
- 76,843 − 16,021 (production duplicate-invoice-line count, unrelated unit) = 60,822 — not equal, and duplicate *lines* is not the same unit as duplicate *mappings* in the first place.
- 62,447 (raw unique products) − 47,306 (normalized unique products) = 15,141 — not equal to 55,394 and not equal to 76,843 − 55,394 (=21,449) either.
- No combination of the "Numbers Confirmed Correct" figures in `data_verification_audit.md`
  produces 55,394 through any single arithmetic operation checked.

**None of these establishes provenance. They rule out the simplest hypotheses; they do not replace
a real source.**

## Determination

**STATUS: UNRESOLVED.**

Per the audit task's explicit instruction ("If the provenance cannot be established from the
repository: mark 55,394 as UNRESOLVED"), this document marks it as such. The two remaining
possible explanations this repository cannot adjudicate:

1. The figure exists only in the private/confidential client repository (a different `product_
   account_mapping.csv` computed at a different point in that repo's history, or under a different
   filter/definition) — genuinely out of reach from this public export.
2. The figure was an approximate/misremembered number introduced during a prior chat session (the
   `/grill-me` interview `STATE.md` references) and never existed as a written artifact anywhere —
   in which case there is nothing to "resolve" because there was never a second real number, only a
   recollection of one.

This document cannot distinguish between these two explanations. Only the human author can, by
checking the private repository directly or their own memory/notes of that session.

## Recommendation

- **Treat 76,843 as canonical** for "(company, product, account) mapping count, production" — its
  provenance is fully and explicitly verified (`reports/phase1_final_report.md` §6), independent of
  whatever 55,394 turns out to be, per the audit task's own rule ("treat 76,843 as the canonical
  value only if its provenance is explicitly verified" — it is).
- **Remove the "~55,394" framing from `ROADMAP.md`'s Phase A task list**, or reword it to state
  plainly that the figure is unsourced and the discrepancy could not be substantiated by this
  repository, so it stops reading as an open, resolvable-from-here question. See Question F1 in
  `RESEARCH_AUDIT.md`.
- Do **not** publish "~55,394" anywhere in `TECHNICAL_REPORT.md` or any other public-facing
  document — it is not currently a citable number.
