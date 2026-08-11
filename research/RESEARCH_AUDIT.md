# RESEARCH AUDIT — ADS-Cascade / TECHNICAL_REPORT.md

> Phase A deliverable per `ROADMAP.md`. **Audit only.** This document, `claim_evidence_matrix.csv`,
> and `artifact_inventory.csv` were produced in the initial pass (below) without executing any code
> or modifying any source file. A follow-up pass (see "Resolution status," directly below) resolved
> findings A1-A4: it made two narrowly-scoped documentation edits (`STATE.md`, `ROADMAP.md`, both
> fixing only the false tracking-status claim / updating checklist status — no technical content
> changed) and executed `scripts/03_5_dataset_intelligence.py` and `scripts/04_architecture_decision.py`
> read-only for verification (outputs were byte-identical to committed versions except a run
> timestamp, which was reverted; see `research/determinism_provenance.md`). No manuscript prose was
> rewritten, no novelty claims were made, and no literature review was performed, per that pass's
> instructions. A third pass fixed the A5 bug this audit surfaced (see `research/a5_correction_analysis.md`).
> A fourth, final pass — the **Final Phase-A Evidence Closure Audit** (2026-08-11) — independently
> re-checked every quantitative claim in `TECHNICAL_REPORT.md` against the current canonical
> artifacts (not just the existing `claim_evidence_matrix.csv`), producing
> `research/final_numbers_audit.csv` (47 claims), `research/MANUSCRIPT_UPDATE_QUEUE.md`, and
> `research/PHASE_A_CLOSURE.md`. It surfaced one new finding (A6, §2.4's T2 cascade description is
> stale relative to shipped code) and two previously-unflagged unsupported claims (§4, §6 — see
> Section B). No manuscript prose was rewritten in this pass either.

## Resolution status (updated 2026-08-11 — Final Phase-A Evidence Closure Audit)

| Finding | Status | Detail |
|---|---|---|
| A1 — architecture docs "untracked" | **RESOLVED** | Confirmed false; `STATE.md` and `ROADMAP.md` corrected. |
| A2 — 76,843 vs ~55,394 | **PARTIALLY RESOLVED** | 76,843 confirmed canonical. ~55,394 is **UNRESOLVED** (exhaustive search found no trace anywhere in this repo) — see `research/mapping_count_provenance.md`. This is the only item this repository cannot close by further audit; it needs the author to check outside sources. |
| A3 — 0.7756/0.9746 vs 0.763/0.931 | **RESOLVED** | Both pairs are live, current, non-stale outputs of different (legitimate) aggregation formulas — see `research/determinism_provenance.md`. That investigation also surfaced finding A5. |
| A4 — R3 threshold structure | **RESOLVED** | Full three-band structure documented, no bug in the decision logic itself — see `research/r3_threshold_analysis.md`. |
| A5 — dominant-account selection bug in `product_ambiguity.csv` | **RESOLVED — fixed 2026-08-11** | Regression-tested and corrected; see `research/a5_correction_analysis.md`. (This table row was previously stale — see the A5 entry below, which was already marked resolved in prose but not reflected here until this closure pass.) |
| A6 (new) — `TECHNICAL_REPORT.md` §2.4's T2 cascade description is stale relative to the shipped code | **OPEN — pending author decision** | Discovered during the Final Phase-A Evidence Closure Audit, independent of A1-A5. See below and `research/MANUSCRIPT_UPDATE_QUEUE.md` item I2. |

Canonical values are consolidated in `research/EVIDENCE_BASELINE.md`. The full closure-pass
cross-check of every quantitative claim in `TECHNICAL_REPORT.md` is in
`research/final_numbers_audit.csv`, with the manuscript-facing punch list in
`research/MANUSCRIPT_UPDATE_QUEUE.md` and the closure summary in `research/PHASE_A_CLOSURE.md`.

---

**Date:** 2026-08-10 (initial pass); resolution follow-up same day
**Scope:** Every quantitative or methodological claim in `TECHNICAL_REPORT.md`, cross-checked
against `STATE.md`, `ROADMAP.md`, `README.md`, `METHODOLOGY.md`, `data_verification_audit.md`,
`architecture/00_SCOPE.md`, `architecture/DECISIONS.md`, `architecture/08_CONFIDENCE_CASCADE.md`,
the generating scripts, and the currently-committed CSV/JSON/MD artifacts under `data/outputs/`
and `reports/`.

**Method note:** This audit reads and cross-references committed files and reads threshold
constants directly out of the scripts. It does **not** re-execute the pipeline end-to-end (that
is out of scope for an audit and belongs to Phase A/H's reproducibility re-run, or to Phase D).
Where a figure could be checked by hand against a small committed CSV (row counts, weighted
averages), it was; this is noted per-row in `claim_evidence_matrix.csv`'s Confidence column.

---

## How to read the two CSVs

- **`claim_evidence_matrix.csv`** — one row per claim (or tightly-related cluster of restatements
  of the same number across sections). Columns: `ID, Claim, Paper Section, Claim Type, Source
  Artifact, Generating Script, Supporting File Path, Reproducible In This Repo?, Confidence, Notes
  / Contradictions`.
- **`artifact_inventory.csv`** — one row per file this audit touched or needed to reason about
  (scripts, data outputs, reports, docs). Columns: `Path, Type, Tracked in Git?, Produced By /
  Role, Consumed By, Confidentiality, Notes`.

---

## A. Critical inconsistencies

**A1 — STATE.md's "17 untracked architecture docs" claim is stale and false.**
`STATE.md` (Done section) says Phase 2 architecture is "17 docs... **Written but untracked in
git**," and `ROADMAP.md`'s Phase A explicitly tasks the author with "decide the fate of the 17
untracked `architecture/` docs." Checked directly: `git ls-files architecture/` lists all 17 files
(`00_SCOPE.md` through `14_COST_MODEL.md`, plus `DECISIONS.md` and `OPEN_QUESTIONS.md`), and
`git log --oneline -- architecture/` shows they were added in the very first commit
(`81fb74e`, 2026-07-28) and have been tracked ever since. `git status --porcelain` confirms no
pending changes to `architecture/`. **There is nothing to resolve here except updating the stale
status text** — no privacy review is needed, because these files have been public since the
repository's initial commit and the same commit already anonymized worked examples per
`METHODOLOGY.md` item 4.

> **RESOLVED (2026-08-10).** `STATE.md`'s Done section and `ROADMAP.md`'s Phase A checklist have
> both been corrected to state the true tracking status. No technical content was changed in
> either file — only the false "untracked" claim and its dependent checklist item.

**A2 — The "76,843-vs-~55,394" mapping-count discrepancy has no traceable source in this
repository.**
`76,843` is well-attested: it appears identically in `reports/phase1_final_report.md` §6 ("The
product account mapping table contains 76,843 unique (company, product, account) tuples"),
`TECHNICAL_REPORT.md` §2.1, `README.md`'s results table, and ADR-003/ADR-004 in
`architecture/DECISIONS.md`. By contrast, `~55,394` appears **nowhere** in this repository's
current file tree, and a full-history search (`git log --all -p` across all 8 commits on the only
branch, `main`) finds it in zero commits, ever. The only two places `~55,394` exists at all are
`ROADMAP.md` and `STATE.md`'s own sentences *describing* the alleged discrepancy — i.e., the
number that's supposedly in tension with 76,843 cannot itself be found anywhere to check. This
audit cannot resolve it: either the figure lives only in the private/confidential client repository
(out of reach here), or it was a misremembered/approximate figure from the `/grill-me` session that
produced `ROADMAP.md`, and never existed as a written artifact. **This should not block Phase A
indefinitely** — see Question F1.

> **PARTIALLY RESOLVED (2026-08-10).** A complete provenance search was performed per
> `research/mapping_count_provenance.md`: current tree, full git history (`git log --all -p`),
> deleted files, commit messages, tags/branches, and dangling/unreachable git objects (a pre-amend
> commit was found and inspected — it contains no mapping-count content, only an old draft of the
> demo HTML). **~55,394 remains formally UNRESOLVED** — it cannot be found anywhere in this
> repository. **76,843 is confirmed canonical** (its provenance was already explicitly verified
> above, independent of what 55,394 turns out to be). `STATE.md` and `ROADMAP.md` have been updated
> to stop presenting this as an open, resolvable-from-this-repo question.

**A3 — A same-name-different-value pattern for "cross-company consistency/determinism" reproduces
live in the currently-committed synthetic branch, mirroring an already-known production issue.**
`data_verification_audit.md` itself flags, for the *production* data, that
`dataset_intelligence_report.md` reportedly said "Global Cross-Company Determinism: 0.7454" while
`phase1_final_report.md` says "0.695" — and declares the latter authoritative "per user directive,"
without recording *why* the two computations differ. That production `dataset_intelligence_report.md`
is not in this public repo, so the discrepancy can't be independently re-examined.

But the exact same pattern exists right now, today, in this repo's own synthetic artifacts —
not as a historical footnote, but as a live, reproducible inconsistency:
- `data/outputs/intelligence/dataset_intelligence_report.md` states **"Global Cross-Company
  Determinism: 0.7756"** and **"Average Company Determinism: 0.9746."**
- `data/outputs/intelligence/decision_matrix.csv` and `reports/architecture_decision.md` (both
  generated by the same pipeline, same run) state **cross-company consistency = 0.7632**.
- `TECHNICAL_REPORT.md` §3.2 and `METHODOLOGY.md` cite **0.763** (i.e., the 0.7632 figure, not
  0.7756) — so the paper's own citation is internally consistent with the decision-matrix number,
  but a different, differently-labeled number sits uncorrected in a third committed file one
  directory away, with no note explaining the difference (unlike `data_verification_audit.md`,
  which at least flags its own production-side version of this problem).
- Similarly, "Average Company Determinism: 0.9746" does not match "unweighted ADS 0.931," the
  number the paper actually cites for the synthetic run — a third distinctly-computed aggregate
  under a name generic enough to be confused with a cited metric, even though the paper itself
  never cites 0.9746.

**None of this makes any claim in `TECHNICAL_REPORT.md` wrong** — the paper cites the number that
matches the decision matrix, not the outlier. But it means the underlying intelligence-reporting
script (`03_5_dataset_intelligence.py`) currently emits at least three differently-aggregated
"determinism"-family numbers under similar names in the same run, without documenting which is
which anywhere except by inference. A reader who opens `dataset_intelligence_report.md` instead of
`decision_matrix.csv` would see a different number and have no way to know it's not the one the
paper cites.

> **RESOLVED (2026-08-10).** `research/determinism_provenance.md` traces both pairs to exact code
> (Path 1: `dataset_intelligence_report.md`'s `generate_report()`, occurrence-weighted /
> company-vote aggregates; Path 2: `decision_matrix.csv`'s `compute_cross_company_score()` /
> `compute_dataset_ads()`, simple-mean aggregates) and confirms, by executing both scripts, that
> **neither report is stale** — both are live, current, byte-for-byte reproducible outputs of the
> present code. The discrepancy is a genuine, legitimate difference in aggregation method (weighted
> vs. unweighted, exactly parallel to the ADS weighted/unweighted split the paper already discusses
> for the production numbers), not a bug and not staleness. **Canonical for the manuscript:** 0.7632
> (≈0.763) and 0.9310 (≈0.931) — these are what the reproduction chain named in
> `TECHNICAL_REPORT.md`/`METHODOLOGY.md` actually produces and cites; `dataset_intelligence_report.md`
> is not part of that chain. See `EVIDENCE_BASELINE.md`.
>
> **This investigation also found something more consequential than the original A3 question** — a
> real computational bug in the code that produces the *canonical* numbers themselves, not just the
> non-canonical ones. See new finding **A5** below.

**A4 — TECHNICAL_REPORT.md §2.3 describes R3 as a single-threshold decision; the live script
encodes three bands.**
The paper's decision-matrix table (§2.3) gives R3 a single cutoff: "≥90% → rules-first." Reading
`scripts/04_architecture_decision.py` directly (lines 43-56) shows the actual logic is three-way:
`THRESHOLD_DETERMINISTIC_RULES = 0.90` (→ RULES_FIRST), `THRESHOLD_DETERMINISTIC_EMBED = 0.70`
(→ EMBEDDING_PRIMARY between 70-90%), and an unnamed third branch below 70% (presumably an
LLM-first or similar fallback, never triggered by either the production or synthetic runs so never
described in the paper). The synthetic run's headline finding — R3 flipping to EMBEDDING_PRIMARY at
84.1% — depends on this middle band, but §2.3 never states the middle band exists; a reader has to
infer it from the results table in §3.2. This isn't wrong, but §3.3's entire "boundary case"
argument rests on a threshold structure the paper only half-discloses.

> **RESOLVED (2026-08-10).** `research/r3_threshold_analysis.md` documents the full three-band
> structure (RULES_FIRST ≥90%, EMBEDDING_PRIMARY 70-90%, LLM_REQUIRED <70%, the last never
> triggered in this repo), confirms the decision logic itself has **no bug** (bands meet cleanly at
> their boundaries, thresholds are the documented named constants), and confirms the synthetic R3
> flip is a genuine consequence of `det_pct` landing on the Band-2 side of the 90% cutoff — not an
> artifact of anything else, including the A5 bug below (corrected `det_pct` ≈87.56%, still inside
> Band 2). Recommendation: state the full band structure in §2.3 (Recommendation E4, not applied —
> manuscript edits are out of scope for this pass).

**A5 (new finding, surfaced while investigating A3) — `product_ambiguity.csv`'s dominant-account
selection doesn't merge same-account rows before comparing, and understates ADS for multi-company
products.**
`scripts/03_5_dataset_intelligence.py`'s Module C.1 (the block that produces `product_ambiguity.csv`,
which is the direct input to `TECHNICAL_REPORT.md`'s weighted/unweighted ADS figures and R3's
91.2%/84.1% "deterministic products" figures) selects each product's "dominant account" by taking
the single largest **row** in the per-(company, product, account) mapping data, rather than summing
counts **by account** first as its sibling computation (`cross_company_consistency.csv`'s Module
C.3) correctly does. Concrete, verified example — product `synth office 00073` is booked to 4
distinct accounts by 5 companies (608:12, 625:21, 605:25, 371:10, 371:18); the true dominant account
is 371 (28/86 = 32.6%, correctly computed by C.3), but `product_ambiguity.csv` reports dominant
account 605 (25/86 = 29.1%) because it never noticed 371's two rows sum to more than 605's one row.
Worse cases exist: three synthetic products where *every single company agrees on the same account*
(true determinism = 1.0) are reported by the current code as 25-33% deterministic, because the
per-company rows for that one account were never merged. Quantified across the whole synthetic
dataset (844 products): 74 products (8.8%) are affected; **unweighted ADS 0.9310 → ~0.9597**,
**weighted ADS 0.8094 → ~0.9031** if corrected. This bug does **not** change any of the five
architecture decisions (R1/R3/R4/R5 all confirmed robust to the correction on synthetic data — see
`research/determinism_provenance.md` Step 4), but it does materially affect the *magnitude* the
paper reports and interprets — particularly §2.2's "ADS divergence... a gap of 0.117" narrative,
whose synthetic-branch analogue would roughly halve under correction (0.1216 → 0.0566). Full
evidence, exact code citations, and the standalone verification methodology are in
`research/determinism_provenance.md` Step 3.

> **RESOLVED 2026-08-11.** The bug has been fixed (regression test written first, watched to fail,
> then the aggregation logic corrected — full record in `research/a5_correction_analysis.md`). The
> pipeline was re-run on the same synthetic input; the `~0.9597`/`~0.9031`/`~87.56%` estimates above
> are now the confirmed, actual output, not estimates. All five architecture decisions confirmed
> unchanged by direct re-run (not just estimated). See `research/EVIDENCE_BASELINE.md` §2 for the
> new canonical values and §3/Note 1 for what is now `SUPERSEDED — DO NOT CITE`. Question F6 below
> is resolved. `TECHNICAL_REPORT.md` §3.2/§3.3 still cite the pre-fix synthetic numbers and need
> updating in the manuscript-rewrite phase — not done here, per this pass's scope.

**A6 (new finding, Final Phase-A Evidence Closure Audit, 2026-08-11) — `TECHNICAL_REPORT.md` §2.4's
T2 tier description no longer matches the shipped cascade code.**
An independent, line-by-line pass over every quantitative claim in `TECHNICAL_REPORT.md` (not
relying solely on the existing `claim_evidence_matrix.csv`) found that §2.4's T2 row — "Fuzzy/
embedding match (similarity ≥ 0.85) or a weaker company rule (0.80–0.95 ADS) corroborated by VAT |
Auto-apply, flagged for a sampled spot-check" — describes an **earlier version** of the cascade
design, not the code as currently shipped. In `scripts/phase2/p2lib/confidence.py`, `T2_ADS_LOW =
0.90` (not 0.80), and `FUZZY_AUTO_APPLY = False` is a hardcoded constant that makes the entire
fuzzy-similarity auto-apply branch in `cascade.py` dead code — every fuzzy match, at any similarity
score, now falls through to Tier 3 (`FUZZY_REVIEW`), never Tier 2. Code comments explain this was a
deliberate post-launch tightening: a Stage-A held-out eval measured the original 0.80-ADS-floor
rules at ~45% accuracy and fuzzy auto-apply at ~49% — both judged unsafe. `STATE.md`'s own Phase 2
notes already record this recalibration ("fuzzy is demoted to review (never auto-applied)"), and
`architecture/08_CONFIDENCE_CASCADE.md` §3 independently confirms it describes the same *original*
0.80/fuzzy-auto-apply design as the manuscript — so this is not a manuscript-vs-architecture-doc
disagreement, it is a manuscript-and-architecture-doc-vs-shipped-code disagreement. Both documents
are stale in the same direction, for the same reason. This also means §2.4's T3 row ("Similarity <
0.85 ... routed to human review") is imprecise as currently implemented: *all* fuzzy matches land
at T3 regardless of score, not just those below 0.85. Full evidence:
`research/final_numbers_audit.csv` rows F19/F20; recommended manuscript fix:
`research/MANUSCRIPT_UPDATE_QUEUE.md` item I2. This also means the original claim_evidence_matrix.csv
row C18 ("Exact match between the architecture doc's written spec and the running code's named
constants") was itself incomplete — that earlier check verified T1's constants and T2_SIM/T3_FLOOR,
but not `T2_ADS_LOW`, `T2_MIN_EVIDENCE`, `T2_GLOBAL_ADS_LOW`, or `FUZZY_AUTO_APPLY`, and did not
cross-reference `cascade.py`'s actual tier-assignment logic against the prose. **Not a code bug —
the code is internally consistent and intentionally safety-tightened.** Not fixed here, per this
task's "do not modify methodology or code" constraint — this is a documentation-lag finding,
requiring an author decision on whether to update the manuscript+architecture-doc to match the
safer shipped behavior, or reconsider re-enabling `FUZZY_AUTO_APPLY` if warranted. See Question F7
below.

---

## B. Unsupported claims

**None found in `TECHNICAL_REPORT.md` itself.** Every quantitative claim in the report traces to
either (a) `reports/phase1_final_report.md` / `data_verification_audit.md` for production numbers,
or (b) a currently-committed, independently-recomputable CSV/JSON for synthetic numbers (see
Section D). The report is also self-aware about its own qualitative/not-yet-measured claims — e.g.,
§4 explicitly labels domain-transfer and semantic-retrieval-gap claims as expectations argued from
design, not measured results, rather than asserting them as findings. That honesty means they don't
count as "unsupported" in the sense of overclaiming; they're correctly hedged.

The one item that comes closest to "unsupported" is the **`~55,394` figure** discussed in A2 —
but it is not actually a claim *in* `TECHNICAL_REPORT.md`; it exists only in the planning documents
(`STATE.md`, `ROADMAP.md`) as a description of an open question. It is flagged here so it doesn't
silently get carried into the manuscript before its source is confirmed one way or the other.

> **UPDATED 2026-08-11 — Final Phase-A Evidence Closure Audit found two genuine unsupported claims
> *in* `TECHNICAL_REPORT.md` itself**, missed by the original pass above. The "none found" verdict
> above is now superseded for these two specific sentences (the rest of the original finding still
> stands):
>
> - **§4:** "Cross-company consistency has a real, measured ceiling (0.695 in production; **0.76–0.80
>   across synthetic seeds**)." No multi-seed sweep exists anywhere in this repository — only a
>   single `seed=42` run has ever been executed, producing 0.7632 (a point, not a range). This
>   directly contradicts §4's own later bullet that the synthetic run is single-seed and "was not
>   swept." An internal self-contradiction, not just an unverifiable aside.
> - **§6:** "the LLM's job shrinks to re-ranking retrieved candidates for a measured minority tail
>   (**under 10% of production volume**)." No artifact in this repository states an LLM-share-of-
>   *volume* (occurrence-weighted) figure; the closest real number, 8.8% non-deterministic products,
>   is a product-*count* statistic, and §2.2 itself argues weighted and unweighted figures diverge
>   substantially in this dataset — so presenting an unweighted-derived number as a "volume" share is
>   the exact conflation §2.2 warns against.
>
> Full evidence: `research/final_numbers_audit.csv` rows F42/F45. Recommended manuscript fix:
> `research/MANUSCRIPT_UPDATE_QUEUE.md` items I5/I6. Neither has been edited in the manuscript — see
> Question F8 below.

---

## C. Production-only claims (confidential, cited not reproduced)

All of §3.1, and the Phase 1 statistics that feed it:

- 296,648 invoice lines / 169 companies (201 inventoried) / 1,020 XML filings (C01, C08)
- 91.2% deterministic / 1.1% ambiguous products (C02)
- Cross-company consistency 0.695 over 2,696 multi-company products (C03)
- 47,306 normalized unique products / 76,843 (company, product) → account mappings (C09, C10)
- Weighted/unweighted ADS 0.847 / 0.964 (C13)
- GL extraction: 154,068 records, 201 companies (C12)
- Tier-1 98.4% @ 42% coverage; full cascade 98.1% @ 42.8% coverage; 66.7% raw held-out accuracy
  on 63,048 test lines, 80/20 split (C04, C05, C06)
- 10-real-receipt end-to-end trace: 0 auto / 8 T3 / 14 T4 before the retrieval bridge; 14→T3 with
  candidate, 2 novel after (C07)
- LLM re-ranking behavior change on the same 10-receipt trace (C19)

For every one of these, the **generating script is public and unmodified** and runs identically on
the synthetic branch — only the confidential input data (and, for C19, live API calls against a
production KB) makes the specific number non-reproducible here. This is exactly the tradeoff
`METHODOLOGY.md` and `TECHNICAL_REPORT.md`'s own Reproducibility section already state; this audit
found no case where a "production-only" label was being used to hide something that should
actually be public.

---

## D. Publicly reproducible claims

All of §3.2's synthetic table, independently checked against currently-committed artifacts during
this audit (not merely trusted from the prose):

| Claim | Checked against | Result |
|---|---|---|
| 60 companies / 7,523 invoice lines | `invoice_lines_all_companies.csv` row count | Matches (7,524 lines incl. header) |
| Weighted/unweighted ADS 0.809 / 0.931 | `reports/architecture_decision.md` header (0.8094 / 0.9310) | Matched *at the time of the original pass*. **SUPERSEDED 2026-08-11** — A5 fix changed these to 0.9031/0.9597; see `research/EVIDENCE_BASELINE.md` §2. |
| 84.1% deterministic | `decision_matrix.csv` R3 row (`deterministic_pct` 0.8412) | Matched *at the time*. **SUPERSEDED 2026-08-11** — now 87.56%; decision (EMBEDDING_PRIMARY) unchanged. |
| Cross-company consistency 0.763 | `decision_matrix.csv` R1 row (0.7632) | Matches (see A3 for the *other*, uncited 0.7756 figure sitting nearby) |
| VAT missing 4.45% | `data_quality_report.csv` | Matches |
| R1 HYBRID / R4 SECONDARY_FEATURE / R5 DROP | `decision_matrix.csv` | Matches |
| R3 flips to EMBEDDING_PRIMARY | `decision_matrix.csv` (0.8412 < 0.90 threshold) | Matches, and is a real property of the live threshold logic (A4), not a cherry-pick |
| Cascade auto-apply 99.8% @ 76.2% coverage | Hand-recomputed from `tier_distribution.csv`: (1223+9)/1616 = 76.24% coverage, weighted accuracy ≈99.76% | Matches within rounding |
| 844 vs 47,306 unique products (catalog-size explanation) | `kb_summary.json` (`global_products: 844`) | Matches |

Also reproducible as **methodology** (code/spec, not a specific number): the four-tier cascade
trigger definitions (§2.4) match `p2lib/confidence.py`'s named constants exactly (T1_ADS=0.95,
T1_MIN_EVIDENCE=3, T1_GLOBAL_ADS=0.98, GLOBAL_MIN_COMPANIES=5, T2_SIM=0.85, T3_FLOOR=0.50); the
retrieval placeholder (§2.5) matches `p2lib/retrieval.py`'s rapidfuzz implementation and its
in-code `# ponytail:` gap marker; the Textract caching claim matches the 5 committed synthetic
fixture files under `data/outputs/phase2/textract_raw/`.

> **CORRECTION 2026-08-11 — the "match... exactly" claim above is incomplete.** The Final Phase-A
> Evidence Closure Audit found that this list checked only T1_ADS, T1_MIN_EVIDENCE, T1_GLOBAL_ADS,
> GLOBAL_MIN_COMPANIES, T2_SIM, and T3_FLOOR — it did not check `T2_ADS_LOW`, `T2_MIN_EVIDENCE`,
> `T2_GLOBAL_ADS_LOW`, or `FUZZY_AUTO_APPLY`, and did not cross-reference `cascade.py`'s actual
> tier-assignment logic against the manuscript's T2/T3 prose. Doing so this pass found §2.4's T2 row
> is stale (code uses `T2_ADS_LOW=0.90` not 0.80, and `FUZZY_AUTO_APPLY=False` makes fuzzy matches
> never reach T2 regardless of similarity) — see finding A6 above. The T1 constants listed here
> remain independently re-verified and correct.

---

## E. Recommended corrections

Ordered roughly by effort-to-fix, not severity.

1. ~~Fix the stale "17 untracked architecture docs" line in `STATE.md`~~ — **DONE (2026-08-10).**
   `STATE.md` and `ROADMAP.md` both corrected (A1).
2. **Either trace `~55,394` to a real source or drop the discrepancy framing** from `ROADMAP.md`'s
   Phase A task list — **partially done:** `ROADMAP.md`'s checklist item now states plainly that
   the figure is unresolved and untraceable from this repository, rather than presenting it as an
   open, resolvable-here question. Still pending: the author checking the private repo/session notes
   (A2, Question F1) — this audit cannot do that part.
3. **Reconcile or annotate `data/outputs/intelligence/dataset_intelligence_report.md`'s 0.7756 /
   0.9746 figures** against the 0.7632 / 0.931 figures used in the paper — confirmed **not stale**
   (A3); still recommend a one-line annotation explaining the differing aggregation, mirroring
   `data_verification_audit.md`'s existing NOTE for the production case. **Not applied** — this is a
   data-file edit, out of scope for an audit/provenance pass.
4. **State the full R3 threshold structure in `TECHNICAL_REPORT.md` §2.3**, not just the ≥90%
   cutoff — name the 70-90% EMBEDDING_PRIMARY band explicitly, since §3.3 leans on it (A4). **Not
   applied** — manuscript edit, out of scope for this pass.
5. **Link `data_verification_audit.md` from `README.md`'s folder map and/or `docs/INDEX.md`** — it
   is the single most-cited numbers source in the repo (`STATE.md` and `METHODOLOGY.md` both point
   to it) but has no entry in either navigation document. **Not applied.**
6. **§2.1's pipeline stage table header says "Script" but lists descriptive stage names**
   ("Inventory," "GL extraction") rather than actual filenames — either rename the column or add
   filenames, so a reader auditing a claim can find the generating script without cross-referencing
   `README.md`'s folder map first. **Not applied.**
7. **Document the ~5% gap between `product_account_mapping.csv`'s 1,234 synthetic rows and
   `kb_summary.json`'s 1,172 `company_product_rules`** — likely an expected KB-build filter
   (minimum evidence count, or direction consolidation), but nothing currently states what it
   filters or why, for either the production or synthetic run. **Not applied; not investigated
   further in this pass** (out of scope — A1-A4/A5 only).
8. **RESOLVED 2026-08-11 — the A5 dominant-account-selection bug in `03_5_dataset_intelligence.py`**
   (`product_ambiguity.csv`'s Module C.1) has been fixed, regression-tested, and the pipeline
   re-run. See Question F6 and `research/a5_correction_analysis.md`. Remaining sub-item: update
   `TECHNICAL_REPORT.md` §3.2/§3.3's cited synthetic figures in the manuscript-rewrite phase.
9. **NEW (2026-08-11) — rewrite `TECHNICAL_REPORT.md` §2.4's T2/T3 tier descriptions** to match the
   shipped cascade code (A6): state the actual `T2_ADS_LOW=0.90` floor, and that fuzzy/embedding
   matches currently always route to Tier 3 review (`FUZZY_AUTO_APPLY=False`), not Tier 2 auto-apply
   as currently written. Also update `architecture/08_CONFIDENCE_CASCADE.md` §3, which describes the
   same stale design. **Not applied** — manuscript/architecture-doc edit, out of scope for an audit
   pass; see Question F7.
10. **NEW (2026-08-11) — remove or substantiate two unsupported claims**: §4's "0.76–0.80 across
    synthetic seeds" (no multi-seed sweep exists in this repo) and §6's "under 10% of production
    volume" (no volume-weighted LLM-share artifact exists in this repo). See
    `research/MANUSCRIPT_UPDATE_QUEUE.md` items I5/I6 and Question F8. **Not applied** — manuscript
    edit, out of scope for an audit pass.

---

## F. Questions requiring the human author's decision

**F1. OPEN.** Where did `~55,394` come from? A second, exhaustive search (current tree, full git
history including deleted files and dangling objects, commit messages, tags/branches — see
`research/mapping_count_provenance.md`) still found nothing. It is not in this repository. Possible
sources this audit cannot check: the private/confidential client repository, or an earlier chat
session's `/grill-me` transcript (in which case it may never have existed as a written artifact at
all, only as a recollection). Please check the private repo or your own notes; if it can't be
found, treat it as permanently unresolved rather than a blocking discrepancy — 76,843 stands as
canonical regardless (its own provenance is independently and fully verified).

**F2. STILL OPEN, but now better understood.** `data_verification_audit.md` designates
`phase1_final_report.md`'s 0.695 authoritative over `dataset_intelligence_report.md`'s 0.7454
(production) "per user directive," with no recorded methodological reason. The synthetic-branch
investigation (`research/determinism_provenance.md`) now shows *what kind* of difference this
almost certainly is (occurrence-weighted vs. simple-mean aggregation — the same pattern confirmed
on the synthetic pair, 0.7632 vs 0.7756), but this cannot be verified against the actual production
`dataset_intelligence_report.md`, which isn't in this repository. Do you want a one-line
explanation written into `data_verification_audit.md` now (stating the *likely* mechanism, clearly
labeled as inferred-by-analogy rather than confirmed on the production file), or is "one file is
designated authoritative" sufficient for the manuscript's purposes?

**F3. Still open** — a process question, unaffected by this pass. Should the Claim-Evidence Matrix
be treated as satisfying `ROADMAP.md`'s Phase A checklist item, or do you want a stricter version
keyed to exact line numbers / exact sentences in `TECHNICAL_REPORT.md`?

**F4. RESOLVED.** The follow-up pass executed `03_5_dataset_intelligence.py` and
`04_architecture_decision.py` directly (not the full six-script chain — `00_generate_synthetic.py`,
`p2_01`, `p2_02`, and `p2_05` were not re-run in this pass, since the question was specifically
about `03_5`/`04`'s determinism outputs, not the whole pipeline). Result: both scripts reproduce
their committed outputs byte-for-byte (only a run timestamp differed, reverted afterward) —
confirmed deterministic and current, not stale. A full six-script end-to-end re-run (to raise C29's
confidence from "Medium" to "High" and to satisfy Phase H's reproducibility audit) is still
outstanding and would be a reasonable next step, but was not necessary to answer the specific A3
question.

**F5. RESOLVED.** `research/r3_threshold_analysis.md` documents the never-triggered third R3 band
(`LLM_REQUIRED`, `det_pct < 0.70`) and recommends the paper name the 70-90% EMBEDDING_PRIMARY band
explicitly (since it's empirically reached) while leaving documentation of the never-triggered band
as an author's call — this remains a manuscript-wording decision, not a code question.

**F6. RESOLVED 2026-08-11 — fixed.** The author's decision was to fix rather than document-as-limitation.
`research/determinism_provenance.md` Step 3's bug in `product_ambiguity.csv`'s dominant-account
selection (Module C.1 of `scripts/03_5_dataset_intelligence.py`) has been corrected: counts are now
summed by `account_id` across all rows for a product before selecting the dominant account
(mirroring C.3's existing correct logic), guarded by a permanent regression test
(`scripts/test_dataset_intelligence.py`, TDD red→green). The synthetic pipeline was re-run;
confirmed actual (not estimated) impact: unweighted ADS 0.9310→**0.9597**, weighted ADS
0.8094→**0.9031**, deterministic-product share 84.12%→**87.56%**. None of the five architecture
decisions changed (confirmed by direct re-run, not just estimated). Full record:
`research/a5_correction_analysis.md`; updated canonical values: `research/EVIDENCE_BASELINE.md` §2.

**Remaining open sub-item:** `TECHNICAL_REPORT.md` §3.2/§3.3 still cite the pre-fix synthetic
numbers (0.809/0.931, 84.1%) — updating those is a manuscript edit, out of this pass's scope, and
is now a punch-list item for the manuscript-rewrite phase (Phase E), not an open research question.
Also still unresolved: whether the *production* numbers (91.2%/0.847/0.964) carry the same
understatement — this repository has no production data to re-run the corrected code against, so
that remains an explicit author to-do (re-run `03_5_dataset_intelligence.py`'s corrected version
against production data before citing production ADS figures as final).

**F7. NEW, OPEN (2026-08-11) — what should happen to the T2 cascade tier (finding A6)?** The
shipped code (`FUZZY_AUTO_APPLY=False`, `T2_ADS_LOW=0.90`) is stricter/safer than the design both
`TECHNICAL_REPORT.md` §2.4 and `architecture/08_CONFIDENCE_CASCADE.md` §3 describe (fuzzy matches
auto-applying at similarity ≥0.85, and a 0.80 ADS floor). Two options, and this audit does not
recommend one over the other: (a) update the manuscript and architecture doc to describe the
current, safer, shipped behavior (fuzzy always routes to review) — the more conservative choice,
since it just documents what already ships; or (b) treat the current code as *itself* not yet
final, and revisit whether `FUZZY_AUTO_APPLY` should be re-enabled now that more evidence exists
(this would be a methodology/code change, out of scope for any audit pass). Recommend (a) as the
lower-risk default for the upcoming manuscript rewrite, but this is the author's call.

**F8. NEW, OPEN (2026-08-11) — how to handle the two unsupported §4/§6 claims?** "0.76–0.80 across
synthetic seeds" (§4) and "under 10% of production volume" (§6) have no supporting artifact in this
repository (see updated Section B above, and `research/MANUSCRIPT_UPDATE_QUEUE.md` items I5/I6).
For the seed-range claim: either actually run a small multi-seed sweep (this would also serve
Phase D's minimal-validation goal) and report the true range, or replace it with the single
reproducible value (0.763) and drop the range framing. For the volume claim: either compute a true
occurrence-weighted LLM-touch-rate from production data (author-only, confidential), or soften the
wording to "under 10% of the product catalog" (product-count framing, which the data does support).
Neither requires new methodology — just a decision on which honest, supportable sentence to publish.
