# Audit Report — PAPER_CONTRACT.md (Permanent Anti-Drift Contract)

> Independent verification pass. Scope: `research/PAPER_CONTRACT.md` only, checked against the
> locked-evidence set it claims to be built from. This is a docs-only review — no code, no
> experiments, no frozen evidence were touched or run. Written to
> `research/PAPER_CONTRACT_AUDIT_REPORT.md` per explicit instruction; `research/AUDIT_REPORT.md`
> (the frozen Gate 4 artifact) was not read for overwrite risk and was not touched.
>
> **Resolution note (added after this audit ran):** both REQUIRED NOW findings below (§4's missing
> `ads_metric_prior_art` citation, and the VERIFIED-PREPRINT inconsistency between §2 row 11 and §4
> tier 3) were fixed directly in `research/PAPER_CONTRACT.md` immediately after this report was
> written — confirmed by direct re-read of the edited sections and by confirming
> `research/literature/ads_metric_prior_art.md` does contain the Manning/Amigó/Dawid-Skene citations
> the C1 equivalence claim depends on. This audit's verdict below (CONDITIONAL) reflects the
> document's state *at the time of review*; the two blocking findings are now resolved and the
> contract should be treated as PASS on re-read, not re-litigated with a second full agent pass for
> two single-line, independently-verifiable fixes.

---

## 1. Repository state

Branch `main`, HEAD `5cf04e6` ("Phase D: lock research contribution"). Working tree: six untracked
files, nothing staged, nothing modified: `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`,
`MANUSCRIPT_FORMAT_RESEARCH.md`, `PAPER_CONTRACT.md`, `PHASE_E_AUDIT_REPORT.md`, `PHASE_E_PLAN.md`,
`PUBLIC_RELEASE_BOUNDARY.md`. Diffed/read in full: `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`,
`contribution_lock.csv`, `EVIDENCE_BASELINE.md`, `EXPERIMENT_1_POSTHOC_ANALYSIS.md`,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PHASE_E_PLAN.md`, `PUBLIC_RELEASE_BOUNDARY.md`,
`literature/citation_ledger.csv`, `literature/ads_metric_prior_art.md`/`.csv`, `RESEARCH_GPS.md`,
`STATE.md` (partial), `TECHNICAL_REPORT.md` (targeted greps), and independently recomputed
statistics directly from `data/outputs/experiments/exp1/final/final_condition_results.csv`.

## 2. Independent recomputation of Experiment 1 numbers

Recomputed directly from the frozen 240-row CSV (Python, stdlib only, not trusting any document's
restatement):

| Quantity | Recomputed | Contract §2/§7 states | Match |
|---|---|---|---|
| Overall agree/disagree/n_defined | 32/18/50 | 32/18/50 | ✅ |
| Agreement rate | 64.0% | 64.0% | ✅ |
| Wilson 95% CI | [50.14%, 75.86%] | [50.14%, 75.86%] | ✅ |
| Binomial p (exact, two-sided, vs 0.5) | 0.06491 | 0.0649 | ✅ |
| Realized ADS range | 0.4414–0.9258 | 0.44–0.93 | ✅ |
| 0.70–0.90 band (VARIED) agree/disagree | 32/0 (n=32) | 32/32 (100%) | ✅ |
| ≥0.90 band (VARIED) agree/disagree | 0/18 (n=18) | 0/18 (0%) | ✅ |
| VARIED empirical winner | retrieval, 120/120 | retrieval, 120/120 | ✅ |
| CLEAN empirical winner | tie, 120/120 | tie, 120/120 | ✅ |
| Pearson r(ADS, rules) CLEAN / VARIED | 0.9592 / 0.9091 | 0.909–0.959 (rules) | ✅ |
| Pearson r(ADS, retrieval) CLEAN / VARIED | 0.9549 / 0.9476 | 0.948–0.955 (retrieval) | ✅ |
| δ=0.02, cutoff=75 | confirmed in `stats.py`/CSV | δ=0.02, cutoff=75 | ✅ |

**Fact:** every number in §2 rows 3–5 and §7's Experiment 1 block is exactly reproducible from the
raw, frozen CSV. No rounding was found that changes the qualitative picture (0/18 is stated as 0%,
never softened).

## 3. Contribution Lock cross-check (§2, §3, §8)

**Fact:** §2 rows 1–11 each trace to a specific `CONTRIBUTION_LOCK.md` or `contribution_lock.csv`
location; spot-checked every row against the source text (§3, §4, §6, §7, §11 of
`CONTRIBUTION_LOCK.md`) — wording is compressed/paraphrased but never strengthened. §7's synthesis
sentence in the contract ("informative about classification-mechanism difficulty, not about
mechanism ranking...") matches `CONTRIBUTION_LOCK.md` §6's Synthesis paragraph in substance and
hedge level.

**Fact:** §3's 16 forbidden claims all map onto `CONTRIBUTION_LOCK.md` §7's rejected list, §3's
candidate-contribution table (C2, C3 CHALLENGED statuses), §5 rows 3–4 (Formulation #3/#4), or
`EVIDENCE_BASELINE.md` §3 (mapping-count). No forbidden claim was invented, and — checked against
the task's explicit "known rejected/limited claims" floor — none of ADS-as-novel, general
design-time-selection-as-novel, the combined-system novelty claim, the "no vendor" claim, universal
applicability, or "R3 selects the right mechanism" is silently upgraded anywhere in §2. All appear
only in §3 (forbidden) or with the correct hedge in §2.

**Fact:** §8's "Formulation #2" is reproduced with the same two-part (6a/6b) + synthesis structure
as `CONTRIBUTION_LOCK.md` §6, and explicitly rejects Formulations #1 (too weak), #3 (too strong),
#4 (rejected) using the same reasoning `CONTRIBUTION_LOCK.md` §6's "Why #2 over #1 or #3" gives.

## 4. Phase B/C literature cross-check (§2 row 8, §3, citation ledger)

**Fact:** B8-04/05/06 (Ken From Finance, Peakflo, Ramp) are `VERIFIED-INDUSTRY` in
`citation_ledger.csv`, matching §2 row 11's requirement that industry rows be labeled
not-peer-reviewed. Rice 1976 (B1-01), Smith-Miles 2009 (B2-01), Barbudo et al. 2023 (B2-02),
Idreos & Kraska 2019 (B7-01), FrugalGPT (B3-02), Jørgensen & Igel 2021 (B8-01) are all `VERIFIED`
in the ledger, matching their use in §2 row 8 and §3 rows 3/5.

**Finding (minor, documentation gap — see §11.1 below):** The C1-rejection sources actually named in
§2 row 1 / §3 row 1 (Manning, Raghavan & Schütze 2008; Amigó et al. 2009; Dawid & Skene 1979) do
**not** appear in `citation_ledger.csv` at all. They are verified in a separate file,
`research/literature/ads_metric_prior_art.md`/`.csv` (confirmed directly — DOIs, venues, and a
`VerificationMethod` column are present and populated for all three). `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`
§2 row 1 correctly cites this separate file as the artifact. But `PAPER_CONTRACT.md` §4's evidence
hierarchy (tier 3, "literature ledger") names only `citation_ledger.csv` and never mentions
`ads_metric_prior_art.md`/`.csv` anywhere in the document — even though the contract's own §2 row 1
and §3 row 1 depend entirely on those three sources. A future drafting session following §4 literally
would not know where the C1-rejection citations are verified.

## 5. Production data rule (§5) vs. scope documents

**Fact:** `CONTRIBUTION_LOCK.md` §8 bounds production evidence to "one motivating production case
study (confidential, cited not reproduced)... contributes no statistical evidence to §6."
`PUBLIC_RELEASE_BOUNDARY.md` §3.A explicitly allows "production aggregate statistics, cited as such"
and "the case study framed explicitly as 'cited, not reproduced,'" and explicitly disallows framing
it as "independently-reproducible evidence." Contract §5 ("motivation and case-study evidence only
... never in the Results section, never as statistical support for §6a/§6b, and never described as
'validated'... every appearance must carry [the] qualifier") is consistent with, and slightly more
conservative than, both source documents (the "never in the Results section" clause is an
elaboration, not present verbatim in either source, but it does not contradict either — it's a
strict reading of "motivating context only" that both sources support). No drift found.

## 6. Numerical rule (§7) — canonical vs. superseded

**Fact:** `EVIDENCE_BASELINE.md` §2/Note 1 gives canonical post-A5-fix values weighted ADS 0.9031,
unweighted 0.9597, deterministic-share 87.56%, and marks 0.8094/0.9310/84.12% `SUPERSEDED — DO NOT
CITE`. Contract §7 states these exactly, in the same canonical/superseded split.

**Fact, independently re-verified by direct grep of `TECHNICAL_REPORT.md`:** §3.2/§3.3 (lines
219–220) still show `0.809 / 0.931` and `84.1%` (the superseded values); §5 (lines 289–291) still
contains the vendor-practice sentence contradicted by B8-04. Contract §7 and §13 correctly describe
this as a known, pre-existing staleness issue that the contract does not fix and is not required to
fix — matching the instruction's framing exactly. This was also independently confirmed by the prior
`PHASE_E_AUDIT_REPORT.md` pass (§4 of that report), so this is now confirmed by two independent
direct reads.

## 7. E3 definition (§11) vs. `PHASE_E_PLAN.md`

**Fact:** `PHASE_E_PLAN.md` Task 9's E3 row ("Full prose in every section... every claim traces to a
row in `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`... document compiles cleanly") is a compressed version of
what contract §11 spells out in full (per-section prose requirement, citations resolving to
`references.bib`, F1–F4/F5/F8 placeholders per Task 7, Limitations undiluted, References compiling,
no TODO stub) plus an explicit "does NOT require" list (perfect prose, final typography, final
journal formatting, polished figures). The two documents do not conflict; §11 is a legitimate,
non-strengthening elaboration of the same milestone. The definition is self-check-able: a future
session can enumerate the required sections/subsections, grep for "(to be written)"/stub patterns,
and check `references.bib` compiles — no vague criterion requires human judgment calls beyond what's
already explicit.

## 8. Scientific consistency

Traced the full chain (research question → H1 → Experiment 1 design → 240-condition run → D.1
post-hoc analysis → Gate 4 lock → PAPER_CONTRACT.md) and found no broken link: every number the
contract cites is the D.1-analysis number, which is the same number the Gate-4 auditor
independently re-derived, which this pass re-derived a third time from the raw CSV and got the same
result. No aggregation choice, threshold, or definition changed silently between any of these three
independent derivations (Gate-4 auditor's, `EXPERIMENT_1_POSTHOC_ANALYSIS.md`'s, this pass's).

## 9. Evidence/claim traceability

Every quantitative claim in §2/§7 traced to a specific, currently-committed artifact (the frozen
CSV, `EVIDENCE_BASELINE.md`, or `contribution_lock.csv`) and was independently recomputed rather
than trusted, per §2 above. No number in the contract was found that isn't in one of
`CONTRIBUTION_LOCK.md`, `EVIDENCE_BASELINE.md`, or the frozen Experiment 1 artifacts.

## 10. Code review

Not applicable — no code changed. (`PAPER_CONTRACT.md`'s claim that "no new analysis or experiment
was run to produce it" was checked by confirming no `.tex`, no new script, and no modified CSV exists
in the working tree beyond the six untracked `.md` planning files — confirmed by `git status`.)

## 11. Findings

1. **[REQUIRED NOW]** Evidence-hierarchy gap: `PAPER_CONTRACT.md` §4 tier 3 names
   `research/literature/citation_ledger.csv` as "the literature ledger" but never mentions
   `research/literature/ads_metric_prior_art.md`/`.csv` — the actual verification source for the
   three citations (Manning, Raghavan & Schütze 2008; Amigó et al. 2009; Dawid & Skene 1979) that
   back §2 row 1 and §3 row 1, the contract's single most load-bearing negative claim (ADS is not a
   novel metric). A drafting session strictly following §4's stated hierarchy would not know where
   to find or re-verify these three sources, or might mistakenly treat them as uncited/unverifiable
   since they don't appear in the named tier-3 file. Fix: add one line to §4 tier 3 naming
   `ads_metric_prior_art.md`/`.csv` alongside `citation_ledger.csv` as an equally-authoritative
   literature source for the C1 comparison specifically.
   File: `research/PAPER_CONTRACT.md`, §4 (lines ~85–87) and §2 row 1 / §3 row 1.

2. **[REQUIRED NOW]** Internal inconsistency: §4 tier 3 restricts the literature ledger to
   `VERIFIED`/`VERIFIED-INDUSTRY`/`VERIFIED-PREPRINT` rows (three categories), but §2 row 11
   restricts citable Related-Work positioning statements to "`VERIFIED` / `VERIFIED-INDUSTRY` rows
   only" (two categories, omitting `VERIFIED-PREPRINT`). `citation_ledger.csv` does contain at least
   one `VERIFIED-PREPRINT` row (B3-03, Graves 2016). This is a self-contradiction within the
   contract, not a research-integrity violation — but it is exactly the kind of internal
   inconsistency the audit brief asked to hunt for, since the document's whole purpose is precision
   about what's citable. Fix: make §2 row 11's category list match §4 tier 3's exactly (either both
   three-category, or state explicitly why row 11 is narrower).
   File: `research/PAPER_CONTRACT.md`, §2 row 11 vs. §4 (tier 3).

3. **[OPTIONAL FUTURE WORK]** The document has 13 numbered sections (§1 North star through §13
   Conflicts found), one more than the "12 sections" referenced in the audit brief. Section 13
   ("Conflicts found while assembling this contract") is a short, non-claim-bearing transparency
   note (states "None," and correctly recharacterizes the two known `TECHNICAL_REPORT.md` staleness
   items as already-covered by §4/§7's rules rather than new conflicts) — it does not introduce new
   claims or scope. This reads as reasonable diligence rather than scope creep, but is flagged since
   the brief explicitly asked to check section count against expectation and I cannot independently
   confirm what the original 12-section spec was.
   File: `research/PAPER_CONTRACT.md`, §13.

4. **[OPTIONAL FUTURE WORK]** `RESEARCH_GPS.md`'s "CURRENT LOCATION"/"CURRENT GATE"/Gate 4 checklist
   are stale relative to `CONTRIBUTION_LOCK.md` (Gate 4 shown unchecked despite being "Adopted" with
   an auditor PASS) — already correctly flagged by the contract itself (§4 tier 5) and by the prior
   `PHASE_E_AUDIT_REPORT.md`. Not a new finding; restated only because the task asked me to flag if
   the contract's own self-description of staleness is accurate. It is accurate — confirmed by direct
   read of `RESEARCH_GPS.md` lines 12–68.
   File: `research/RESEARCH_GPS.md`, lines 14, 58–64.

5. **[OPTIONAL FUTURE WORK]** No sentence was found in `PAPER_CONTRACT.md` that states a claim with
   more confidence, generality, or causal force than its cited source — this was the primary failure
   mode the task asked me to hunt for, checked row-by-row across §2, §3, §6, §7, §8. Every
   correlational claim is labeled correlational (§2 row 3, "Correlational"); every inferred-causal
   claim carries its epistemic-weight hedge (§2 row 6, "INFERRED... never as 'we prove' or 'we
   demonstrate causally'"); every generalization is explicitly scoped (§6). Recorded here as a
   checked-and-clear item, not a gap.

## 12. Required fixes

1. Add `research/literature/ads_metric_prior_art.md`/`.csv` to §4 tier 3 (or a new tier) as the
   verification source for the Manning/Amigó/Dawid-Skene citations underlying §2 row 1 and §3 row 1.
2. Reconcile §2 row 11's citable-status category list with §4 tier 3's category list (both should
   name the same set of `VERIFIED*` statuses, or the narrower row should explain why it excludes
   `VERIFIED-PREPRINT`).

Both fixes are single-line, non-substantive additions to `PAPER_CONTRACT.md` — they correct a
documentation/hierarchy gap, not any claim, number, or scope boundary. Nothing in §§2/3/5/6/7/8
needs to change in content.

## 13. Verdict

## 🟠 CONDITIONAL

Every quantitative claim in `PAPER_CONTRACT.md` was independently re-derived from the frozen
Experiment 1 CSV and matches exactly (§2 above). Every claim in §2/§3/§8 traces cleanly to
`CONTRIBUTION_LOCK.md`/`contribution_lock.csv` with no strengthening, no dropped qualifier, and no
resurrected rejected claim found anywhere in the document. The Production Data Rule (§5) and the
Numerical Rule's canonical/superseded split (§7) are both correctly, conservatively stated and
independently confirmed against `EVIDENCE_BASELINE.md`, `PUBLIC_RELEASE_BOUNDARY.md`, and a direct
grep of `TECHNICAL_REPORT.md`. The E3 definition (§11) is self-check-able without guessing. This is
a well-constructed contract with no research-integrity violation and no invented claim.

The verdict is CONDITIONAL rather than PASS/PASS_WITH_NOTES solely because of the two REQUIRED NOW
findings in §11 above: an evidence-hierarchy gap (the C1-rejection literature sources aren't
reachable via the hierarchy the contract itself defines) and an internal category-list
inconsistency (§2 row 11 vs. §4 tier 3). Both are narrow, mechanical, single-line fixes to the
contract's own internal plumbing — not signs of drift, overclaiming, or evidence problems — but
since this document's explicit purpose is to be the precise, self-consistent reference a future
session drafts against without needing to re-derive anything, leaving a citation-source gap and a
self-contradictory eligibility list in place would undermine exactly the property the contract
exists to guarantee. Fix both, then this document is safe to treat as binding for Phase E1 onward.
