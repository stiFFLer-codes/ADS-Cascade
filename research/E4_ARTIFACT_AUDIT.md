# E4 Artifact Audit — Claim/Evidence, Novelty, Production Case-Study, Statistics, and Reproducibility

> **Scope of this document.** Independent, evidence-grounding pass over the Phase E3 manuscript
> checkpoint (`manuscript/main.tex` @ commit `95c2b18b7a49898233a1d0d44e4cfbae1fb7c071`, in full,
> plus `manuscript/references.bib`), covering exactly Parts B, E, F, G, I of the Phase E4 audit brief
> plus an independent verdict. This is not a literary/structural critique (a separate report covers
> that) and not a re-litigation of the locked contribution — it is artifact verification: does every
> number and framing in the manuscript actually trace to, and match, the repository's own frozen
> evidence. No file was modified to produce this document. No experiment was run. No new literature
> search was performed. `manuscript/main.tex`, `manuscript/references.bib`,
> `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, and all frozen Experiment 1
> artifacts were read, not edited.
>
> **Sources read in full:** `manuscript/main.tex` (1518 lines), `manuscript/references.bib`,
> `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`,
> `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `research/EVIDENCE_BASELINE.md`,
> `research/literature/contribution_status.md`, `research/literature/citation_ledger.csv`,
> `research/literature/ads_metric_prior_art.csv`, `research/literature/llm_advisory_prior_art.csv`,
> `research/EXPERIMENT_1_FINAL_RESULTS.md`, `research/EXPERIMENT_1_EVIDENCE_CHECKPOINT.md`,
> `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `research/EXPERIMENT_1_DATA_DICTIONARY.md`,
> `research/EXPERIMENT_1_CALIBRATION_REPORT.md`, `research/r3_threshold_analysis.md`, plus targeted
> greps of `METHODOLOGY.md` and `research/EXPERIMENT_1_REDESIGN_REVIEW.md`.

---

## PART B — Claim/Evidence Audit

For each claim: **Source**, **Verification**, **Classification**. Classification vocabulary:
SUPPORTED, CONDITIONALLY_SUPPORTED, CASE_STUDY_ONLY, UNSUPPORTED, SUPERSEDED, AMBIGUOUS.

| # | Claim (manuscript location) | Source artifact | Verification | Classification |
|---|---|---|---|---|
| B1 | ADS formula, $\text{ADS}(p)=\max_i c_i/\sum_i c_i$ (Eq. 1, §3.2) | `TECHNICAL_REPORT.md` §2.2; `PAPER_CONTRACT.md` §2 row 1 | Definitional; matches the canonical formula exactly, correctly paired with the cluster-purity equivalence sentence in the same subsection, per `PAPER_CONTRACT.md` §2 row 1's requirement. | SUPPORTED (as a definition, explicitly non-novel) |
| B2 | ADS is mathematically identical to cluster purity (Manning 2008; Amigó 2009) and the Dawid–Skene majority-vote-agreement baseline (§2.1, §3.2) | `ads_metric_prior_art.csv` rows G1-01–G1-04 | G1-01/G1-02 give the identical closed-form `max_j(count)/size`. G1-04 (Dawid–Skene) is flagged in the ledger itself as "Analogous," not "Equivalent," for the model's own output — the *equivalent* quantity is only Dawid–Skene's informal majority-vote baseline comparator, "never named as a citable metric in its own right" (ledger notes). The manuscript's phrasing ("the same quantity under a different name") is a defensible compression of that nuance but slightly overstates the G1-04 row's own equivalence label (which is "Analogous" for the paper as a whole, "Equivalent" only for the baseline-within-the-paper). | CONDITIONALLY_SUPPORTED — correct for G1-01–03 (cluster purity), a minor precision loss for the Dawid–Skene framing (see Finding F1). |
| B3 | "No claim that design-time selection from historical evidence is itself new" — Algorithm Selection Problem (Rice 1976), Smith-Miles 2009 (§2.2) | `citation_ledger.csv` B1-01, B2-01; `contribution_status.md` C2 | Matches: C2 is CHALLENGED at the general-pattern level per the ledger; manuscript correctly states only the narrower C2b question is being tested. | SUPPORTED |
| B4 | AutoML/workflow composition (Barbudo 2023) is the closest terminological echo but a different evidence type/mechanism (§2.3) | `citation_ledger.csv` B2-02 | Ledger's `WhyRelevant` field: "black-box optimized search over configurations, not a historical-label-consistency-driven qualitative architecture decision" — matches manuscript's framing closely. | SUPPORTED |
| B5 | Idreos & Kraska 2019 is the closest non-ML structural analog, opposite temporal philosophy (§2.4) | `citation_ledger.csv` B7-01 | Ledger: "continuous, self-adapting design driven by workload/query FREQUENCY... a different evidence type and a one-shot rather than continuously-adapting decision" — matches. | SUPPORTED |
| B6 | Chow 1970 / El-Yaniv & Wiener 2010 / Hendrickx 2024 establish reject-option/selective-classification lineage; not directly engaged because Exp 1 is design-time, not runtime (§2.5) | `citation_ledger.csv` B4-01, B4-02, B4-05 | Matches ledger descriptions exactly; the design-time/runtime distinction is the ledger's own recurring framing across B4/B5 rows. | SUPPORTED |
| B7 | Mozannar & Sontag 2020 establishes learning-to-defer; not an instance of Exp 1's rule, same design/runtime boundary (§2.6) | `citation_ledger.csv` B5-02 | Matches. | SUPPORTED |
| B8 | FrugalGPT (Chen 2023) closest cascade match, RankGPT (Sun 2023) establishes LLM-reranking as commodity technique; neither engaged, LLM excluded from Exp 1 (§2.7) | `citation_ledger.csv` B3-02, B6-02; `EXPERIMENT_1_REDESIGN_REVIEW.md` §10 | Matches; LLM-exclusion rationale independently verified against `EXPERIMENT_1_REDESIGN_REVIEW.md` §10 (see Part I). | SUPPORTED |
| B9 | Jørgensen & Igel 2021 shows the identical cross-company generalization phenomenon in the same domain (§2.8) | `citation_ledger.csv` B8-01 | Ledger: "Empirically demonstrates the EXACT phenomenon... in the SAME application domain" — matches, including the correct hedge that it's "reported there as a direct accuracy gap rather than formalized into a named metric." | SUPPORTED |
| B10 | "At least one industry source directly contradicts" the no-vendor-measures-consistency framing, and this is still uncorrected in `TECHNICAL_REPORT.md` (§2.8) | `citation_ledger.csv` B8-04 (Ken From Finance); `CONTRIBUTION_LOCK.md` §7 | B8-04 is `VERIFIED-INDUSTRY` (not peer-reviewed) and does independently recommend a pre-deployment historical-consistency audit, contradicting the "no vendor measures this" framing. Manuscript correctly labels this an open, uncorrected item tracked outside the manuscript rather than silently repeating the false framing. | SUPPORTED (as a hedge/disclosure, not as new vendor-practice research) |
| B11 | Realized ADS is train-only, invariant to lexical condition by construction, confirmed byte-identical between CLEAN/VARIED at every target (§4.4) | `EXPERIMENT_1_DATA_DICTIONARY.md` "What realized ADS is, precisely"; `EXPERIMENT_1_FINAL_RESULTS.md` §2 | Matches exactly, including the specific example cited (target=0.75: 0.7973±0.0105 both conditions). | SUPPORTED |
| B12 | Realized ADS ranges 0.44–0.93 across the frozen run, structurally capped below ~0.91 by `CROSS_COMPANY_ALIGN=0.695` (§4.4) | `EXPERIMENT_1_CALIBRATION_REPORT.md` §2 (mean ceiling 0.9076, individual max 0.9211 at target=0.99); `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §10 (target=1.00 individual range 0.894–0.926) | Numerically consistent: min ≈0.44 (target=0.00, individual min 0.441), max ≈0.93 (target=1.00, individual max 0.926). The "capped below ~0.91" language describes the *mean* ceiling; individual seeds legitimately exceed it up to ~0.926. This exact phrasing is inherited verbatim from `CONTRIBUTION_LOCK.md` §8 and `PAPER_CONTRACT.md` §6/§7 — not a manuscript-introduced imprecision — but the juxtaposition ("capped below approximately 0.91" next to "ranges... to 0.93") reads as self-contradictory to a reader who does not already know mean vs. individual-seed variance is the resolving distinction. | AMBIGUOUS (wording inherited from locked evidence, numerically consistent on inspection, but not self-explanatory in context — see Finding F2) |
| B13 | Pearson r(realized ADS, rules acc) ≈ 0.909 (VARIED) / 0.959 (CLEAN); r(realized ADS, retrieval acc) ≈ 0.948 (VARIED) / 0.955 (CLEAN) (§5.2, Table T4) | `CONTRIBUTION_LOCK.md` §4; `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §11 (rounded: 0.96/0.91, 0.95/0.95) | Manuscript's more-precise figures match `CONTRIBUTION_LOCK.md`'s independently-audited precise values exactly (`PAPER_CONTRACT.md` §7 canonical: "0.909–0.959 (rules) / 0.948–0.955 (retrieval)"). | SUPPORTED |
| B14 | Under VARIED, empirical winner = retrieval in 120/120 conditions, exceptionless, unconditional on realized ADS 0.44–0.93 (§5.3) | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §11; `final_condition_results.csv` | Matches `CONTRIBUTION_LOCK.md` §4/§6b exactly, itself independently re-derived by a prior audit. | SUPPORTED |
| B15 | Under CLEAN, empirical winner = tie in 120/120 conditions, exceptionless (§5.3) | Same as B14 | Matches. | SUPPORTED |
| B16 | R3 agrees 100% (32/32) in realized 0.70–0.90 band, 0% (0/18) in realized ≥0.90 band (§5.4) | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5, §9 | Exact match to the per-row realized-ADS-band table. | SUPPORTED |
| B17 | Secondary by-nominal-target framing: 30/30 (100%) at targets 0.50/0.75, 2/20 (10%) at target 1.00 (§5.4) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 | Exact match. | SUPPORTED |
| B18 | Overall 32/50 (64.0%) agreement, Wilson CI [50.14%, 75.86%], p=0.0649 (§5.4, Table T4) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §6; independently re-derived below (Part G) | Wilson-CI hand-recomputation in Part G reproduces [50.14%, 75.87%] (0.01pp rounding difference, immaterial). | SUPPORTED |
| B19 | p=1.9×10⁻⁹ (30/30) and p=4.0×10⁻⁴ (2/20) are correctly paired with the **by-nominal-target** counts, not the per-row realized-band counts (32/32, 0/18) (§5.4, Table T4 caption) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7; Table T4's own footnote documents a prior CONDITIONAL fix from `E3_DRAFT_AUDIT_REPORT.md` | Independently re-derived exact two-sided binomial p-values in Part G: 30/30 → 2×2⁻²⁹ ≈ 1.86×10⁻⁹ ✓; 2/20 → 422/2²⁰ ≈ 4.03×10⁻⁴ ✓. Table T4's own caption explicitly states no p-value is claimed for 32/32/0/18. Correctly resolved. | SUPPORTED |
| B20 | Table T5: mean accuracy and rules−retrieval gap by realized-ADS band × lexical condition (§5.5) | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5 | Every one of the 6 rows (n, rules acc, retrieval acc, gap) matches the source table exactly to 4 decimal places. | SUPPORTED |
| B21 | "The interaction is real, monotonic, and continuous... not threshold-like" mechanistic account (§6.5) | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §7–8 | Matches; correctly hedged as "inferred from exhaustive but post-hoc inspection... not a second independently designed confirmatory experiment," exactly the epistemic weight `CONTRIBUTION_LOCK.md` §2 step 8 requires. | SUPPORTED (as INFERRED, correctly labeled) |
| B22 | H1 verdict = PARTIALLY_SUPPORTED, matching the pre-registered falsification-table row exactly, not a post-hoc reinterpretation (§4.11, §7.10) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §9; `EXPERIMENT_1_REDESIGN_REVIEW.md` §18 | Matches; the checkpoint's own §9 verdict text and reasoning (band effect + CLEAN uninformative + aggregate inconclusive) is reproduced faithfully, not softened toward SUPPORTED. | SUPPORTED |
| B23 | Retrieval coverage 1.0 in all 240 conditions; rules coverage always <1.0, real asymmetry not normalized away (§3.3–3.4, §7.10) | `EXPERIMENT_1_FINAL_RESULTS.md` §2 integrity checks | Matches: "`retrieval_coverage` 1.0 in all 240 conditions"; "`rules_coverage` < 1.0 in all 240 conditions." | SUPPORTED |
| B24 | Retrieval cutoff = 75, calibrated once via product-identity hit-rate (not accuracy), disjoint calibration seeds, never re-tuned (§4.7) | `EXPERIMENT_1_CALIBRATION_REPORT.md` §5–6 | Matches exactly, including the specific "does not use classification accuracy... uses product-identity hit rate" distinction and the cutoff-selection table (60–95 candidates, 75 selected by the tie-break-toward-conservative rule). | SUPPORTED |
| B25 | δ=0.02 practical-equivalence margin fixed before the run at the calibration stage, not re-examined against outcome data (§4.10, §5.6) | `EXPERIMENT_1_CALIBRATION_REPORT.md` §8–9 | Matches; the manuscript's justification ("a judgment call... anchored to precedent") is a compressed but accurate restatement of the calibration report's own §9.5 justification. | SUPPORTED |
| B26 | Production case study is motivating context only, never statistical evidence for §5/§6a/§6b (§6.2, throughout) | `PAPER_CONTRACT.md` §5 | Verified directly: no production number appears anywhere in §5 Results; every appearance in §1/§6/§7 carries or is adjacent to the required caveat (with one partial exception — see Part F, Finding F3). | CASE_STUDY_ONLY (correctly scoped, one location under-qualified — see Part F) |
| B27 | Synthesis: "historical consistency is informative about mechanism difficulty, not ranking, when ranking is governed by a representation-stability property the signal does not observe" (§6.1, §9) | `CONTRIBUTION_LOCK.md` §6, exact wording to reuse | Manuscript's wording is a close paraphrase, not a verbatim reuse, but preserves the exact epistemic structure (refinement, not confirmation) `CONTRIBUTION_LOCK.md` §6 specifies. Formulation #2, not #1/#3/#4. | SUPPORTED |

**Overall Part B assessment:** of 27 claims audited, 24 are SUPPORTED, 2 are CASE_STUDY_ONLY/CONDITIONALLY_SUPPORTED with a precise, narrow qualification (Findings F1, F3), and 1 is AMBIGUOUS due to wording inherited unchanged from the locked contract (Finding F2). No claim in this sample is UNSUPPORTED or SUPERSEDED. No stale (pre-A5-fix) number was found cited as current anywhere in the manuscript body — the manuscript's own two production/synthetic figures (91.2%, 87.56%) are both the current canonical values per `EVIDENCE_BASELINE.md`.

---

## PART E — Novelty/Prior-Art Audit

Checked whether the manuscript accidentally claims novelty for any of: ADS itself, cluster
purity/majority agreement, the Algorithm Selection Problem, meta-learning, workflow composition,
model cascades, selective classification, reject option, LLM ranking, human deferral.

| Concept | Manuscript location | Claim made | Consistent with `contribution_status.md` verdict? |
|---|---|---|---|
| ADS as a metric | §2.1, §3.2, abstract | Explicitly non-novel: "mathematically identical to cluster purity... We therefore make no claim that ADS is a novel metric — this is a closed question" | Yes — matches C1 REJECTED/CHALLENGED exactly, including the "closed question, not an open one" framing from `contribution_status.md`'s own C1 verdict text. |
| Cluster purity / majority agreement | §2.1 | Cited as prior art establishing the identity, not claimed | Yes. |
| Algorithm Selection Problem (Rice 1976) | §1.3, §2.2 | "a specific, narrower instance of a well-established research question, not a new one" | Yes — matches C2 CHALLENGED. |
| Meta-learning (Smith-Miles 2009) | §2.2 | Cited as unifying frame, not claimed | Yes. |
| AutoML / workflow composition (Barbudo 2023) | §2.3 | Explicitly: "We do not claim that this paper's simple, interpretable threshold rule competes with that automated search paradigm" | Yes. |
| Model cascades (FrugalGPT) | §2.7 | "We do not claim that Experiment 1's two-mechanism comparison is itself a cascade contribution" | Yes — matches C3 CHALLENGED; correctly notes the shipped cascade (C3) is not evaluated in Exp 1 at all. |
| Selective classification / reject option (Chow 1970, El-Yaniv 2010, Hendrickx 2024) | §2.5 | "We make no claim that this experiment introduces a new reject-option variant" | Yes — matches B4 ledger rows; correctly draws the design-time/runtime line rather than claiming novelty on either side of it. |
| LLM ranking (RankGPT) | §2.7 | Cited only for the design-time/runtime distinction; LLM excluded from Exp 1 | Yes — matches C4's PARTIALLY_SUPPORTED status is not even invoked, since the manuscript doesn't claim the C4 four-part-combination novelty at all in Results (C4 concerns the *shipped cascade*, out of Exp 1's scope; correctly absent from the Results/Discussion sections). |
| Human deferral (Mozannar & Sontag 2020) | §2.6 | "We do not claim that this experiment's mechanism-selection rule is an instance of learning to defer" | Yes — matches B5 ledger rows. |

**No instance found** of the manuscript claiming novelty for any of the ten listed concepts beyond
what `contribution_status.md`/`citation_ledger.csv` currently support. Every Related Work subsection
in §2 follows the same rhetorical pattern: name the closest prior art, state explicitly what is *not*
claimed, then state the (narrow) delta actually being tested. This pattern is applied consistently
across all eight subsections and Table T2.

**One item flagged for precision, not for a novelty violation (see also B2/Finding F1):** §2.1's
sentence "Independently, the raw majority-vote agreement proportion used throughout the crowdsourcing
and truth-inference literature descending from Dawid & Skene (1979) is the same quantity under a
different name" compresses the ledger's own G1-04 nuance (Dawid–Skene's *model output* is
"Analogous," not "Equivalent"; only its *naive baseline comparator* is the truly identical quantity,
and even that baseline "is not itself named/defined as a standalone metric in this paper" per the
ledger). The manuscript's simplification is defensible for a Related Work paragraph and does not
create a false novelty claim in either direction, but a reviewer checking primary sources against the
ledger could flag the compression as slightly overstated equivalence. This is the same finding as B2,
not a new one — listed here because it is the Part E-relevant instance of it.

**Part E verdict: no novelty-inflation violations found.** The manuscript's Related Work section is
the strongest-audited section of the draft — every claim in it traces cleanly to a specific,
already-verified ledger row, and the "we do not claim X" disclaimer pattern is applied exhaustively
rather than selectively.

---

## PART F — Production Case-Study Audit

Every location where a production-sourced number or claim appears in the manuscript, with exact
framing:

| Location | Number/claim | Framing | Compliant with `PAPER_CONTRACT.md` §5? |
|---|---|---|---|
| §1.1, line 100 | 91.2% deterministic → RULES_FIRST | "In one production deployment, that statistic was measured at 91.2%..." followed two sentences later by "the production figures cited here are drawn from a confidential engagement, not independently reproducible from this repository" | Yes — caveat present in the same paragraph. |
| §1.1, line 103 | 87.56% → "retrieval-based mechanism" (i.e., the synthetic-branch EMBEDDING_PRIMARY decision) | Not itself a production figure (it is the *synthetic* reproduction's figure, publicly reproducible per `EVIDENCE_BASELINE.md` §2) — correctly not carrying the "confidential" caveat, since that caveat is scoped only to the production figure in the same sentence pair. | Yes, and correctly distinguished from the production figure — see Finding F4 for a related terminology concern. |
| §4.2, line 600 | Cross-company alignment fixed at 0.695, "the production-observed value" | **No "cited from a confidential engagement, not independently reproducible from this repository" qualifier attached at this location.** Every other appearance of a production number in the manuscript (91.2%, 0.847, 0.964, and 87.56%'s production counterpart) carries this qualifier at or near its point of use; this one does not. | **No — see Finding F3 (CONDITIONAL).** |
| §6.2 | Repeats the 91.2%/87.56% observation and its caveat, extended: "generated by an earlier version of the measurement pipeline and are cited from a confidential engagement, not independently reproducible from this repository" | Correctly repeated rather than assumed to carry forward from §1.1 (the manuscript's own stated design goal, per its EVIDENCE comment). | Yes. |
| §7.6 (Limitations, "Production Confidentiality") | 91.2%, weighted ADS 0.847, unweighted ADS 0.964 | "were generated by an earlier version of the measurement pipeline and remain likely understated and unverified; they cannot be re-run against the corrected pipeline, since no production data exists in this repository" | Yes — matches `EVIDENCE_BASELINE.md` Note 1's exact caveat content and reasoning. |
| §7.7 (Limitations, "Absence of Independent Production Validation") | "Production never ran a lexical-noise sweep; only two single-run data points feed the... narrative" | Explicit negative statement, matches `CONTRIBUTION_LOCK.md` §7's rejected-claim framing. | Yes. |
| Reproducibility Statement | "the production case study... is confidential and not reproducible from this repository in any sense; only its cited aggregate statistics appear in this paper" | Correctly scoped. | Yes. |

**Never observed:** any production number used as statistical support inside §5 (Results), described
as "validated," "confirmed," or "independently reproduced," or silently reused without its caveat
after having carried it once. The Introduction/Discussion/Limitations placement matches
`PAPER_CONTRACT.md` §5's "Introduction to motivate, briefly in Discussion, never in Results" rule
exactly.

**Part F verdict:** production evidence is used correctly as motivation/case-study context in every
location but one (§4.2's 0.695 figure), which is a real, narrow, concrete compliance gap against
`PAPER_CONTRACT.md` §5's own explicit rule ("**every** appearance of a production number must carry"
the qualifier) — see Finding F3. No instance of production data silently becoming experimental
validation, reproducibility evidence, or proof of the synthetic result was found.

---

## PART G — Results/Statistics Audit (sixth independent pass)

Independently re-derived, not merely re-read:

**32/32, 0/18 (realized-ADS-band per-row counts, §5.4):** Cross-checked against
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5/§9's own independently-recomputed table (n=32 at 0.70–0.90,
n=18 at ≥0.90, both VARIED, zero rules-wins/ties in either band). Manuscript states these correctly
as *not* paired with any p-value (Table T4 caption: "no independently frozen p-value exists for
those exact counts, so none is stated here") — this is the correct resolution of the CONDITIONAL
finding a prior audit (`E3_DRAFT_AUDIT_REPORT.md`) raised about a prior draft misattributing p-values
to these counts. Confirmed fixed.

**30/30, 2/20 (by-nominal-target counts, §5.4, §5.6):** Matches
`EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §7 exactly.

**64.0% (32/50) — recomputed:** 32/50 = 0.64 exactly. ✓

**Wilson CI [50.14%, 75.86%] — recomputed by hand:**
$\hat p=0.64$, $n=50$, $z=1.959964$. Center $=(\hat p + z^2/2n)/(1+z^2/n) = 0.63005$. Margin
$= \frac{z}{1+z^2/n}\sqrt{\hat p(1-\hat p)/n + z^2/4n^2} = 0.12862$. Interval $=[0.50143, 0.75867]$
→ **[50.14%, 75.87%]**. Matches the manuscript's stated [50.14%, 75.86%] to within 0.01 percentage
point (rounding-method difference in the last digit, not a discrepancy). ✓

**p=0.0649 (32/50 exact binomial, vs. 50% chance) — sanity-checked:** normal-approximation z=1.98
(two-sided p≈0.048); exact binomial (finite-sample, more conservative than the normal approximation)
producing p=0.0649 is directionally and magnitudinally consistent with a normal-approximation
check, and this exact figure has independently been re-derived five separate times across five
independently-written scripts per the E3 checkpoint commit message. Not independently re-derived to
full precision in this pass (would require enumerating all $k$ with $P(k)\le P(32)$ for $n=50$), but
no red flag found. ✓ (consistent, not independently re-derived digit-for-digit in this pass)

**p=1.9×10⁻⁹ (30/30 vs. 50% chance) — independently re-derived from first principles in this pass:**
Exact two-sided binomial for $k=n=30$: $p = 2 \times 0.5^{30} = 2^{-29} \approx 1.863\times10^{-9}$.
Matches the manuscript's stated $1.9\times10^{-9}$ exactly. ✓

**p=4.0×10⁻⁴ (2/20 vs. 50% chance) — independently re-derived from first principles in this pass:**
For $n=20$, the exact two-sided binomial p-value (sum of all outcomes at least as extreme as $k=2$,
i.e. $k\in\{0,1,2,18,19,20\}$): $\binom{20}{0}+\binom{20}{1}+\binom{20}{2}+\binom{20}{18}+\binom{20}{19}+\binom{20}{20}
= 1+20+190+190+20+1 = 422$; $p = 422/2^{20} = 422/1{,}048{,}576 \approx 4.025\times10^{-4}$. Matches
the manuscript's stated $4.0\times10^{-4}$ exactly. ✓

**Correct p-value/count pairing, confirmed:** the manuscript never pairs $1.9\times10^{-9}$ or
$4.0\times10^{-4}$ with the 32/32 or 0/18 realized-band counts — every occurrence of these two
p-values in §5.4, §5.6, and §6.3 is explicitly and consistently attached to "30 of 30" / "2 of 20"
language, with the by-target framing named in the same sentence. Table T4's own footnote documents
this as a previously-corrected misattribution (confirmed by direct inspection: the correction is
present and holds throughout the current draft).

**Nominal-target vs. realized-ADS-band framing, confirmed never conflated silently:** every instance
in §5.4/§5.6 that uses one framing explicitly names it ("realized 0.70–0.90 band" vs. "nominal
targets 0.50 and 0.75"; "by-nominal-target counts" vs. "per-row realized-ADS bands"). No sentence
found anywhere in the manuscript that states a count or p-value without specifying which binning
convention it uses.

**Part G verdict:** every headline statistic in the manuscript was re-verified against its frozen
source this pass (a sixth independent verification in this project's history for these specific
numbers), and three (30/30, 2/20's exact p-values, and the Wilson CI) were independently re-derived
from first principles rather than merely re-read. **No discrepancy found.** This is the
highest-confidence section of this audit.

---

## PART I — Reproducibility Audit

| Element | Manuscript description | Actual repo artifact | Classification |
|---|---|---|---|
| Seeds | 31001–31020, identical across all 12 cells (§4.8) | `final_seed_manifest.csv`, `final_condition_results.csv` — confirmed exactly `{31001..31020}` in `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §3–4 | FULLY REPRODUCIBLE |
| Target bands | 6 nominal targets {0.00, 0.20, 0.30, 0.50, 0.75, 1.00} (§4.3, Table T3) | `final_summary.csv` 12 rows; matches `EXPERIMENT_1_CALIBRATION_REPORT.md` §12's frozen `FINAL_TARGETS` list exactly | FULLY REPRODUCIBLE |
| Realized ADS definition | Train-only, grouped by `product_code`, invariant to lexical condition (§4.4) | `EXPERIMENT_1_DATA_DICTIONARY.md` "What realized ADS is, precisely," traced to `consistency.py` line references | FULLY REPRODUCIBLE (code cited by name and line; script present at `scripts/experiments/exp1/consistency.py`, confirmed present in repo) |
| Lexical conditions | CLEAN (p=0.0) / VARIED (p=0.3), five named transform types, per-line deterministic sub-seed (§4.5–4.6) | `EXPERIMENT_1_REDESIGN_REVIEW.md` §8; `run_final.py:43` | FULLY REPRODUCIBLE |
| Mechanism definitions | rules = exact company-then-global lookup, no threshold; retrieval = rapidfuzz WRatio, company-then-global, cutoff=75, never a rules-miss fallback (§3.3–3.4) | `EXPERIMENT_1_DATA_DICTIONARY.md` columns `rules_whole_set_accuracy`/`retrieval_whole_set_accuracy`; `mechanisms.py` (confirmed present at `scripts/experiments/exp1/mechanisms.py`) | FULLY REPRODUCIBLE |
| Retrieval cutoff | 75, calibrated once on a dedicated seed pool disjoint from the final run, via product-identity hit-rate, coverage floor 30% (§4.7) | `EXPERIMENT_1_CALIBRATION_REPORT.md` §5–6, exact cutoff table reproduced | FULLY REPRODUCIBLE |
| Winner/tie rule | Paired bootstrap on accuracy difference, 2000 resamples, 95% CI, δ=0.02 (§4.9, Eq. 3) | `EXPERIMENT_1_CALIBRATION_REPORT.md` §8; `stats.py` (confirmed present at `scripts/experiments/exp1/stats.py`) | FULLY REPRODUCIBLE |
| Statistical test | Exact two-sided binomial vs. 50% chance baseline, Wilson 95% CI (§4.9) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §6; independently re-derived in Part G above | FULLY REPRODUCIBLE |
| Train/test separation | Realized ADS computed exclusively from train split; verified in code, not merely asserted (§4.8) | `EXPERIMENT_1_EVIDENCE_CHECKPOINT.md` §11: "Verified in code: `consistency.py:106` filters to `split_of(r)=="train"`... Test account labels not used to select mechanism" | FULLY REPRODUCIBLE |
| Calibration | Three gates (ADS-target selection, retrieval cutoff, winner/CI definition), mechanism-blind, documented order | `EXPERIMENT_1_CALIBRATION_REPORT.md` full document, cross-checked against manuscript §4.11 point-by-point | FULLY REPRODUCIBLE |
| Implementation entry point | `python scripts/experiments/exp1/run_final.py` reproduces `final_condition_results.csv` exactly (Reproducibility Statement) | Confirmed: `run_final.py` exists at the stated path; `final_condition_results.csv` and companion artifacts confirmed present at `data/outputs/experiments/exp1/final/` | FULLY REPRODUCIBLE |
| Test suite | "covered by an automated test suite" (Reproducibility Statement) | Confirmed present: `test_generator_rng.py`, `test_leakage.py`, `test_mechanisms.py`, `test_lexical_transform.py`, `test_stats.py` all exist in `scripts/experiments/exp1/` | FULLY REPRODUCIBLE |
| Production case study (§1.1, §6.2) | 91.2%, weighted ADS 0.847, unweighted ADS 0.964 | Explicitly and correctly marked non-reproducible throughout (`METHODOLOGY.md`, `EVIDENCE_BASELINE.md` §1) | CONFIDENTIAL/CASE-STUDY ONLY (correctly labeled) |
| 87.56% synthetic-branch figure (§1.1) | "an independently generated synthetic reproduction of the same pipeline" | Reproducible, but via a **different** script chain (`00_generate_synthetic.py` → `03_5_dataset_intelligence.py` → `04_architecture_decision.py`, per `EVIDENCE_BASELINE.md` §2) than the one the manuscript's own Reproducibility Statement names (`scripts/experiments/exp1/run_final.py`, the Experiment 1 harness). The Reproducibility Statement's scope is explicitly limited to "every number in Section 5," so this is not a false claim, but a reader trying to reproduce the §1.1 motivating figure from the Reproducibility Statement alone would not find the right entry point. | PARTIALLY REPRODUCIBLE — reproducible in principle from this repository, but the path to reproduce it is never named anywhere in the manuscript (see Finding F5, minor/optional) |

**Part I verdict:** every element of Experiment 1 itself (the paper's actual evidentiary core) is
FULLY REPRODUCIBLE — seeds, targets, mechanism code, cutoff, winner rule, statistical test, and
train/test separation are all traceable to named files/line numbers in already-existing frozen
documentation, and this pass confirmed the named scripts and data files actually exist at the stated
paths. The one gap (Finding F5) is minor and affects only a motivating Introduction figure, not any
Results-section number.

---

## Findings

**F1 (OPTIONAL FUTURE WORK).** §2.1's Dawid–Skene equivalence sentence ("the same quantity under a
different name") slightly compresses `ads_metric_prior_art.csv` row G1-04's own more careful
"Analogous" (not "Equivalent") label for the Dawid–Skene model itself — the true mathematical
identity is only with Dawid–Skene's informal, uncited majority-vote baseline comparator, not the
paper's own EM-estimated posterior. This does not create a false novelty claim (if anything it
under-claims novelty, which is the safe direction), but a precise reviewer could ask the authors to
tighten the sentence to distinguish "Dawid–Skene's own estimator" from "the naive baseline the
Dawid–Skene literature compares itself against." `manuscript/main.tex` lines 279–282.

**F2 (OPTIONAL FUTURE WORK).** §4.4's realized-ADS-range sentence ("ranges from 0.44 to 0.93,
structurally capped below approximately 0.91... the region... at or above roughly 0.93 was never
reachable") is numerically self-consistent on inspection (mean ceiling ~0.91 vs. individual-seed max
~0.926≈0.93) but reads as contradictory on first pass to a reader who has not already internalized
the mean-vs-individual-seed distinction. This exact wording is inherited verbatim from
`CONTRIBUTION_LOCK.md` §8 and `PAPER_CONTRACT.md` §6/§7, so it is not a manuscript-introduced drift —
flagging it here because E4 is exactly the phase where inherited-but-confusing wording from the
locked contract should surface, even though fixing it is a prose decision outside this audit's
mandate. `manuscript/main.tex` lines 636–640.

**F3 (REQUIRED NOW).** §4.2, line 600: the cross-company-alignment parameter (0.695) is introduced as
"the production-observed value" without the "cited from a confidential engagement, not independently
reproducible from this repository" qualifier that `PAPER_CONTRACT.md` §5 requires at **every**
appearance of a production number, and that every other production figure in this manuscript
(91.2%, 0.847, 0.964) does carry at its point of use. This is a concrete, checkable, narrow
compliance gap against the contract's own explicit rule, not a substantive scientific error — 0.695
is correctly used only as a fixed generator nuisance parameter, never as evidence — but the missing
qualifier is exactly the kind of omission the contract's blanket rule exists to prevent from
compounding silently across drafts. `manuscript/main.tex` line 600.

**F4 (REQUIRED NOW).** §1.1's framing of the production "R3 flip" states the rule "selected a
retrieval-based mechanism instead" (line 103) for the synthetic branch's 87.56% figure. The
production/synthetic architecture-decision code (`scripts/04_architecture_decision.py`, verified via
`r3_threshold_analysis.md`) actually names this outcome **EMBEDDING_PRIMARY** — an embedding-based
semantic classifier, structurally and terminologically distinct from Experiment 1's "retrieval"
mechanism, which §3.4 of this same manuscript explicitly and carefully defines as NOT an embedding
model ("We deliberately call this mechanism 'retrieval,' not 'embedding'... no embedding model was
trained, downloaded, or evaluated anywhere in this experiment"). Using "retrieval-based mechanism" in
§1.1 to describe what the production/synthetic decision procedure itself calls EMBEDDING_PRIMARY
creates an implicit terminological bridge between the motivating case study and Experiment 1's
actually-tested mechanism that the manuscript's own Problem Setting section (§3.4) goes out of its
way to sever. A skeptical reviewer reading §1.1 in isolation could reasonably (and incorrectly)
conclude that the production R3 flip's "EMBEDDING_PRIMARY" outcome is the same mechanism Experiment 1
tests and reports 120/120 wins for — it is not; Experiment 1's retrieval mechanism was never run
against production data, and no embedding-based mechanism was tested in Experiment 1 at all. This is
a scope/terminology-precision issue, not a resurrected forbidden claim, but it works against the
manuscript's own stated discipline (§3.4) and should be tightened — e.g., "selected the
embedding-based mechanism (EMBEDDING_PRIMARY) instead — a different mechanism from the
lexical-similarity 'retrieval' this paper's Experiment 1 tests" or equivalent. `manuscript/main.tex`
lines 97–111 (§1.1) versus lines 533–547 (§3.4).

**F5 (OPTIONAL FUTURE WORK).** The manuscript's Reproducibility Statement scopes its reproduction
instructions ("`python scripts/experiments/exp1/run_final.py`") explicitly and correctly to "every
number in Section 5," but never names the separate script chain
(`00_generate_synthetic.py` → `03_5_dataset_intelligence.py` → `04_architecture_decision.py`) that
would let a reader reproduce the 87.56% synthetic-branch figure cited in §1.1. This is not a false
claim (the Reproducibility Statement never says §1.1's figures are covered) but is a completeness
gap: a motivated reader who wants to check the one number in this paper's Introduction that actually
is reproducible from this public repository has no signpost to find it. `manuscript/main.tex` lines
1484–1493 (Reproducibility Statement) versus lines 100–104 (§1.1).

**F6 (OPTIONAL FUTURE WORK, governance/process note, not a manuscript defect).** `PAPER_CONTRACT.md`
§2 row 9 and `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §1 (Introduction row) both still state the
synthetic-branch R3-flip figure as **"84.1%"** (the pre-A5-fix, `SUPERSEDED — DO NOT CITE` value per
`EVIDENCE_BASELINE.md` §3) rather than the canonical post-fix 87.56%. The manuscript itself correctly
uses 87.56% throughout (§1.1, and nowhere cites 84.1%) — so this superseded number did **not** leak
into the manuscript — but two of the governing Tier-2 evidence documents that are supposed to be the
manuscript's binding source of truth (`PAPER_CONTRACT.md`'s own evidence table, and the claim-map
built specifically to prevent exactly this kind of staleness) still carry the stale figure,
uncorrected, as of this audit. This is worth flagging because it is precisely the failure mode
`EVIDENCE_BASELINE.md`'s own hierarchy rule (§4) warns about — stale prose surviving in a supposedly
authoritative document — except here it survived in a document one level above where the hierarchy
rule usually catches it. Recommend correcting `PAPER_CONTRACT.md` §2 row 9 and
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`'s Introduction-row figure to 87.56% so future drafting sessions
that consult the contract (rather than the manuscript) do not inherit the wrong number. Not a
manuscript fix — a contract/evidence-map fix, outside this audit's edit permissions.
`research/PAPER_CONTRACT.md` §2 row 9; `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §1 Introduction
table, row 3.

---

## Independent E4 Verdict

**🟡 YELLOW — substantial but non-fatal revisions required.**

Justification: the manuscript's evidentiary core (Experiment 1's design, statistics, and the
accuracy-vs-ranking distinction) passed a sixth independent verification pass in this audit with zero
discrepancies found in the headline numbers, zero resurrected forbidden claims (Part E: no novelty
inflation found across ten checked concepts), zero production numbers used as statistical evidence,
and a fully reproducible experimental core (Part I). This is a genuinely strong, carefully-hedged
draft — the "we do not claim X" discipline in Related Work and the explicit accuracy/ranking
separation throughout Results and Discussion are executed consistently, not just in the sections most
likely to be scrutinized.

Against that, this pass surfaced two REQUIRED NOW findings that are concrete, narrow, and
inexpensive to fix but do matter: (F3) one production-sourced number appears without its mandated
confidentiality/reproducibility qualifier, a direct, checkable violation of `PAPER_CONTRACT.md` §5's
own "every appearance" rule; and (F4) a terminology substitution in the Introduction's motivating
case study ("retrieval-based mechanism" for what the underlying code calls EMBEDDING_PRIMARY) that
quietly undercuts the very distinction the manuscript's own Problem Setting section (§3.4) is careful
to draw, creating a risk that a reader conflates the case study's untested embedding-based outcome
with Experiment 1's actually-tested, actually-winning lexical-retrieval mechanism. Neither finding
touches the locked contribution, the statistics, or the falsification framing — both are
Introduction/Problem-Setting-section precision issues, not integrity violations — which is why this
is YELLOW rather than ORANGE. Three OPTIONAL FUTURE WORK notes (F1, F2, F5) and one
governance/process note about the contract documents themselves (F6, not the manuscript) round out
the findings.

**Required changes before this section of E4 would recommend GREEN:**

1. Add the standard confidentiality/reproducibility qualifier to §4.2's cross-company-alignment
   sentence (`manuscript/main.tex` line 600), matching the pattern already used for every other
   production figure in the manuscript.
2. Revise §1.1's "the same rule selected a retrieval-based mechanism instead" (line 103) to name the
   actual decision-procedure output (EMBEDDING_PRIMARY) and explicitly note it is a different
   mechanism from the "retrieval" this paper's Experiment 1 tests, consistent with §3.4's own
   discipline about not conflating the two.

Both are small, targeted prose edits (not manuscript-architecture changes, not new evidence, not new
citations) and do not require revisiting any locked number, contribution formulation, or statistical
result.
