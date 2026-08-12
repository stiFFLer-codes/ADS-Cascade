# Paper Contract — Permanent Anti-Drift Contract for the ADS-Cascade Manuscript

> **Status: binding for all of Phase E.** This document governs every subsequent manuscript-drafting
> session (E1 onward). It is derived exclusively from already-locked evidence — `CONTRIBUTION_LOCK.md`,
> `contribution_lock.csv`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PHASE_E_PLAN.md`, the Phase B
> literature ledger, the frozen Experiment 1 evidence, and the D.1 post-hoc analysis — and invents
> nothing new. Where this contract and any other document conflict, **this contract wins for
> drafting decisions**, except where it conflicts with `CONTRIBUTION_LOCK.md` itself, in which case
> `CONTRIBUTION_LOCK.md` is re-consulted and this contract is corrected, not overridden silently.
> Does not modify `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`, any frozen evidence, or any
> other file.

---

## 1. North star

Complete a defensible first manuscript draft → adversarial manuscript audit → reproducibility/
public-release package → arXiv preprint → (later, only if warranted) adapt to a journal. Not an
indefinitely expanding research program (`RESEARCH_GPS.md`'s own north star, restated here so the
manuscript contract carries it independently of that file's freshness).

---

## 2. Claims the paper MAY make

Every claim below traces to a named evidence source and is bounded to the scope stated. No claim
here may be drafted more strongly than its scope allows — if a sentence in the manuscript needs to
say more than a row below permits, the sentence is wrong, not the row.

| # | Claim (exact scope) | Evidence source | Scope boundary |
|---|---|---|---|
| 1 | The ADS formula: for product $p$ with historical account counts $c_1,\dots,c_k$, $\text{ADS}(p)=\max_i c_i/\sum_i c_i$, is a descriptive definition, not a novelty claim. | `TECHNICAL_REPORT.md` §2.2; `CONTRIBUTION_LOCK.md` §3 (C1) | Must be paired with the cluster-purity/majority-vote-agreement equivalence statement wherever introduced — see §3 row 1. |
| 2 | H1 (revised) was pre-registered before Experiment 1's data existed, with falsification criteria fixed in advance. | `EXPERIMENT_1_REDESIGN_REVIEW.md` §2, §18 | Procedural fact only; do not imply the *result* was known in advance. |
| 3 | **(6a, supported)** In this synthetic generator, realized ADS is strongly predictive of each mechanism's own accuracy (exact-match rules and fuzzy retrieval alike): Pearson r ≈ 0.909–0.959 (rules) / 0.948–0.955 (retrieval), both lexical conditions. | `CONTRIBUTION_LOCK.md` §4, §6a; independently re-derived, `AUDIT_REPORT.md` | Correlational; this synthetic generator only; both correlations must be reported together, never just the stronger one. |
| 4 | **(6b, the limiting/negative finding)** ADS is **not** predictive of which of the two mechanisms outperforms the other: retrieval wins 120/120 VARIED conditions and the two mechanisms tie (within δ=0.02) in 120/120 CLEAN conditions, unconditional on realized ADS across its full observed range (0.44–0.93). | `CONTRIBUTION_LOCK.md` §4, §6b; `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §6 | The 120/120 + 120/120 split is exhaustive (not sampled) over the 240 frozen conditions of this one experiment. |
| 5 | R3's agreement with the empirical winner is 100% (32/32) in the realized 0.70–0.90 ADS band and 0% (0/18) in the realized ≥0.90 band; overall 64.0% (32/50), Wilson 95% CI [50.1%, 75.9%], barely excluding chance (p=0.065). | `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §4–5; `CONTRIBUTION_LOCK.md` §2 step 7 | This exact banding, these exact numbers, no rounding that changes the qualitative picture (e.g. never round 0/18 up to "rare disagreement"). |
| 6 | Causal account: ADS is computed on the stable `product_code`, structurally blind to the perturbable surface string, which is why it cannot track the noise-driven ranking. | `CONTRIBUTION_LOCK.md` §2 step 8; `EXPERIMENT_1_DATA_DICTIONARY.md` | INFERRED from exhaustive code inspection and matching, not a second independently-designed confirmatory experiment — must be phrased with that epistemic weight, never as "we prove" or "we demonstrate causally." |
| 7 | **Synthesis:** historical decision consistency is informative about classification-mechanism *difficulty*, not about mechanism *ranking*, when — as observed here — ranking is governed by a representation-stability property the consistency signal does not observe. | `CONTRIBUTION_LOCK.md` §6, exact wording to reuse | This is the paper's one central claim. It is a refinement of, not a confirmation of, the original "historical consistency selects the right architecture" hypothesis — never state it as a confirmation. |
| 8 | This refines, rather than contradicts, the algorithm-selection/meta-learning lineage (Rice 1976; Smith-Miles 2009) by identifying a specific failure mode of a single-feature, label-consistency-only selector. | `CONTRIBUTION_LOCK.md` §5 row 2 | Positioning claim only — never "this literature failed to anticipate X," always "this narrower instance was not directly anticipated," per the literature ledger's own hedge. |
| 9 | The production system's single-run "R3 flip" (RULES_FIRST at 91.2% vs. EMBEDDING_PRIMARY at 84.1%) motivated this research question. | `METHODOLOGY.md` real-vs-synthetic table; `r3_threshold_analysis.md` | CASE_STUDY — two single data points, cited as motivation, never as statistical evidence for §6a/§6b. |
| 10 | Canonical production aggregate statistics (91.2% deterministic, weighted ADS 0.847, unweighted 0.964, cross-company consistency 0.695, etc.) may be cited as motivating/contextual figures. | `METHODOLOGY.md` public/confidential table | Cited from a confidential engagement, not independently reproducible from this repository — every appearance must carry that qualifier (§5 of this contract). |
| 11 | The Related Work positioning statements in `citation_ledger.csv` (VERIFIED / VERIFIED-INDUSTRY / VERIFIED-PREPRINT rows only, matching §4 tier 3's exact set). | `research/literature/citation_ledger.csv` | Industry-source rows (B8-04/05/06) must be labeled as not peer-reviewed wherever cited; preprint rows (e.g. B3-03) must be labeled as not yet peer-reviewed wherever cited. |

---

## 3. Claims the paper MUST NOT make

Reproduced in full from `CONTRIBUTION_LOCK.md` §7 and the Phase B/C stress test — this is the
manuscript's negative checklist. Any drafting session that finds a sentence resembling one of these
must rewrite it before continuing, not footnote it.

| # | Forbidden claim | Why rejected | Locked in |
|---|---|---|---|
| 1 | "ADS is a novel metric" | Mathematically identical to cluster purity (Manning et al. 2008; Amigó et al. 2009) and the majority-vote-agreement baseline (Dawid & Skene 1979 lineage) — C1, REJECTED | `CONTRIBUTION_LOCK.md` §3, §7; `contribution_lock.csv` row C1 |
| 2 | "ADS universally selects the correct architecture" | Directly falsified, 0/18 exceptionless disagreement in the realized ≥0.90 band under lexical noise | §7 |
| 3 | "Design-time architecture selection from historical consistency" as a general, unprecedented pattern (C2) | CHALLENGED by Rice 1976, Barbudo et al. 2023, Idreos & Kraska 2019 | `contribution_lock.csv` row C2 |
| 4 | "The cascade architecture (Part 1 + Part 2 combined) is novel" | C6, WEAK — no baseline comparison (Experiment 2) was ever run | `contribution_lock.csv` row C6 |
| 5 | "The runtime multi-tier confidence cascade is a novel general pattern" (C3) | CHALLENGED by FrugalGPT, reject-option/selective-classification lineage, LLM-routing literature | `contribution_lock.csv` row C3 |
| 6 | "The method generalizes to enterprise AI broadly" | Out of scope per the project's own settled positioning; bounded explicitly by four preconditions (repeated historical decisions, observable labels, measurable consistency, sufficient historical coverage) | `STATE.md`; §7 |
| 7 | "Production data independently validates the synthetic finding" | Production never ran a lexical-noise sweep; only two single-run data points feed the R3-flip narrative, and production ADS figures remain pre-A5-fix, "likely understated, unverified" | §7 |
| 8 | "The experiment proves that consistency alone is sufficient for architecture selection" | The opposite of what Experiment 1 + D.1 show | §7 |
| 9 | "Higher ADS means rules is better" | Reversed under noise in this data — retrieval's advantage over rules *widens*, not narrows, as ADS increases under VARIED | §7 |
| 10 | "CLEAN implies the two mechanisms are equivalent in general" | CLEAN shows near-equivalence specifically absent lexical noise, for this generator only — not a general-equivalence claim | §7 |
| 11 | "The synthetic p_transform=0.3 perturbation represents real-world OCR/typo noise" | An unvalidated synthetic stand-in, not a measured noise model | §7 |
| 12 | "A design-time selector should account for representation stability" stated as demonstrated/built | The two-feature idea (Formulation #3) was never built or tested — explicitly NOT RECOMMENDED, named only as future work | `CONTRIBUTION_LOCK.md` §5 rows 3–4, §10 |
| 13 | "ADS predicts mechanism suitability" (unqualified — collapsing accuracy-prediction and ranking-prediction into one claim) | The two are empirically distinct: one holds (6a), one is falsified (6b); collapsing them is exactly the error this contract exists to prevent | `CONTRIBUTION_LOCK.md` §4 |
| 14 | Commercial vendors "typically ship a single learned classifier... chosen up front rather than derived from a measured determinism distribution" | Factually contradicted by B8-04 (Ken From Finance's public materials, which already describe a pre-deployment historical-consistency audit); currently still present, uncorrected, in `TECHNICAL_REPORT.md` §5 lines 289–291 | `CONTRIBUTION_LOCK.md` §7; `RESEARCH_AUDIT.md` F7/F8 |
| 15 | Any claim naming the ~55,394 mapping-count figure | UNRESOLVED, untraceable in this repository or its git history; 76,843 is the only canonical value | `mapping_count_provenance.md` |
| 16 | "This method is validated as effective for hybrid classification-system composition" (Formulation #4) | Explicitly named and rejected — this is precisely the claim five phases of audit (A–D.1) have progressively disproven | `CONTRIBUTION_LOCK.md` §5 row 4 |

---

## 4. Evidence hierarchy

When two sources disagree about a fact, number, or framing, resolve in this order — higher wins:

1. **Frozen experimental artifacts** — `data/outputs/experiments/exp1/final/final_condition_results.csv`
   and its companions (`final_summary.csv`, `final_bootstrap_results.csv`, `final_run_metadata.json`).
   These are the ground truth for every Experiment 1 number. Never re-derive a different number from
   a re-run — the run is frozen (`RESEARCH_GPS.md`'s DO NOT CHASE list, §9 of this contract).
2. **Verified research artifacts** — `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`,
   `EXPERIMENT_1_POSTHOC_ANALYSIS.md`, `AUDIT_REPORT.md`, `EVIDENCE_BASELINE.md`,
   `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` — documents that have already independently re-derived and
   verified numbers from tier 1, and recorded an auditor verdict.
3. **Literature ledger** — `research/literature/citation_ledger.csv`, restricted to `VERIFIED`/
   `VERIFIED-INDUSTRY`/`VERIFIED-PREPRINT` rows, plus the dedicated prior-art ledgers
   `research/literature/ads_metric_prior_art.md`/`.csv` (the source for the C1 equivalence claim —
   Manning et al. 2008; Amigó et al. 2009; Dawid & Skene 1979 lineage — §2 row 1 / §3 row 1's most
   load-bearing citation) and `research/literature/llm_advisory_prior_art.md`/`.csv`.
   `UNVERIFIED`/`UNVERIFIED-PARTIAL`/`NOT FOUND` rows may be mentioned only with their exact caveat
   attached, never cited as settled fact.
4. **Case-study production evidence** — `METHODOLOGY.md`'s real-vs-synthetic table, the R3-flip
   observation, `reports/phase1_final_report.md`. Motivating context only (§5 of this contract).
5. **Historical project prose** — `STATE.md`, `ROADMAP.md`, `RESEARCH_GPS.md`, `TECHNICAL_REPORT.md`,
   `README.md`. **Lowest authority.** These files can and do go stale (confirmed twice already this
   project: `RESEARCH_GPS.md`'s Gate 4 status lagging `CONTRIBUTION_LOCK.md`, and
   `TECHNICAL_REPORT.md` §3.2/§3.3/§5 still carrying superseded numbers and a contradicted sentence —
   `PHASE_E_AUDIT_REPORT.md` findings 1–2). **Stale historical prose must never override a verified
   artifact from tiers 1–3, even when the prose is more recent-sounding, longer, or more confidently
   worded than the artifact it contradicts.** If `TECHNICAL_REPORT.md` states a number that conflicts
   with `EVIDENCE_BASELINE.md`, `EVIDENCE_BASELINE.md` wins, and the manuscript should not inherit the
   stale number merely because it was convenient to copy from an existing document.

---

## 5. Production data rule

Production/client data is **motivation and case-study evidence only**. It may be cited in the
Introduction (to motivate the research question) and briefly in the Discussion (as a real-world
observation consistent with the finding) — never in the Results section, never as statistical
support for §6a/§6b, and never described as "validated," "confirmed," or "independently reproduced"
by any party outside the confidential engagement. Every appearance of a production number must carry
an explicit "cited from a confidential engagement, not independently reproducible from this
repository" qualifier, matching the existing pattern already established in `TECHNICAL_REPORT.md`
§3.1 and `PUBLIC_RELEASE_BOUNDARY.md`. No production data may enter the public arXiv source package
or be presented as something a reader could re-run (`PUBLIC_RELEASE_BOUNDARY.md` §3, tier "case-study
only / confidential"). This rule holds unless a future, explicit, separately-documented clearance
process authorizes specific production figures for public release — no such clearance exists today,
and none is assumed by this contract.

---

## 6. Generalization rule

Every experimental claim in the manuscript (i.e., every row in §2 sourced to Experiment 1) must
remain scoped to exactly:

- **The tested synthetic generator** — the Experiment 1 product-classification generator at 60–1,200
  product scale, one seeded RNG family, not an external population.
- **The tested mechanisms** — exact-match `rules_only` lookup vs. rapidfuzz-based `retrieval_only`
  fuzzy matching (cutoff=75). Not embeddings, not an LLM (excluded by design), not the shipped
  multi-tier production cascade.
- **The tested lexical perturbation** — `p_transform=0.3`, exactly five fixed transform types (case,
  punctuation, token-reorder, abbreviation, whitespace), pilot-tuned to a target corruption-share
  band, not derived from measured real-world OCR/typo error rates.
- **The tested factorial design** — 240 conditions = 20 seeds × 6 nominal-ADS targets × 2 lexical
  conditions (CLEAN/VARIED); realized-ADS range 0.44–0.93, structurally capped below ~0.91 by the
  fixed `CROSS_COMPANY_ALIGN=0.695` nuisance parameter — the "deep rules-first" region (≥0.93) was
  never reachable or tested.

No sentence may generalize beyond this scope by dropping a qualifier (e.g., writing "retrieval
outperforms rules under noise" without "in this generator, under this perturbation model" is a scope
violation even if the underlying number is correct). Any generalization beyond this scope belongs in
§8 Future Work, explicitly hedged as "not built, not tested here," never in Results or Discussion as
if demonstrated.

---

## 7. Numerical rule

Only canonical, verified values may enter the manuscript. Superseded values must never be copied,
even from an existing document that still contains them.

**Canonical (citable):**

- Synthetic (post-A5-fix): weighted ADS **0.9031**, unweighted ADS **0.9597**, deterministic-share
  **87.56%** (`EVIDENCE_BASELINE.md`).
- Experiment 1: overall agreement 32/50 = **64.0%**, Wilson CI **[50.14%, 75.86%]**, p=**0.0649**;
  band split **32/32 (100%)** at realized ADS 0.70–0.90, **0/18 (0%)** at realized ADS ≥0.90; Pearson
  r **0.909–0.959** (rules) / **0.948–0.955** (retrieval); winner constancy **120/120** VARIED
  (retrieval), **120/120** CLEAN (tie); realized-ADS range **0.44–0.93**; δ=**0.02**; retrieval
  cutoff=**75**; R3 thresholds **0.90/0.70**.
- Production (case-study, cited not reproduced): deterministic products **91.2%**, weighted ADS
  **0.847**, unweighted ADS **0.964**, cross-company consistency **0.695**, mapping count **76,843**.

**Superseded — must never be cited:**

- Pre-A5-fix synthetic figures: weighted ADS **0.8094**, unweighted ADS **0.9310**, deterministic-
  share **84.12%** (still present in `TECHNICAL_REPORT.md` §3.2/§3.3 as of this pass — a stale-prose
  case explicitly covered by §4's hierarchy rule; the manuscript draft must use the canonical figures
  above regardless of what `TECHNICAL_REPORT.md` currently shows).
- The **~55,394** mapping-count figure — UNRESOLVED, untraceable; only 76,843 is canonical
  (`mapping_count_provenance.md`).

Any new number that doesn't already appear in `CONTRIBUTION_LOCK.md`, `EVIDENCE_BASELINE.md`, or the
frozen Experiment 1 artifacts is not canonical by default — trace it to its source before drafting a
sentence around it, don't assume a number is safe because it "sounds right" or appears in prose
somewhere in the repo.

---

## 8. Contribution rule

**Formulation #2** (`CONTRIBUTION_LOCK.md` §6) is the current, locked contribution:

> **6a.** Realized ADS is strongly predictive of each mechanism's own accuracy.
> **6b.** ADS is not predictive of which mechanism outperforms the other; ranking is governed by a
> separately-manipulated representation-stability factor ADS cannot observe.
> **Synthesis.** Historical consistency is informative about difficulty, not ranking, in this
> experiment.

The manuscript must draft toward exactly this formulation — not Formulation #1 (too weak — omits the
positive §6a correlations), not Formulation #3 (too strong — implies a fix was designed and tested),
and never Formulation #4 (rejected outright). **Do not silently strengthen or broaden Formulation #2
during drafting.** A drafting session that finds itself wanting to add confidence, generality, or
prescriptive force to the contribution must stop and treat that impulse as a signal to re-read
`CONTRIBUTION_LOCK.md` §5's comparison table, not as a drafting improvement.

---

## 9. Experiment rule

**No new experiments during manuscript drafting.** Experiment 1 is closed (`RESEARCH_GPS.md`'s Gate
3, `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §14: "no residual uncertainty a new run would resolve").
Frozen parameters (δ=0.02, cutoff=75, thresholds 0.90/0.70, the generator, the perturbation model)
are not to be re-tuned, re-run, or extended.

**Exception:** if a genuine evidence gap is discovered that *blocks* a specific claim the paper
needs to make (not merely one that would make the paper more thorough or impressive), that gap must
be **escalated to the human author before any new experimental code is written or run** — not
resolved unilaterally mid-draft. "Blocks a claim required by the paper" means: without new evidence,
a section required by `PHASE_E_PLAN.md`'s structure cannot be written at all, not that an existing
section could be strengthened. Experiment 2 (C6 baseline comparison) and Experiment 3 (C5 feedback-
loop measurement) are named, known, and explicitly **not required** for the current, narrower,
locked contribution (`CONTRIBUTION_LOCK.md` §10) — their absence is not itself an escalation trigger.

---

## 10. Venue/template rule

Generic LaTeX `article` class first (`MANUSCRIPT_FORMAT_RESEARCH.md` §2.3). **Do not optimize the
manuscript around a specific journal's template, page limits, or house style before the first
complete draft (E3) exists.** Venue choice is explicitly deferred to `ROADMAP.md` Phase I
(post-arXiv-preprint) and is out of scope for every Phase E milestone through E8. If a specific
journal is proposed before E3, treat that as a distraction from the hard milestone, not as a
reason to restructure.

---

## 11. E3 definition — "FIRST COMPLETE DRAFT"

**E3 is reached when every section named in `PHASE_E_PLAN.md` §3.3 exists with:**

- Actual prose (not bullet-point outlines, not placeholder sentences) for every section: Introduction,
  Related Work, Problem Setting, Experimental Design, Results (all four subsections 5.1–5.4),
  Discussion, Limitations, Future Work, Conclusion.
- Citations wired in for every Related Work / positioning claim, resolving to real entries in
  `references.bib` (compiled from the VERIFIED subset of `citation_ledger.csv`).
- Table/figure **placeholders** present at minimum where `PHASE_E_PLAN.md` §Task 7 requires them
  (F1–F4, plus the F5/F8 tables) — a placeholder may be a draft-quality figure or an explicit
  `\includegraphics` reference to a not-yet-final image, but the slot must exist and be captioned.
- The actual Experiment 1 results reported, matching §2/§7 of this contract's numbers exactly.
- A Limitations section containing every item from `CONTRIBUTION_LOCK.md` §9, undiluted.
- A References section that compiles (even if not yet fully polished).
- **No section is a TODO stub standing in for substantive content.** A section header followed by
  "(to be written)" or a one-line summary where a full section is required does not satisfy E3.

**E3 does NOT require:**

- Perfect prose (awkward phrasing, repetition, or rough transitions are acceptable at E3 — that is
  what E4 is for).
- Final typography (spacing, exact table styling, font choices).
- Final journal formatting (per §10 of this contract — generic LaTeX is fine at E3 and likely fine
  indefinitely until a venue is chosen).
- Perfectly polished figures (draft-quality plots that convey the correct data are sufficient; final
  visual polish is not an E3 gate).

The distinction that matters: **E3 is about completeness and correctness of content, not quality of
presentation.** A complete draft with rough prose passes E3; a beautifully typeset draft missing a
Limitations section does not.

---

## 12. Phase E stop rule

**Once E3 is reached, drafting stops and the project enters audit mode (E4 → E5 → E6 → E7 → E8).**
Do not continue adding research, new analyses, new figures, or new sections simply because the draft
*could* be improved — improvement-seeking after E3 is scope creep against this contract's north star
(§1), which is a *complete* draft followed by *audit*, not an indefinitely polished one. Any
improvement identified after E3 either (a) is a required fix surfaced by the E4/E5/E6 audits, and
gets made then, in that context, or (b) is not required, and goes into Future Work (§8 of the
manuscript, §9 experiment-escalation path of this contract) rather than being drafted in. The
hard milestone is E3; everything after it is verification, not expansion.

---

## 13. Conflicts found while assembling this contract

None. Every claim, number, and rule above was cross-checked against `CONTRIBUTION_LOCK.md`,
`contribution_lock.csv`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PHASE_E_PLAN.md`, and the frozen
Experiment 1 evidence during drafting, and no internal disagreement was found between those source
documents. The two known, already-flagged staleness issues in `TECHNICAL_REPORT.md` (§5's
vendor-practice sentence; §3.2/§3.3's superseded synthetic figures) are not conflicts *within* the
locked-evidence set this contract is built from — they are exactly the kind of stale-historical-prose
case §4's hierarchy rule and §7's numerical rule are designed to override, and are recorded there
rather than treated as unresolved contradictions.
