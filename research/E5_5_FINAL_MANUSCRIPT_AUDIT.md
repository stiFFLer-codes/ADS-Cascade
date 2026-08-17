# E5.5 — Final Manuscript Polish + Holistic Audit

> Review pass only. This document reports findings; it does not itself edit `manuscript/main.tex`.
> No frozen evidence, no `research/PAPER_CONTRACT.md`, no `research/CONTRIBUTION_LOCK.md`, no
> `research/contribution_lock.csv`, and no `manuscript/references.bib` were modified to produce this
> report. Read in full: `manuscript/main.tex` (1,447 lines, complete, three passes), `manuscript/
> references.bib`, `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, `research/
> contribution_lock.csv`, `research/MANUSCRIPT_ARCHITECTURE.md`, `research/
> MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `research/E5_1_MANUSCRIPT_AUDIT.md`, `research/
> E5_2_CORRECTION_AUDIT.md`, `research/E5_3_CORRECTION_AUDIT.md`, `research/
> E5_4_FIGURE_GENERATION_AUDIT.md`.

---

## 1. Reader-journey assessment

Read `main.tex` start to finish as a first-time reader, then answered the ten questions from the
task brief:

1. **What question does the reader think the paper is answering after the Introduction?** Exactly
   the intended one: "can historical decision consistency, measured before deployment, select
   between qualitatively different classification mechanisms?" §1.2 states this in one sentence, and
   §1.3/§1.4 immediately preview that the answer splits into two different sub-claims (accuracy vs.
   ranking). A reader cannot walk away from the Introduction thinking this is a "does ADS work"
   yes/no paper — the two-part structure is set up before any result is given.
2. **What do they think the contribution is after Related Work?** Correctly narrowed: not a new
   metric (§2.1 states this in the first paragraph, paired with the cluster-purity/majority-vote
   citation in the same sentence, per the contract's requirement), not a new architecture-selection
   pattern in general (§2.2), and the Table T2 positioning table gives a reader who knows this
   literature a fast, honest "what's the delta" summary. No row overclaims a gap.
3. **Do Methods make the experiment reconstructible?** Yes. §4 gives generator scale, the six nominal
   targets, the CLEAN/VARIED perturbation model and its five transform types, the retrieval cutoff
   calibration procedure, the seed list, the train/test separation logic, the winner/tie definition
   (Equation 2) and its δ=0.02 margin, and the R3 threshold rule — in that order, before any result.
   A reader who wanted to re-run this could do so from §4 alone plus the Reproducibility Statement's
   one command.
4. **Does Results make the core finding obvious?** Yes, and the ordering is doing real work: §5.1
   (completeness) → §5.2 (accuracy correlation, 6a) → §5.3 (ranking constancy, 6b, the causal
   groundwork) → §5.4 (the headline band-agreement finding, 32/32 vs 0/18) → §5.5 (the mechanistic
   widening-gap table) → §5.6 (statistics) → §5.7 (summary). The flat 64.0% aggregate is deliberately
   introduced only after the band structure and is explicitly labeled a number that "obscures the
   structure just shown" (§5.4) — this is the single most important rhetorical move in the paper and
   it lands correctly.
5. **Does Discussion explain the surprising result?** Yes — §6.4 ("Mechanistic Explanation:
   Representation Stability") gives the ADS-is-blind-to-surface-form account, correctly hedged as
   INFERRED/post-hoc rather than a second confirmatory experiment, and §6.6 states four explicit
   non-inferences a reader might otherwise draw.
6. **Does Conclusion answer the original research question directly?** Yes: "It does not predict
   which mechanism wins... The main lesson is that historical consistency is informative about
   mechanism difficulty, not mechanism ranking..." directly closes the loop opened in §1.2, using
   almost the same vocabulary the question was originally posed in.
7. **Where does the reader have to work unnecessarily hard?** Two places, both minor:
   - §5.4's two framings (per-row realized-ADS band: 32/32, 0/18; by-nominal-target: 30/30, 2/20)
     are introduced in the same paragraph with a "these two framings differ because..." explanation
     that is accurate but dense on first read — a reader has to hold four numbers and two binning
     rules in their head simultaneously. The explanation is necessary (it is exactly what prevents
     the p-value misattribution the contract forbids) but could be one sentence shorter.
   - §1.1's opening paragraph packs the production motivation, the EMBEDDING_PRIMARY disambiguation,
     the "cited not evidence" caveat, and the "both figures near the threshold" observation into one
     11-line paragraph. All four pieces are necessary and none is redundant, but it is the single
     densest paragraph in the paper and is also the very first thing a reader encounters.
8. **Where could wording accidentally imply a stronger claim?** Nothing found on this full read that
   isn't already correctly hedged in the same sentence or the immediately adjacent one (see Section 13
   below, the forbidden-claim sweep, for the exhaustive term-by-term check). The closest candidates —
   every "governed by" instance, every "novel"/"validated"/"significant" occurrence — all carry an
   inline scope qualifier or are a correct negation.
9. **What is repeated unnecessarily?** The "cited from a confidential engagement, not independently
   reproducible from this repository" qualifier appears (correctly, by design per
   `PAPER_CONTRACT.md` §5, "every appearance... must carry that qualifier") at every production-number
   mention: §1.1, §6.2, §7.4. This is required repetition, not accidental bloat — removing any one
   instance would let a reader who starts at that section treat the number as evidence. Genuinely
   unnecessary repetition was not found: the four-preconditions list (§1.2) and the accuracy/ranking
   distinction (§3.4, §5.2/§5.3 handoff, §6.1) each appear once as a full statement and are referenced,
   not restated, elsewhere.
10. **What is missing that a skeptical reader needs?** One real gap, not a scientific one: the author
    block (`\author{TODO: Author Name \\ TODO: Affiliation... \\ TODO: ORCID iD}`) and
    `\date{TODO: submission date}` are still literal placeholders (lines 47, 52). This is a known,
    already-flagged, deliberately-deferred human decision (`research/MANUSCRIPT_ARCHITECTURE.md`
    §14 item 4), not an E5.5 defect — noted here only because a skeptical reader opening the PDF
    would see it immediately. No content gap was found in the scientific argument itself.

**Overall:** the manuscript already reads as a coherent, single-argument paper. The reader-journey
walk did not surface a structural problem — only the two density notes in item 7 and the pre-existing
placeholder metadata in item 10.

---

## 2. Title assessment

Current title: *"Historical Consistency Predicts Mechanism Accuracy, Not Mechanism Ranking: Evidence
from a Controlled Synthetic Study"* (line 39-40) — Candidate #1 of the five ranked in
`research/MANUSCRIPT_ARCHITECTURE.md` §1, with "classifier" swapped to "mechanism" per the in-file
title-decision comment (lines 17-22), consistent with the rest of the paper's vocabulary (rules is an
exact-match lookup, not a trained classifier).

Checked against the four required properties:
- **Accurate:** states both halves of Formulation #2 (6a positive, 6b negative) without a reader
  needing to continue past a colon to find the qualifier.
- **Interesting:** the accuracy/ranking split is itself the paper's surprising fact; leading with it
  is a stronger hook than a generic "we study X" title.
- **Specific enough to be defensible:** "Evidence from a Controlled Synthetic Study" pre-empts any
  implied production validation before a reader reaches the abstract.
- **Not broader than the evidence:** no forbidden term (see Section 13) appears in the title.

**No change proposed.** This is exactly the recommended candidate from the E1 architecture pass, and
this read-through found no reason to reopen that decision.

---

## 3. Abstract assessment

Read against `research/MANUSCRIPT_ARCHITECTURE.md` §2's seven required elements, in order: Problem
(line 59-61) → Research question (61-63) → Method (63-67, pre-registered 240-condition factorial,
20×6×2) → Core result, both halves (67-74, correlation then the 100%/0% band split) → Contribution/
interpretation (74-80, the "should not be trusted... without also accounting for representation
stability" synthesis, explicitly future-tense/not-built) → Scope limitation (75-77, "one synthetic
generator, one lexical-perturbation model, one motivating (non-evidentiary) production case study").
All seven present, in the specified order, nothing extra.

Checked against the four forbidden abstract patterns:
- Does **not** call ADS a novel metric (no mention of ADS's novelty status at all in the abstract —
  correct; that discussion belongs in §2.1, not the abstract).
- Does **not** imply ADS reliably selects mechanisms — the abstract's own words are "it does not
  predict which mechanism wins," the negative half stated as plainly as the positive half.
- Does **not** present the production case study as validation — the production case study is not
  mentioned in the abstract at all (correct per `MANUSCRIPT_ARCHITECTURE.md` §2's numbers table,
  which excludes production figures from the abstract entirely).
- Does **not** hide the partial H1 result — "This finding is scoped to one synthetic generator..."
  and the closing "a direction for future work, not something built or tested here" both keep the
  result bounded; H1's exact PARTIALLY_SUPPORTED label is not named by that phrase in the abstract,
  but the content of a partial result (predicts accuracy, doesn't predict ranking) is fully present.

Per `MANUSCRIPT_ARCHITECTURE.md` §2's own numbers table: the flat 64.0%/Wilson-CI/p-value are
correctly **absent** from the abstract (reserved for the body); the 100%/0% band contrast and the
r>0.9 correlation are correctly **present**, each as one compressed statement, not the full per-
mechanism/per-condition breakdown. No change proposed.

---

## 4. Introduction assessment

§1.1 (motivation) → §1.2 (research question + four preconditions) → §1.3 (experimental approach +
the two-part-finding framing) → §1.4 (contribution statement + roadmap). All four required elements
from the task brief present: motivation, gap positioning (deferred to §2 by design, correctly
signposted "Section 2 develops this positioning fully"), research question, why it matters (the four
preconditions), the accuracy/ranking distinction (stated explicitly in §1.3, "these are two different
claims... this paper never merges them"), synthetic-experiment scope (§1.3's second paragraph), and
contribution statement (§1.4, near-verbatim `CONTRIBUTION_LOCK.md` §6 wording).

No repetition found that reads as leftover draft-stage duplication — §1.1's caveat sentence
("neither run measured whether the mechanism it selected actually performed best, and the production
figures... are... not independently reproducible") and §1.4's contribution statement do not restate
each other; they operate at different levels (motivating anecdote vs. formal finding). Necessary
caveats (production non-evidentiary status, EMBEDDING_PRIMARY disambiguation, four preconditions) are
all present and none read as prunable. The one density note from Section 1 item 7 above (§1.1's
first paragraph) is an optional tightening candidate, not a required fix — see Section 16/17.

---

## 5. Related-work assessment

Checked each of the six brief items against §2's four subsections and Table T2:

- **Literature families correctly positioned:** cluster purity/majority-vote agreement (§2.1),
  Algorithm Selection/meta-learning/AutoML/self-designed-systems (§2.2), reject-option/learning-to-
  defer/model-cascades (§2.3), domain-specific practice (§2.4) — matches
  `research/MANUSCRIPT_ARCHITECTURE.md` §10's eight-row table exactly, including the two families
  merged into §2.3 that the architecture table lists as separate rows (reject-option and learning-to-
  defer) — a presentation choice, not a missing family.
- **ADS's mathematical prior art acknowledged:** §2.1's first paragraph, in the same paragraph as the
  metric's own introduction — not deferred to a footnote.
- **Algorithm Selection / workflow composition terminology accurate:** §2.2 correctly attributes Rice
  1976 to per-instance/per-dataset algorithm selection, Smith-Miles 2009 to the meta-learning
  unification, and Barbudo et al. 2023 to the AutoML-workflow-composition reframing — matches each
  citation's actual documented contribution per `citation_ledger.csv`.
- **Selective classification / learning-to-defer / model cascades not falsely claimed as new:** every
  paragraph in §2.3 opens with an explicit "We make no claim that..." / "We do not claim that..."
  sentence before describing the prior art — confirmed by direct read, not merely by the earlier
  grep sweep (Section 13 below).
- **LLM re-ranking prior art correctly positioned:** RankGPT (§2.3, line 374) is cited as establishing
  that LLM re-ranking over a pre-fetched candidate list is "commodity information-retrieval technique"
  — correctly scoped, and the E5.2 correction pass's internal-comment fix (pointing the evidence
  anchor at `llm_advisory_prior_art.csv` G2-01 instead of the wrong ledger row) is confirmed still in
  place and correct.
- **Industry sources labeled non-peer-reviewed:** §2.4's three industry citations
  (`kenfromfinance2025`, `peakflo2025`, `ramp2025`) carry the "(accounts-payable automation vendors,
  not peer-reviewed)" qualifier at the group citation and a second, individual "(not peer-reviewed)"
  qualifier at the standalone `kenfromfinance2025` citation — confirmed present, matches
  `PAPER_CONTRACT.md` §2 row 11's "wherever cited" requirement, and matches the E5.2 audit's own
  verification of the same point.

**No literature addition proposed** — no existing citation was found demonstrably wrong on this pass
(the one prior wrong-pointer defect, the RankGPT internal-comment misattribution, was already found
and fixed at E5.2 and is confirmed still fixed).

---

## 6. Methods / problem-setting assessment

Checked reconstructibility against the brief's eleven-item checklist, each traced to its exact
location: synthetic generator (§4.2, 60 companies × 1,200 products) — train/test split (§4.6,
"exclusively on that condition's train... test rows," verified in code per that paragraph's own
claim) — realized ADS (§3.2 defines ADS, §4.3 defines *realized* ADS as the actual Section-5
independent variable, explicitly distinguished from the nominal target) — six target regions (§4.2,
the exact six values listed) — CLEAN/VARIED (§4.4, both conditions' construction described in full,
including the exact five transform types and the $P_{\mathrm{TRANSFORM}}=0.3$ calibration provenance)
— 20 seeds (§4.6, the exact seed range) — rules mechanism (§3.3, exact-match, company-scoped then
global fallback, no confidence threshold) — retrieval mechanism (§3.3, rapidfuzz WRatio, cutoff
calibrated separately per §4.5) — retrieval cutoff (§4.5, the exact calibration procedure and
candidate-cutoff set) — R3 thresholds (§4.7, the exact 0.90/0.70 boundaries) — paired-bootstrap/
winner rule (§4.6, Equation 2, 2,000 resamples, δ=0.02) — LLM exclusion (§1.3 first, then §4.1's H1
statement names the excluded band, and §7.3 restates the exclusion as a limitation) — all present,
all before any result is reported.

**The lexical-similarity-retrieval ≠ EMBEDDING_PRIMARY distinction, specifically checked:** §1.1
states it explicitly on first mention ("a different mechanism from the lexical-similarity retrieval
mechanism this paper's Experiment 1 tests... no embedding-based mechanism is evaluated anywhere in
this paper"), and §3.3 restates it a second time, independently, with the strongest possible wording
("We deliberately call this mechanism 'retrieval,' not 'embedding'... no embedding model was trained,
downloaded, or evaluated anywhere in this experiment, and describing it as 'embedding-primary' would
misstate what was actually tested"). This distinction is stated twice, at two points a reader might
enter the paper from, and never blurred anywhere else in the document (confirmed by the full-file
"embedding" grep in Section 13).

---

## 7. Results assessment

This is the section the task brief calls most important; verified line-by-line against the frozen CSV
one more time (not merely re-trusted from the E5.4 pass):

1. **6a stated as association with individual mechanism accuracy, not ranking:** §5.2's own text says
   this explicitly — "This is a correlational finding about each mechanism's own performance level --
   it says nothing yet about which mechanism performs better than the other."
2. **6a does not translate into ranking prediction:** §5.3's opening sentence states this as the
   section's thesis ("Realized ADS does not predict which mechanism wins").
3. **Central finding is regime divergence, not the aggregate:** confirmed structurally — §5.4 reports
   the band split (32/32, 0/18) as its first and primary content, then explicitly introduces the flat
   aggregate afterward with "Only after this band structure do we report the flat aggregate" and calls
   it "a near-cancellation of two individually far more decisive, opposite patterns."
4. **64% is secondary context:** confirmed — see item 3; also stated a second time in §5.6 ("Both
   individual by-nominal-target bands are far more statistically significant than the flat aggregate").
5. **32/32 and 0/18 use realized-ADS bands (not nominal target):** confirmed — §5.4's own text: "Binned
   by each row's own realized ADS against R3's own thresholds -- the primary framing... R3 agrees...
   in 100% (32 of 32)... and in 0% (0 of 18)..." explicitly labeled "the primary framing."
6. **30/30 and 2/20 p-values belong only to the nominal-target framing:** confirmed at three
   independent points that must all agree, and do: (a) §5.4's prose introduces the by-target framing
   as "a secondary, also valid framing" with its own 30/30 and 2/20 counts; (b) §5.6 attaches
   $p=1.9\times10^{-9}$ to "the 30/30 retrieval-region band" and $p=4.0\times10^{-4}$ to "the 2/20
   rules-region band" by name, then explicitly states the per-row bands "are not independently paired
   with a frozen p-value anywhere in this paper's evidence base"; (c) Table T4's own caption states
   "The sharper, exceptionless per-row realized-ADS-band counts (32/32, 0/18) are reported in
   Section~5.4; no independently frozen $p$-value exists for those exact counts, so none is stated
   here" and the table body itself pairs each p-value only with its own by-target row (30/30 → 1.9e-9;
   2/20 → 4.0e-4), never with 32/32 or 0/18. **No p-value reattachment found anywhere in the
   manuscript** — re-verified independently this pass (Section 12 below), not merely carried forward
   from the E3-audit's earlier finding-and-fix on this exact issue (recorded in Table T4's own
   in-file comment, lines 1035-1044).

**Figures/tables checked against the frozen CSV directly** (re-verification, not reuse of E5.4's
numbers): re-ran `python scripts/experiments/exp1/analyze_posthoc.py --demo` this pass (see Section
14) and re-confirmed 32/50, the Wilson CI, and p=0.0649 reproduce exactly; spot-checked Table T5's six
cells (realized-ADS band × lexical → rules acc / retrieval acc / gap) against
`EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5, matching the same source `E5_1_MANUSCRIPT_AUDIT.md` already
verified — unchanged since that pass (confirmed no diff to Results between then and now via `git log
-p` scope, since neither E5.2, E5.3, nor E5.4 touched Results).

---

## 8. Discussion assessment

Checked against the brief's eight questions, each mapped to its subsection: what did we learn (§6.1,
the synthesis sentence, near-verbatim `CONTRIBUTION_LOCK.md` §6) — why did H1 partially fail (§6.3,
both the "what it got right" and "what it got wrong" halves stated explicitly, including the
"precisely there that the rule disagrees... in every single one of 18 tested conditions" framing of
the ≥0.90-band failure as maximally embarrassing for the rule, not softened) — why the failure is
informative (§6.4's mechanistic account plus §6.5's "refines, rather than contradicts" positioning) —
what ADS captures/fails to capture (§6.1's difficulty-vs-ranking split, restated) — what representation
stability contributes (§6.4's widening-gap asymmetry, explicitly scoped to "this specific perturbation
model and this specific retrieval implementation... not a claim about fuzzy or embedding-based
retrieval in general") — what practitioners should NOT infer (§6.6, four explicit non-inferences,
each independently checked in Section 13's sweep) — future direction (§6.6's closing paragraph,
correctly hedged "no pseudocode, no proposed threshold values, and no partial results, because none
exists").

**Causal-interpretation scoping, specifically checked:** §6.4 states the representation-stability
account is "inferred from exhaustive but post-hoc inspection of the frozen data and the generator's
code, not... the result of a second, independently designed confirmatory experiment" — this epistemic
hedge is present at the account's introduction, not only in Limitations, so a reader encountering the
causal claim for the first time sees the hedge immediately, not several sections later.

---

## 9. Limitations assessment

§7 leads with §7.1 "H1 Only Partially Supported" (confirmed first subsection, matches the task
brief's explicit instruction and the E5.1 pass's intentional reorder). All eight brief-required items
present: synthetic generator (§7.2) — lexical perturbation model (§7.2) — limited mechanism family
(§7.3, "Only exact-match rules and rapidfuzz-based retrieval were compared -- not embedding-based
retrieval, and not the shipped multi-tier production cascade") — single domain/evidence lineage (§7.3
first sentence) — no universal-selector claim (§7.5, "This paper makes no deployment or generalization
claim") — production evidence confidential (§7.4, with the specific "likely understated and
unverified" qualifier repeated) — no claim ADS alone suffices in all settings (§7.5's closing
sentence, and reinforced by §6.6's four non-inferences). Nothing found softened toward a strength
("...though this suggests..." pattern, explicitly checked for and not found anywhere in §7).

---

## 10. Conclusion assessment

§9 (lines 1387-1403) directly restates the research question and answers it in the same paragraph:
"tested... whether historical decision consistency predicts which of two classification mechanisms...
should be selected... Realized historical consistency strongly predicts each mechanism's own
accuracy. It does not predict which mechanism wins... H1 overall is only partially supported, not
confirmed." This matches the brief's required takeaway almost verbatim: the paper's own final
sentence-equivalent is "historical consistency is informative about mechanism difficulty, not
mechanism ranking, when... ranking is governed by a representation-stability property the consistency
signal does not observe" — the same content the brief specifies the reader should leave with, not the
"ADS solved architecture selection" framing the brief prohibits. The Conclusion introduces **no new
claim** not already made earlier in the paper (checked line-by-line against §5/§6's content) — this
was flagged in `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §1 as the section with the highest claim-inflation
risk, and this read found no inflation.

---

## 11. Figure/table consistency assessment

All four figures and all four tables re-inspected against source, caption, terminology, and
surrounding prose (figures re-viewed as rendered PDFs this pass, not only as generation code):

- **F1** (design flow, `fig:f1`): static schematic, caption matches content, no data-fidelity claim
  to check.
- **F2** (`fig:f2`, ADS vs. accuracy): caption reads "visualizing the Section 5.2 correlations
  directly" — accuracy-focused, as required; confirmed the figure plots two accuracy series with no
  "winner" annotation, ranking left to F3/F4 as designed.
- **F3** (`fig:f3`, agreement by band): caption states "100% (32/32) in the 0.70–0.90 band versus 0%
  (0/18) in the $\geq0.90$ band" — matches the rendered figure exactly: `<0.70` = a hatched box
  labeled "N/A (R3 excludes this band)" (not a 0% bar), `0.70`–`0.90` = a solid bar labeled "32/32",
  `\geq0.90` = a solid bar at 0% labeled "0/18" — re-confirmed by direct visual inspection this pass
  (Section 14). The caption never mentions a percentage for the `<0.70` band, consistent with the
  figure itself.
- **F4** (`fig:f4`, ranking constancy): caption states "the rules-minus-retrieval accuracy difference
  never crosses zero within a lexical condition, regardless of realized ADS" — confirmed
  ranking-focused, matches the rendered figure (CLEAN cluster at/near zero, VARIED cluster
  consistently below zero across the full ADS range, gap widening at higher ADS).
- **Table T2** (Related Work positioning): checked against Section 5 above — accurate.
- **Table T3** (experimental configuration): checked against §4's prose — all values match (six
  targets, CLEAN/VARIED, 20 seeds, cutoff 75, R3 thresholds, δ=0.02/2,000 resamples/α=0.05, 240 total).
- **Table T4** (main results): checked in Section 7 above — p-value pairing correct, no reattachment.
- **Table T5** (mechanism-winner behavior by band): checked in Section 7 above — matches
  `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5, and the widening-gap numbers it reports ($-0.137$ to
  $-0.185$ under VARIED) are the same numbers §6.4's mechanistic-account prose cites.

No figure or table required a change on this pass. This reconfirms, independently, the E5.4 checkpoint
already committed at `5dbec5c`.

---

## 12. Numerical integrity

Every protected number from the task brief's list was grepped directly against the current
`manuscript/main.tex` and found present at its expected location(s), with no altered value:

`32/50` (§5.4/T4), `64.0%` (§5.4/T4/§6.3, four occurrences), Wilson CI `[50.14%, 75.86%]` (§5.4/T4),
`p=0.0649` (§5.4/T4/§5.6), `32/32` (§5.4/F3-caption/T4-footnote/§5.6, five occurrences), `0/18` (same
five locations), `30/30` (§5.4/T4/§5.6), `p=1.9\times10^{-9}` (§5.4/T4/§5.6/§6.3, four occurrences),
`2/20` (§5.4/T4/§5.6), `p=4.0\times10^{-4}` (§5.4/T4/§5.6), Pearson `r\approx0.909`–`0.959` (rules)
and `0.948`–`0.955` (retrieval) (§1.4/§5.2/T4), `\delta=0.02` (§4.6/§4.8/§7.1/Eq.2), retrieval
`cutoff=75` (§1.3/§4.2/§4.5/T3), `P_{\mathrm{TRANSFORM}}=0.3` (§4.4/§7.2/T3), R3 thresholds `0.90`/
`0.70` (§4.7/T3/Eq. implicit). **No number differs from the frozen CSV or from
`research/PAPER_CONTRACT.md` §7's canonical-values list.** No new number was introduced anywhere in
this pass (this pass made zero edits to `main.tex`). No scientific gate was opened.

---

## 13. Forbidden-claim sweep

Full-file, case-insensitive grep for the exact term list in the task brief (`novel|first|proves|
demonstrates|significant|guarantees|always|never|universal|enterprise|architecture selection|
embedding|retrieval|governed|causes|validates|validated`), every occurrence read in context (not
just pattern-matched):

- **`novel`** (7 occurrences): all seven are correct negations — "we... make no claim that ADS is a
  novel metric" (§2.1), "not itself a novel contribution of this paper" (§3.2), "not... a new
  metric... a new architecture" (§1.4, §2.2's framing), etc. Zero positive novelty assertions.
- **`validated`/`validates`** (3 occurrences): all three negations — "not... a validated selection
  method" (§1.4), "not a validated method" (§9 Conclusion), "does not independently validate this
  experiment's finding" (§6.2). Zero assertions that anything was validated.
- **`governed`** (4 occurrences): all four carry an inline same-sentence scope qualifier — checked
  individually in this pass (Section 6/quoted above) — matches the wording already independently
  audited and locked at the E4 `CONTRIBUTION_LOCK.md` wording-fix checkpoint.
- **`enterprise`**: zero occurrences anywhere in `main.tex`. The "enterprise AI broadly" forbidden
  generalization is not present in any form.
- **`universal`**: zero occurrences.
- **`architecture selection`**: three occurrences (§1.2 first paragraph — describing the *field's
  name* for the general problem, i.e. "the Algorithm Selection Problem... later... AutoML...
  workflow composition"; §2.2's section header "Design-Time Algorithm and Architecture Selection";
  §2.2 body, same literature-family framing). All three describe the research area this paper's
  narrower question sits inside, never claim this paper *solved* architecture selection.
- **`embedding`** (9 occurrences): §1.1 (EMBEDDING_PRIMARY, explicitly distinguished from the tested
  `retrieval` mechanism, "no embedding-based mechanism is evaluated anywhere in this paper"), §3.3
  (four occurrences, the "we deliberately call this mechanism 'retrieval,' not 'embedding'" paragraph,
  ending "no embedding model was trained, downloaded, or evaluated anywhere in this experiment"),
  §6.4 (one occurrence, explicitly scoping the widening-gap finding away from "embedding-based
  retrieval... in general, which this experiment does not test"), §7.3/§8.2 (limitations/future-work,
  correctly framed as untested). **Zero occurrences imply Experiment 1 evaluated
  EMBEDDING\_PRIMARY or any embedding-based mechanism** — this was the specific risk named in the
  task's locked-position section, and it is not present anywhere in the manuscript.
- **`retrieval`** (~60 occurrences): the tested mechanism's own name throughout — expected and
  correct; every occurrence checked to confirm none silently substitutes "embedding" or implies a
  semantic/vector-similarity method (none does — see the `embedding` check above, which is the
  disambiguating pair for this term).
- **`always`** (4 occurrences): "almost always been booked to the same account" (§1.2, describing the
  intuitive motivation for the hypothesis, not a claim about this paper's own results), "Coverage...
  is below 1.0 in every one of the 240 conditions" (paraphrased as "always <1.0" in §7.1, an accurate,
  frozen-data-backed factual statement about rules' coverage, not an overreach), similarly for
  retrieval's "coverage is 1.0 in every one of the 240 conditions." All four are accurate statements
  about the frozen 240-condition dataset itself (an exhaustive, not sampled, population — "always" is
  the correct word for a 240/240 fact), not a generalization beyond it.
- **`never`** (~20 occurrences): overwhelmingly scope-limiting ("never merges them," "never
  re-tuned," "not... a general claim," "never implies," "was never designed, prototyped, or tested")
  — the word functions almost entirely as a *hedge* in this manuscript, not an overclaim. No instance
  found asserting something never fails/never happens in a way that oversteps the evidence.
- **`significant`** (4 occurrences): all four are statistical-significance usages tied to a stated
  p-value ("independently significant at $p=1.9\times10^{-9}$," etc.) — standard, correctly-scoped
  terminology, not a colloquial "big/important" claim.
- **`first`** (~11 occurrences): almost entirely either the ordinal transition word ("First, realized
  historical consistency strongly predicts...") or part of the compound term "rules-first" (naming the
  production system's `RULES_FIRST` decision, not a priority/novelty claim). No "first to show/first
  paper to" novelty assertion found anywhere.
- **`proves`/`demonstrates`/`guarantees`/`causes`**: `proves` and `guarantees` have zero occurrences.
  `demonstrates` has one occurrence (§2.4, "Jorgensen and Igel... empirically demonstrates... that a
  global classifier generalizes far worse across companies" — describing a cited third party's prior
  finding, standard Related-Work usage, not this paper's own result). `causes`/`causal` — the paper
  uses "causal account"/"causal claim" only with the explicit INFERRED/post-hoc hedge attached in the
  same sentence (§6.4, §2.1's absence, checked directly) — no unqualified "X causes Y" assertion found.

**Conclusion of the sweep: zero occurrences flagged as overstating the evidence.** This matches (and
independently reconfirms, on the complete post-E5.4 file, not just the pre-E5.4 snapshot) the same
zero-forbidden-claim result the E4, E5.1, and E5.2 audits each independently found on their own passes.

---

## 14. LaTeX / toolchain status

`which pdflatex` and `which bibtex` both fail in this environment — no LaTeX toolchain is installed,
consistent with the pre-existing, already-documented gap noted in `research/
MANUSCRIPT_SKELETON_AUDIT.md` and reconfirmed at the E5.4 checkpoint. Per this pass's explicit
instruction: **reported as a limitation, nothing installed globally, no dependency modified, no
compilation claimed.** Structural checks performed instead, without a compiler:

- `\begin{document}`/`\end{document}`, `\begin{abstract}`/`\end{abstract}`, all eight `\begin{table}`/
  `\end{table}` and four `\begin{figure}`/`\end{figure}` pairs, and both `\begin{equation}`/
  `\end{equation}` pairs were counted and matched (open count == close count for every environment
  type).
- All four `\includegraphics` paths (`figures/f1_design_flow.pdf` … `figures/f4_ranking_constancy.pdf`)
  resolve to files that exist on disk (confirmed at the E5.4 checkpoint and unchanged since).
- `\label{}`/`\ref{}`/`\citep{}`/`\citet{}` key sets were re-checked (see Section 7's Table T4 cross-
  check and the E5.1 audit's already-verified 1:1 citation-key-to-bib-entry match, unchanged since —
  no citation was added or removed by E5.2/E5.3/E5.4).
- No `\begin{figure}`/`\begin{table}` float lacks a `\caption{}` or `\label{}`.

This does not substitute for an actual compile (page breaks, float placement, and overfull-box
warnings genuinely cannot be checked without `pdflatex`), and this report does not claim otherwise.

Independently re-ran, this pass: `python -m pytest scripts/experiments/exp1/ -q` → **30 passed**;
`python scripts/experiments/exp1/analyze_posthoc.py --demo` → reproduces 32/50 agreement, Wilson CI,
and binomial p exactly. `git diff --quiet 6fb6188 -- data/outputs/experiments/exp1/final/` → exit 0
(frozen evidence byte-identical to the freeze commit). `git diff --stat -- research/PAPER_CONTRACT.md
research/CONTRIBUTION_LOCK.md research/contribution_lock.csv manuscript/references.bib
scripts/experiments/exp1/` → empty (all protected artifacts clean vs. HEAD `5dbec5c`). `git status
--short` shows the working tree unchanged by this review pass except this new report file.

---

## 15. Reviewer objections (anticipated, skeptical-external-reviewer framing)

1. *"Is the δ=0.02/cutoff=75/R3-0.90-0.70 parameter set cherry-picked?"* — Pre-empted: §4.5, §4.6,
   §4.8 each state these were calibrated once, before the frozen run, on data disjoint from the
   reported conditions, and never re-tuned after seeing results. §7.1 additionally states these are
   "judgment calls anchored to this repository's own precedent, not derived from a formal cost model"
   — the paper concedes the parameters are judgment calls rather than claiming false rigor.
2. *"Is the 64.0% aggregate just noise dressed up as a finding?"* — Pre-empted by §5.4/§5.6's own
   framing: the paper itself calls the aggregate "not significant at α=0.05" and states the real
   evidence is the two decisive by-target sub-bands, each independently significant. A skeptical
   reviewer reading only the abstract would still see this correctly hedged.
3. *"Why should I believe the representation-stability causal story rather than a simpler
   confound?"* — Pre-empted only partially: §6.4 already hedges the account as post-hoc/INFERRED, but
   a determined reviewer could still ask whether some other property correlated with the lexical
   condition (not just surface-form instability) explains the reversal. The manuscript does not claim
   to have ruled out alternative confounds beyond the ones named — this is an honest, not fatal, gap
   already covered by the existing "a fresh, prospective test... would strengthen it further" hedge
   in §6.4/§7.1.
4. *"Two mechanisms, one perturbation model, one generator family — how do I know this isn't an
   idiosyncrasy of rapidfuzz's WRatio scorer?"* — Pre-empted: §6.4 explicitly scopes the finding to
   "this specific perturbation model and this specific retrieval implementation," and §8.2 names
   generalization to embedding-based retrieval as untested future work. A reviewer raising this
   objection would find the paper already agrees with them.
5. *"Isn't the production motivation basically an anecdote?"* — Pre-empted repeatedly (§1.1, §6.2,
   §7.4) — the paper calls it exactly that ("two single data points," "cited... not... evidence").

No reviewer objection was found that the manuscript fails to anticipate or that would require new
science to answer — the objections above are all already addressed within the existing scope, not
gaps requiring a new experiment.

---

## 16. Exact required changes

**None.** This pass found zero claim-strength violations, zero numerical drift, zero forbidden-claim
resurrections, zero figure/data mismatches, and zero structural (environment-balance/reference)
defects. No edit to `manuscript/main.tex`, `manuscript/references.bib`, or any protected artifact is
required by this audit.

---

## 17. Optional improvements (not required, not applied)

Ranked by expected reader-comprehension benefit, smallest first; none of these touch a claim, a
number, or a scope boundary — purely sentence-level tightening candidates for a future, explicitly
authorized copy-edit pass:

1. §5.4's two-framings paragraph (32/32 vs. 30/30 framing) could be split into two shorter sentences
   for a first-time reader — currently correct and complete, just dense (Section 1, item 7 above).
2. §1.1's opening paragraph (11 lines, four distinct pieces of information) could be split at the
   EMBEDDING_PRIMARY disambiguation clause — again, correct and complete, just the single densest
   paragraph in the paper.
3. The author/affiliation/ORCID/date placeholders (lines 47, 52) are pre-existing, already-flagged,
   deliberately-deferred human decisions (`MANUSCRIPT_ARCHITECTURE.md` §14) — not a content defect,
   but the most reader-visible unfinished item in the file if the PDF were opened today.

None of these were applied, per this pass's explicit instruction not to auto-edit.

---

## 18. Independent auditor verdict

🟠 **CONDITIONAL** (`research/AUDIT_REPORT.md`). The independent auditor re-derived every check in
Sections 12-14 above from source rather than trusting this document, and confirmed all of them: all
11 protected numbers recomputed directly from the frozen CSV and matched exactly; the realized-ADS-
band-vs-nominal-target p-value distinction correctly separated everywhere; all 17 citation keys
resolve with the required peer-review qualifiers; the full forbidden-claim sweep independently
re-read (~150 occurrences) with zero violations; F2/F3/F4 visually confirmed correct; tests and demo
reproduce; all protected artifacts byte-identical to HEAD; git hygiene clean.

**One genuine defect found that this document's Section 11 (Figure/table consistency) missed:**
`manuscript/figures/generate_figures.py` line 66 hardcodes F1's fourth schematic box label as
`"Pre-registered\nfalsification table\n(Sec.4.13)"` — but `main.tex`'s Section 4 (Experimental
Design) only contains subsections 4.1 through 4.9; there is no Section 4.13 anywhere in the document.
The falsification-table content this label points at actually lives in §4.8 ("Calibration and
Preregistration" — confirmed by direct read, lines 771-802, which states "The falsification table
used to classify the experiment's outcome... was fixed in advance of the frozen run"). This is a
dangling internal reference **baked into the rendered PDF image itself** (`f1_design_flow.pdf`), not
into `main.tex`'s LaTeX source — Section 11 above checked F1's `\caption{}` text against its content
correctly, but did not check the schematic's own embedded box labels against the manuscript's actual
section numbering, which is exactly how this was missed at both this pass and the earlier E5.4
checkpoint (commit `5dbec5c`).

**Required fix — approved and applied.** `generate_figures.py:66`'s label was changed from
`Sec.4.13` to `Sec.4.8`, and only `manuscript/figures/f1_design_flow.pdf` was regenerated (a
targeted call to `make_f1()` alone, not the script's full `main()`, so F2/F3/F4 were not touched or
re-rendered). Confirmed by direct inspection of the regenerated PDF: the fourth box now reads
"Pre-registered falsification table (Sec.4.8)"; the other three boxes, arrows, and layout are
unchanged. `python -m pytest scripts/experiments/exp1/ -q` → 30 passed;
`python scripts/experiments/exp1/analyze_posthoc.py --demo` → reproduces the frozen headline exactly.

**Resolution independently re-audited: 🟢 PASS.** A second, targeted `research-code-auditor` run
independently verified: (a) `git diff manuscript/figures/generate_figures.py` shows exactly the one
label-string line changed, nothing else; (b) the rendered PDF matches as described above; (c) — most
importantly — that `Sec.4.8` is actually *correct*, not merely less wrong than `Sec.4.13`: the auditor
independently recounted `main.tex`'s `\subsection` structure inside `\section{Experimental Design}`
(9 subsections, 4.1–4.9) and confirmed §4.8 ("Calibration and Preregistration," lines 771-802)
genuinely contains the falsification-table sentence the box points at, corroborated by two
pre-existing, unmodified in-document cross-references (`Section~4.7` for R3, `Section~4.8` for the
falsification criteria, at lines 568/572) that independently agree with this numbering; (d)
`git diff --stat` confirms only `generate_figures.py` and `f1_design_flow.pdf` changed — `main.tex`,
`references.bib`, `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`, and F2/F3/F4
are all byte-identical to HEAD `5dbec5c`; frozen Experiment 1 evidence remains byte-identical to
freeze commit `6fb6188`; (e) tests and demo independently re-reproduced; (f) a second-instance hunt
across F2/F3/F4 for any other hardcoded, un-typo-checked section/table/figure reference baked into a
rendered image found none — F3's baked-in counts (32/32, 0/18) were independently recomputed from the
frozen CSV and matched exactly. Two OPTIONAL FUTURE WORK notes only (no automated guard against this
class of bug recurring on a future renumbering; unrelated untracked historical audit files should
stay out of this fix's commit) — neither blocks this checkpoint.

**E5.5 final status: the manuscript is unchanged from the E5.4 checkpoint except for the regenerated
`f1_design_flow.pdf` and the one-line generator correction in `generate_figures.py`.** No prose,
citation, number, frozen-evidence, or protected-artifact change occurred anywhere in E5.5.
