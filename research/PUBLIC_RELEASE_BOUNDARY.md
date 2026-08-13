# Public Release Boundary (Phase E, Task 5)

> Defines what can and cannot enter (A) the manuscript, (B) the arXiv source package, (C) the public
> GitHub repository. Documents the boundary; does not delete, redact, or modify anything. Repository
> was inspected directly (grep sweeps + spot-read of outputs + git-history check) on 2026-08-12 —
> findings below, not assumptions carried from `METHODOLOGY.md`'s own description of itself.

---

## 1. Inspection performed this pass

- Grepped the full tracked tree for: AWS credential patterns (`AKIA...`, `amazonaws.com`, `s3://`,
  `X-Amz-`, `AWS_SECRET`), private-key headers, `GROQ_API_KEY=gsk_...` literals, real Romanian
  tax-ID/company-name patterns (`CUI`, `CIF`, named real companies e.g. "Rompetrol", "OMV Petrom"),
  email addresses, Romanian phone-number patterns, and signed-URL query-string patterns
  (`signature=`, `Expires=`).
- Spot-read `data/outputs/invoice_lines_all_companies.csv`, `product_account_mapping.csv`,
  `gl_statistics.csv`, `invoice_statistics.csv` — confirmed all company names are `SYNTH COMPANY
  0NN SRL` with CUIs in a fake `99000NN` range, all product/account data synthetic.
- Checked full git history (`git log --diff-filter=A --name-only --all`) for any historically-added
  real receipt/client files — found only synthetic `synth-receipt-0N.analyze_expense.json` fixtures;
  no real file was ever added to *this* repository's history (consistent with `STATE.md`'s account
  that this repo was created fresh on 2026-07-28 specifically to avoid carrying the private client
  repo's history).
- Confirmed no `.env` or credential file is tracked (`git ls-files` search for
  `.env`/`credential`/`secret` returned nothing).

## 2. Findings

**No client data, CUIs, account identifiers, credentials, signed URLs, or PII were found in the
tracked repository.** This matches `METHODOLOGY.md`'s own description of the anonymization pass and
is independently re-confirmed here, not merely taken on faith.

**One internal-operational detail found, already public, low sensitivity, but flagged:**
`STATE.md` names an AWS IAM username (`contai-textract`) and region (`ap-south-1`) used during Phase
2's OCR work. This is not a secret (no key material, just a resource *name*) and is already committed
to the public GitHub repo — this document does not ask for it to be removed (out of scope, "do not
delete anything"), but it should **not** be carried into the manuscript or arXiv package, which
currently don't reference it anyway (verified — `TECHNICAL_REPORT.md` describes the OCR provider
generically as "AWS Textract's `AnalyzeExpense`" with no account/resource-name detail).

**One content-accuracy issue, not a confidentiality issue, carried over from
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §3-4:** `TECHNICAL_REPORT.md` §3.2/§3.3 still cite pre-A5-fix
superseded synthetic figures, and §5 still contains a factually-contradicted vendor-practice
sentence. Neither is a leak; both are pre-existing, already-documented issues (`RESEARCH_AUDIT.md`,
`CONTRIBUTION_LOCK.md` §7) that a Phase-E draft must not silently inherit.

## 3. What can and cannot enter each destination

### A. Manuscript

| Allowed | Not allowed |
|---|---|
| ADS formula, decision-procedure description, cascade design (methodology — already public) | Any real company/CUI/vendor identifier (none exist in the repo; stays that way) |
| Production **aggregate statistics**, cited as such (91.2% deterministic, 0.847/0.964 ADS, 0.695 cross-company consistency, etc.) — per `METHODOLOGY.md`'s existing public/confidential table | Raw production invoice lines, receipt images, or any row-level production data (none exist in the repo) |
| Full synthetic Experiment 1 result table/statistics | AWS IAM usernames, regions, account IDs, or any other internal-infrastructure identifier (e.g. `contai-textract`) |
| Citation-ledger-verified literature claims | UNVERIFIED-status citations presented without their ledger caveat |
| The case study framed explicitly as "cited, not reproduced" | The case study framed as independently-reproducible evidence |

### B. arXiv source package

Everything in column A above, restricted further to exactly what `main.tex` + `references.bib`/`.bbl`
+ referenced figures need (per `MANUSCRIPT_FORMAT_RESEARCH.md` §1.4/§1.15). Explicitly excluded from
the *source package* even though it's fine for the manuscript's prose or the public repo generally:

- Internal research-governance docs (`CONTRIBUTION_LOCK.md`, `AUDIT_REPORT.md`,
  `RESEARCH_GPS.md`, this document, etc.) — these stay in the GitHub repo for methodological
  transparency but are not part of the arXiv *paper source*.
- Any LaTeX build artifact (`.aux`/`.log`/etc.) or unused figure draft.
- Full raw `final_condition_results.csv` — link to its public GitHub path in the Reproducibility
  section rather than bundling the CSV into the arXiv tarball (keeps the source package lean per the
  50MB-cap discussion in `MANUSCRIPT_FORMAT_RESEARCH.md` §1.7, and the canonical copy already lives in
  the versioned public repo, so bundling would create a second, driftable copy).

### C. Public GitHub repository

Already public (per `STATE.md`, this repo was published and Zenodo-archived at `v1.0.0`,
DOI `10.5281/zenodo.21644208`). This pass found nothing that should be walked back — the existing
public/confidential boundary documented in `METHODOLOGY.md` holds up under direct re-inspection.
Going forward (Phase E2 onward), the same rule applies to every new file added: no client data, no
real company/CUI/vendor names beyond the already-anonymized `SYNTH`/fictitious examples, no
credentials, no internal infrastructure identifiers.

## 4. Standing rule for the rest of Phase E

Before any new file is added to `manuscript/` (Phase E2 onward) or staged for the arXiv package
(Phase E7), re-run this same grep/spot-check sweep — cheap, and it is the only defense against a
draft accidentally quoting an internal doc verbatim (internal docs sometimes discuss the case study
in more operational detail than the public boundary permits, precisely because they're written for a
research-audit audience, not a public one).

## 5. Verdict

**No corrective action required on the current repository state.** The boundary documented in
`METHODOLOGY.md` matches what's actually in the tree. The two items worth carrying forward are
process reminders, not fixes: don't let the IAM-username-level detail leak upward into the manuscript
(it hasn't), and don't let the manuscript inherit `TECHNICAL_REPORT.md`'s two known-stale numeric/
prose issues without a deliberate decision (tracked in `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §4).
