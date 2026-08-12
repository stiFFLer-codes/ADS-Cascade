# Audit Report — Gate 4 Final Verification Pass (Wording-Fix Confirmation)

> Independent audit. This is the third Gate-4 pass on this document: pass 1 verified numeric
> accuracy (PASS); pass 2 audited claim-strength/wording and returned CONDITIONAL with four required
> fixes (F1-F4); this pass verifies those five edits (F4 was satisfied by two edits) actually landed
> correctly, resolved what F1-F4 raised, and introduced nothing new. Re-derived independently, not a
> re-trust of either prior pass's word.

## 1. Repository state

- Branch: `main`. HEAD: `572e1b7` — "Phase D.1: analyze Experiment 1 evidence." No new commit.
- Working tree (`git status --porcelain`): exactly three entries — `M research/AUDIT_REPORT.md` (this
  file, being overwritten), `?? research/CONTRIBUTION_LOCK.md`, `?? research/contribution_lock.csv`.
  `git status --porcelain -- data/outputs/experiments/exp1/final/` returned empty (frozen evidence
  untouched). `git status --porcelain -- README.md TECHNICAL_REPORT.md METHODOLOGY.md` returned empty
  (no manuscript file touched).
- Diffed/verified: `research/CONTRIBUTION_LOCK.md` read in full, fresh, this pass (418 lines);
  `research/contribution_lock.csv` read in full, fresh (11 rows); the prior `research/AUDIT_REPORT.md`
  read first for the exact F1-F4 text and proposed fixes, then independently checked against the live
  file rather than trusted; `data/outputs/experiments/exp1/final/final_condition_results.csv`
  independently re-aggregated via PowerShell (`Import-Csv`/`Group-Object`/`Where-Object`, Python
  unavailable in this shell) for winner-constancy, band-agreement, and Pearson-correlation checks (own
  from-scratch Pearson implementation, not reused from either prior pass); `research/RESEARCH_GPS.md`
  (Gate 4 checkbox status, DO NOT CHASE list); `research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §9 (H1
  verdict cross-check).

## 2. Current research GPS

Phase D.1 complete; current gate = Contribution Lock (Gate 4). `RESEARCH_GPS.md` line 58 still shows
Gate 4 as `⬜` (unchecked) as of this read — expected and correct, since checking that box is the
human/builder's action, not an auditor's, and this pass does not alter `RESEARCH_GPS.md`. DO NOT CHASE
list (lines 70-85) re-read fresh: still current, nothing in this wording-only pass touches any item on
it (no new experiment, no threshold re-tuning, no vendor/model work). North star = defensible
manuscript draft → reproducibility package → arXiv preprint; closing Gate 4 with locked, correctly
scoped wording is directly on that path, not a detour.

## 3. Changed files

- **Docs (untracked, unchanged from prior pass except the five described edits):**
  `research/CONTRIBUTION_LOCK.md` — the document under audit.
- **Data (untracked, confirmed NOT touched this round):** `research/contribution_lock.csv`.
- **Code:** none changed.
- **Experimental artifacts:** none changed; `data/outputs/experiments/exp1/final/` confirmed untouched
  by `git status`.
- **Manuscript:** none touched (`README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md` absent from
  `git status` output).
- **Audit report:** `research/AUDIT_REPORT.md` — this file, overwritten per instructions.

## 4. Research integrity

**All five described edits independently located, read in full context, and confirmed to say what the
brief claims:**

1. §2 step 9 (line 97-99): now reads "...historical consistency predicts mechanism-level accuracy but
   not mechanism ranking, when, as observed in this synthetic experiment, ranking is governed by a
   representation-stability property the consistency signal is blind to by construction." — the
   inserted clause is grammatically integrated (comma-bounded appositive), not a bolted-on fragment.
2. §3 C2b bullet (line 121-124): now reads "...ranking is governed by a separately-manipulated (in
   this factorial design), ADS-blind representation-stability factor" — reads coherently; the
   parenthetical scopes "separately-manipulated" without breaking the sentence.
3. §5 Formulation #2 table, "Claim" cell (line 188): same replacement, "...that ranking is governed by
   a separately-manipulated (in this factorial design) representation-stability factor
   (lexical/surface-form noise) the consistency signal does not capture." — reads coherently inside the
   table cell.
4. §6 "Synthesis" paragraph (lines 216-221): now opens "In this synthetic experiment, historical
   decision consistency is informative about classification-mechanism *difficulty*, not about
   mechanism *ranking*, when — as observed here — ranking is governed by a representation-stability
   property the consistency signal does not observe — a narrower, more specific, and empirically
   falsifiable-and-partly-falsified refinement..." — both insertions present, both grammatically
   integrated, sentence still reads as one coherent claim rather than two clauses stitched together.
5. §11.C (lines 369-373): fully replaced, verbatim match to the brief's specified text — "In this
   experiment, the consistency-based decision rule agreed with the empirically best mechanism in 100%
   of definable comparisons in the 0.70–0.90 realized-ADS band, but in 0% of definable comparisons in
   the ≥0.90 realized-ADS band; under the tested synthetic perturbation, the empirical winner was
   separated by the lexical-noise condition, which the consistency signal did not observe." Confirmed
   byte-for-byte against the brief.

**F1-F4 resolution, checked directly, not assumed:**

- Grepped the entire document for `governed`: exactly four remaining occurrences (lines 98, 122, 188,
  218), matching the four originally-flagged locations (F1=§6/line~216→218, F2 originally at
  §11.C/line~369 was *removed* by full replacement rather than re-scoped in place, F3=§2/line~98, and
  the §5 table row is the same textual instance F4 also covers at line~187→188). **Every one of the
  four remaining `governed` instances now carries an inline, same-sentence scope qualifier** ("as
  observed in this synthetic experiment," / "separately-manipulated (in this factorial design)" ×2 /
  "as observed here —"). No sixth unscoped instance found anywhere in the document.
- Grepped for `orthogonal`: **zero occurrences** in `CONTRIBUTION_LOCK.md`. F4 fully resolved — the
  word was replaced at both flagged locations (§3 bullet, §5 table cell), not merely glossed.
- Grepped for `entirely`: one occurrence remains, at line 127 ("Exp1 explicitly bypasses the shipped
  cascade **entirely**") — an unrelated, pre-existing sentence about scope, not the flagged
  §11.C "governed entirely" construction, which no longer exists anywhere in the document (fully
  replaced). F2 resolved — §11.C no longer contains "entirely" + "governed" in any combination,
  extractable or otherwise.
- **No resurrected rejected claim found.** Re-read §7's rejected-claims list and its grep-check log in
  full; re-read §3's per-claim table; nothing upgraded, no "novel," "validates," "universally,"
  "proves," or unconditional-selection language found asserted as true anywhere (only inside
  correctly-negated disclaimers, consistent with the prior pass's finding).

## 5. Scientific consistency

- **H1 cross-check:** `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §9 re-read directly this pass: verdict is
  **PARTIALLY_SUPPORTED** (line 106), with the same 100%/10% (2/20 nominal-band) split and the same
  "CLEAN provides zero evidence" framing `CONTRIBUTION_LOCK.md` §2 step 7 restates. `CONTRIBUTION_LOCK.md`
  correctly distinguishes the checkpoint's nominal-target-band figure (2/20=10%) from D.1's
  realized-ADS-rebinned figure (0/18=0%) rather than conflating them — both independently verified
  against the raw CSV in §6 below. No contradiction.
- **C2b's "CONDITIONAL" vs. H1's "PARTIALLY_SUPPORTED":** re-confirmed as two different-axis verdicts
  (statistical-hypothesis-test axis vs. contribution-classification-taxonomy axis) describing the same
  underlying result, as the prior pass already established — still not in tension.
- **Evidence-chain integrity (§2, steps 1-9):** traced fresh, start to end — HYPOTHESIZED origin →
  OBSERVED Phase A discovery → HYPOTHESIZED general claim → OBSERVED literature challenge → INFERRED
  stress-test decision → HYPOTHESIZED pre-registered H1 → OBSERVED Experiment 1 result → OBSERVED+INFERRED
  D.1 explanation → INFERRED current synthesis. Every arrow still holds; no step's conclusion outruns
  its own evidence tag, and the wording edits did not alter any tag (all five edits are additions of
  scope language, not changes to the OBSERVED/INFERRED/HYPOTHESIZED labeling).

## 6. Evidence/claim traceability

Independently recomputed, from the raw 240-row `final_condition_results.csv`, four separate numeric
claims the document's edited and unedited passages both rely on:

| Claim | Document states | Independently recomputed | Match |
|---|---|---|---|
| VARIED winner constancy | `retrieval` in 120/120 | `Group-Object empirical_winner` on `lexical_variation=True` rows → `retrieval`=120, no other value | Exact |
| CLEAN winner constancy | `tie` in 120/120 | `Group-Object empirical_winner` on `lexical_variation=False` rows → `tie`=120, no other value | Exact |
| Realized ADS range | 0.44-0.93 | `realized_det_pct` min=0.44139, max=0.92576 | Exact (to stated precision) |
| 0.70-0.90 band agreement (§11.C) | 100% of definable comparisons | 32/32 definable (non-tie) rows in that realized-ADS band, all `r3_agrees_with_empirical=True` | Exact |
| ≥0.90 band agreement (§11.C) | 0% of definable comparisons | 18/18 definable rows in that band, all `r3_agrees_with_empirical=False` | Exact |
| r(ADS, rules accuracy), CLEAN/VARIED | 0.959 / 0.909 | own Pearson implementation: 0.9592 / 0.9091 | Exact |
| r(ADS, retrieval accuracy), CLEAN/VARIED | 0.955 / 0.948 | own Pearson implementation: 0.9549 / 0.9476 | Exact |

No untraceable number found. Every recomputed value matches the document to stated precision. This is
an independent re-derivation (own Pearson function, own PowerShell aggregation), not a re-trust of
either prior pass's arithmetic.

## 7. Code review

Not applicable — no code changed.

## 8. Experimental integrity

Not applicable in the "artifacts changed" sense — `data/outputs/experiments/exp1/final/` confirmed
untouched by `git status`. The raw CSV was read this pass only to re-verify claims made about it
(§6 above); nothing in the frozen evidence directory was written to.

## 9. Scope/GPS alignment

**PASS.** This is a wording-precision fix to a Gate-4 decision document already scoped correctly
everywhere else (§8 Scope, §9 Limitations, §10 Future Work all unchanged by the five edits and still
read as tightly bounded as the prior pass found them). Nothing in this round starts new
experimentation, reopens Experiment 1, or touches a DO NOT CHASE item. The DO NOT CHASE list itself
(re-read fresh this pass, `RESEARCH_GPS.md` lines 70-85) still reads current.

## 10. Git hygiene

- `git status --short`: exactly the three expected entries, nothing unexplained.
- Grepped `CONTRIBUTION_LOCK.md` and `contribution_lock.csv` for API keys, secrets, passwords, bearer
  tokens, private-key blocks, and local Windows user paths: no matches.
- No client/production data or real-company names introduced (production case study still cited by
  reference only, consistent with `METHODOLOGY.md`'s confidentiality boundary).
- No `.bak`/`.swp`/`.orig`/`.tmp` files present.
- `README.md`, `TECHNICAL_REPORT.md`, `METHODOLOGY.md`: absent from `git status`, confirmed untouched.
- `research/contribution_lock.csv`: confirmed untouched this round — file mtime (12:44) predates
  `CONTRIBUTION_LOCK.md`'s edit mtime (13:34) in the same session, consistent with "not touched by
  these edits" as the brief states; content read in full and contains only the pre-existing 11-row
  status table (no `orthogonal`/`governed`-scoping fixes applied to it, which is expected — the brief
  scoped all five edits to the `.md` file only, and the CSV was never in scope for F1-F4).
- A safe `git add` for a future checkpoint would be exactly:
  `git add research/CONTRIBUTION_LOCK.md research/contribution_lock.csv research/AUDIT_REPORT.md`.

## 11. Findings

**No REQUIRED NOW findings.** All five edits landed exactly as described, resolved F1-F4 completely
(re-verified independently, not assumed), and introduced no new numeric, verdict, or scope drift.

**G1 — OPTIONAL FUTURE WORK.** The "Auditor verdict" section embedded at the bottom of
`CONTRIBUTION_LOCK.md` (lines 404-418) still contains the text from the *first* Gate-4 audit pass
(pure numeric-accuracy verification, PASS) and was never updated to reflect the *second* pass's
CONDITIONAL verdict (the one that produced F1-F4) or this third, final pass. A reader who opens only
`CONTRIBUTION_LOCK.md` and reads its self-contained "Auditor verdict" section — which §12 explicitly
makes load-bearing ("Gate 4 is complete pending the auditor verdict below") — would see a verdict
narrative describing the first pass's checks (Pearson re-derivation, winner-constancy, band split) and
would not know a full CONDITIONAL round with four required wording fixes happened in between, even
though the fixes are correctly applied in the document body. Not a research-integrity issue (the body
content is accurate and current) and not something this pass is authorized to fix (editing
`CONTRIBUTION_LOCK.md` is out of scope for an auditor). Recommend the builder append or replace that
section with this pass's verdict before treating Gate 4 as closed in `RESEARCH_GPS.md`, so the
document's self-reported status matches its actual audit history.

**G2 — OPTIONAL FUTURE WORK.** `research/contribution_lock.csv` row 4 (C2b) still contains the word
"orthogonal" in its `Rationale` column ("ranking governed by orthogonal representation-stability
factor") — the same term F4 required removing from the `.md` file for the same reason (risk of being
read as a general statistical-independence claim rather than a within-this-factorial-design fact). The
CSV was explicitly out of scope for this round's five edits and remains untouched as instructed, so
this is not a regression from this pass — it is pre-existing content the wording-precision pass never
touched. Non-blocking (the CSV is a supporting data table, not manuscript-facing prose), but worth
noting for whichever future pass next touches the CSV, for consistency with the now-corrected `.md`.

## 12. Required fixes

None. (G1 and G2 above are optional, non-blocking notes for future housekeeping, not conditions on
this verdict.)

## 13. Verdict

🟢 **PASS.**

Justification: all five wording-only edits were independently located in the live document, read in
full grammatical/logical context (not just as isolated matched strings), and confirmed to say exactly
what the brief described. Direct re-grepping confirms all F1-F4 problems are resolved: every remaining
"governed" instance (4 of them, down from 5 — one was fully replaced rather than re-scoped) now
carries an inline, same-sentence scope qualifier; "orthogonal" has zero remaining occurrences in the
document; §11.C no longer contains an "entirely"+"governed" combination in any form, having been fully
replaced with numerically precise, already-scoped language. Independent re-derivation from the raw
240-row `final_condition_results.csv` (own PowerShell aggregation, own from-scratch Pearson
implementation) confirms seven separate numeric claims — winner constancy in both lexical conditions,
the realized-ADS range, both band-agreement percentages, and four correlation coefficients — all match
the document exactly, with no drift from either prior pass's verified numbers. No verdict word,
classification, or scope/limitation statement changed anywhere relative to what the prior CONDITIONAL
pass already verified as correct; `contribution_lock.csv` is confirmed untouched; no manuscript file,
frozen evidence file, or any file outside the three expected `git status` entries was modified; no
secrets, credentials, or client data present. Two non-blocking notes (G1: the document's
self-embedded "Auditor verdict" section is stale relative to the actual three-pass audit history; G2:
the CSV still contains the pre-existing, out-of-scope "orthogonal" term F4 addressed only in the `.md`)
are recorded for future housekeeping but do not condition this verdict. **Gate 4's wording is now
locked correctly. This document is checkpoint-ready as audited**, contingent only on the builder
updating the embedded verdict text (G1) and `RESEARCH_GPS.md`'s Gate 4 checkbox — both outside this
auditor's authority to change.
