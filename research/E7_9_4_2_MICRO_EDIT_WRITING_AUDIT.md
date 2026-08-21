# E7.9.4.2 Independent Micro-Edit Writing Audit

## 1. Scope

Reviewed the 5 named sentence-level edits to `manuscript/main.tex` supplied by the requesting
session, against the actual `git diff -- manuscript/main.tex` (uncommitted working-tree changes),
`research/PAPER_CONTRACT.md` (read fresh, in full), `research/CONTRIBUTION_LOCK.md` (Sec.1-3 read in
full), and the current rendered text at each edit site (read with full surrounding paragraphs, not
excerpts). Also cross-checked one factual claim embedded in edit 3 (a section-number correction)
against the manuscript's actual section structure, and independently verified the Reproducibility
Statement's new GitHub URL/path claim against `git remote -v` and `git ls-files`.

Independent finding, not inherited from the requesting session: the actual `git diff` for
`manuscript/main.tex` contains more than the 5 described changes. Beyond the 5 named edits, the
diff also includes: (a) a LaTeX comment change locking the paper's title (E7.8.2), (b) a
Section-4.1-to-7.3 cross-reference correction, occurring twice (once inline in edit 3's
paragraph, once in Table 2), and (c) a Reproducibility Statement rewrite that replaces "linked from
the paper's public code repository" with an explicit GitHub URL and file path, wrapped in a new
sloppypar block. references.bib, MANUSCRIPT_ARCHITECTURE.md, and
MANUSCRIPT_FORMAT_RESEARCH.md also show uncommitted changes (bib page-number additions, license/
category-lock notes) outside main.tex entirely. None of this contradicts the 5 edits' own
correctness, but the task's framing (exact 5 changes, pre-verified word-for-word) does not
match the full diff -- this is reported per the independence rule, not accepted at face
value. See Section 11.

## 2. Independent Findings

Read main.tex at each edit site with full paragraph context:

- Edit 1 site: Design-Time Algorithm and Architecture Selection (Barbudo paragraph), lines ~313-324.
- Edit 2 site: Inference-Time Selection and Escalation (Chow paragraph), lines ~350-359.
- Edit 3 site: same subsection, FrugalGPT/RankGPT paragraph, lines ~379-388, plus Table 2 row
  "Model cascades / LLM routing" (line 439).
- Edit 4 site: Domain-Specific Practice, lines ~397-414.
- Edit 5 site: Mechanistic Explanation: Representation Stability, lines ~1170-1201.

Verified independently: Section 7.3 ("Domain and Mechanism Scope", line 1292) is the paragraph that
actually states "The large-language-model mechanism was excluded from H1 ... and was not evaluated
at all in Experiment 1" -- Section 4.1 ("Research Hypothesis", line 566) does not mention the LLM
exclusion at all. The 4.1-to-7.3 reference fix bundled into edit 3 is therefore a genuine
correction of a previously wrong cross-reference, not a cosmetic change.

Verified independently: Section 5.5 (ADS x Representation-Stability Interaction, line
1042) explicitly states "the causal account for why it occurs is developed in Section 6.4, not
here" -- confirming that Section 6.4 (edit 5's location) is the paper's own designated location for
exactly this kind of causal/mechanistic elaboration, not scope creep into an unrelated subsection.

Verified independently: git remote -v shows origin https://github.com/stiFFLer-codes/ADS-Cascade.git,
and git ls-files data/outputs/experiments/exp1/final/* confirms final_condition_results.csv and
its companions are in fact committed at that path -- the new Reproducibility Statement wording is
factually accurate.

## 3. Proposed/Implemented Edit Review

EDIT ID: 1
LOCATION: main.tex, Sec.2.2 (Barbudo paragraph), line ~318-319
ORIGINAL: "We do not claim that this paper's simple, interpretable threshold rule competes with
that automated search paradigm."
PROPOSED: "This paper's simple, interpretable threshold rule is not offered as a competitor to
that automated search paradigm."
VERDICT: PASS
REASON: Style-only rewording; no semantic drift. Both deny the rule competes with the AutoML
search paradigm; scope, evidence relationship, and hedging all unchanged. Converts first-person
meta-disclaimer to third-person passive framing -- see Sec.9 for a voice-consistency note.

EDIT ID: 2
LOCATION: main.tex, Sec.2.3 (Chow paragraph), line ~353
ORIGINAL: "We make no claim that this experiment introduces a new reject-option variant."
PROPOSED: "Nothing in this experiment is offered as a new reject-option variant."
VERDICT: PASS
REASON: Style-only rewording; no semantic drift. Same voice-consistency note as Edit 1.

EDIT ID: 3
LOCATION: main.tex, Sec.2.3 (FrugalGPT/RankGPT paragraph), line ~384-387; also Table 2 row 7
ORIGINAL: "We do not claim that Experiment 1's two-mechanism comparison is itself a cascade
contribution. ... the LLM mechanism is explicitly excluded from Experiment 1 (Section 4.1)"
PROPOSED: "Experiment 1's two-mechanism comparison is not itself put forward as a cascade
contribution. ... the LLM mechanism is explicitly excluded from Experiment 1 (Section 7.3)"
VERDICT: PASS
REASON: Style-only rewording for the disclaimer sentence, plus a bundled, independently verified
factual cross-reference fix (Section 7.3 is the paragraph that actually discusses LLM exclusion;
Section 4.1 does not mention it). No semantic drift in the disclaimer; the reference change is a
correction, not a claim change.

EDIT ID: 4
LOCATION: main.tex, Sec.2.4 (Domain-Specific Practice), line ~408-409
ORIGINAL (deleted clause): ", and a corresponding sentence in this project's companion technical
report remains an open, still-uncorrected item tracked outside this manuscript"
PROPOSED: clause removed; sentence now ends at "... directly contradicts that framing."
VERDICT: PASS
REASON: Confirmed no scientific claim or citation lost. The surviving sentence and the following
sentence ("The narrow delta that survives is academic...") remain fully intact and self-contained.
The kenfromfinance2025 citation and its contradiction claim are unaffected, with the "not
peer-reviewed" qualifier intact per PAPER_CONTRACT.md Sec.2 row 11. The removed clause referenced
an internal, non-submitted companion document (TECHNICAL_REPORT.md), carried no citation or
evidence content, and was confusing to an external reader.

EDIT ID: 5
LOCATION: main.tex, Sec.6.4 (Mechanistic Explanation: Representation Stability), appended sentence,
line ~1195-1200
ORIGINAL: no prior sentence at this position; subsection previously ended at "...which this
experiment does not test."
PROPOSED: "This blindness is a direct consequence of how ADS is defined, so the qualitative shape
of 6b is partly built into the construction; what is not given by that construction is the
magnitude and direction actually observed, namely the empirical winner is constant across all 120
conditions of each lexical condition (retrieval under VARIED, tie under CLEAN), and the
rules-minus-retrieval gap widens, rather than narrows, as realized ADS rises."
SEMANTIC INVARIANT: A: N/A, new sentence. B: two claims. First, ADS's blindness to the perturbable
surface string is a definitional/structural fact, not a new empirical claim; already established
two sentences earlier in the same subsection ("computed on the stable product identity,
structurally blind to the perturbable surface string... a variable ADS cannot observe by
construction") and at Sec.5.3 line 931 ("realized ADS is invariant to the lexical condition by
construction"). Second, the sentence explicitly separates this definitional point from the
empirical magnitude/direction, which it correctly attributes to observation, not construction.
C: both cited facts (120/120 winner constancy; gap widening 0.137 to 0.168 to 0.185 under VARIED)
are independently verified already present at Sec.5.3 (lines 923-926) and Sec.5.5/Table 5 (lines
1034-1036, 1060-1065); no new statistic is introduced. D: scope unchanged, stays within Experiment
1 and this generator, this perturbation model. E: hedging is, if anything, increased; the sentence
adds an explicit definitional-versus-empirical distinction not present before, and uses "partly"
rather than an unqualified claim of predetermination.
EVIDENCE RELATIONSHIP: matches PAPER_CONTRACT.md Sec.2 row 6 (the causal account, INFERRED, cites
CONTRIBUTION_LOCK.md Sec.2 step 8) and reuses only already-canonical Sec.5 numbers.
CLAIM STRENGTH: unchanged, arguably self-limiting; the sentence caveats part of its own
subsection's significance rather than strengthening it. No causal verb stronger than the existing
"structurally blind" / "by construction" language already used earlier in the same subsection and
at line 929 ("governed by," reserved there for the lexical-condition-to-winner relationship, not
reused here for ADS). Does not use "proves," "demonstrates," or "governs" for ADS itself.
SCOPE: unchanged, bounded to this experiment and this generator.
HEDGING: unchanged or increased.
SOURCE-OVERLAP RISK: none identified; no citation-adjacent phrasing.
WRITING QUALITY: dense, a single long sentence, but consistent with the surrounding paragraph's
register. It substantially restates a structural point already made two sentences earlier in the
same subsection (see Sec.7 below), a redundancy note rather than a correctness problem.
VERDICT: PASS
REASON: Does not upgrade H1, does not merge 6a/6b, does not claim ADS predicts ranking, does not
introduce new statistics, and explicitly preserves the empirical/definitional distinction that
prevents this from becoming a claim that 6b was predetermined. Minor redundancy flagged as a style
note only.

## 4. Semantic-Invariant Checks

Summarized per-edit in Section 3. No edit changes claim scope, evidence relationship, or hedging
level in a way that increases claim strength. Edits 1-3 are pure register changes (first-person
disclaimer to passive-voice disclaimer) with no content change. Edit 4 removes a clause with no
scientific content. Edit 5 adds a new, appropriately-hedged sentence in its designated home
subsection (per Sec.5.5's own forward-reference to Sec.6.4), reusing only already-canonical
numbers.

## 5. Source-Overlap / Originality Findings

No new source-overlap risk identified in any of the 5 edits. None introduces new citation-adjacent
phrasing or close paraphrase of a specific source. Not applicable to Edit 4 (pure deletion).

## 6. Formulaic Language Findings

Edits 1-3 each replace one instance of the paper's recurring "We do not claim X" / "We make no
claim that X" disclaimer template with a distinct passive-voice variant ("X is not offered as...",
"Nothing... is offered as...", "X is not itself put forward as..."). Read against the rest of
Sections 2.2-2.3, this same disclaimer template appears at least three more times, left unchanged
by this edit set: line ~301 ("We make no claim that design-time selection... is itself new"), line
~337 ("We do not claim that a one-shot, pre-deployment design gate is itself a contribution"), line
~367 ("We do not claim that this experiment's mechanism-selection rule is an instance of learning
to defer"). The result is a section that now mixes two disclaimer registers roughly evenly rather
than using one consistently or fully varying all six instances. This is not a scientific problem,
it is a genuine authorial-voice/formulaic-pattern finding, classified as useful-but-inconsistent
rather than unnecessary, since some variation from a six-times-repeated template is defensible, but
a half-converted set reads as patchwork rather than a deliberate rhythm. Flagged as advisory, not
blocking.

## 7. Readability & Articulation Findings

Edit 5's new sentence substantially restates, two sentences later in the same subsection, the point
already made at lines 1172-1176 ("Realized ADS is computed on the stable product identity,
structurally blind to the perturbable surface string; in this experiment, which mechanism wins is a
constant function of the lexical condition, a variable ADS cannot observe by construction"). The
new sentence's opening clause ("This blindness is a direct consequence of how ADS is defined") is
close to a paraphrase of that earlier sentence. This is not a factual problem, both statements are
consistent and true, but it is a genuine repetition the human author may want to either accept as
deliberate reinforcement bridging into the pre-emptive-objection point that follows, or tighten.
Edits 1-4 read cleanly at their sites; no ambiguous referents or broken transitions introduced.

## 8. Terminology Consistency

ADS, 6a/6b, historical decision consistency, Experiment 1, R3 all used consistently at each edit
site, matching usage elsewhere in the manuscript. Edit 3's corrected cross-reference (Section 7.3)
improves reference consistency versus the prior incorrect Section 4.1 pointer. Edit 5 correctly
reserves "governed by" for the lexical-condition-to-winner relationship, as already established at
line 929, rather than misapplying it to ADS.

## 9. Authorial Voice

See Section 6. The core finding: Edits 1-3 introduce a second, distinct disclaimer register into
Sections 2.2-2.3 without converting the section's other same-purpose sentences, producing a mixed
voice within adjacent paragraphs. This is not severe, both registers are legitimate formal academic
prose and not evidence of AI-generation drift, but it is inconsistent, and a careful human
editorial pass should decide one way or the other rather than leave it half-done.

## 10. Scientific Guardrail Verification

1. H1 status (PARTIALLY_SUPPORTED): unaffected by any of the 5 edits.
2. 6a/6b distinction: preserved. Edit 5 stays entirely within 6b's territory (ranking), does not
   invoke 6a (accuracy prediction) or merge the two.
3. No claim that ADS predicts mechanism ranking: preserved, Edit 5 reinforces the opposite (ADS
   cannot observe the ranking-determining variable).
4. No universal/general-purpose selection claim: preserved, all 5 edits stay within Experiment 1's
   scope; Edit 5 explicitly stays inside this experiment and this generator.
5. No novelty inflation: preserved, none of the 5 edits touches novelty framing.
6. No production data presented as experimental evidence: not implicated by any of the 5 edits.
7. Canonical numbers unchanged: verified, Edit 5 reuses only already-canonical Sec.5.3/5.5 numbers
   (120/120, gap-widening direction), introduces no new figure.
8. No causal/statistical strengthening: verified, Edit 5 uses "direct consequence" only for the
   already-established definitional blindness fact, not for the empirical ranking result itself,
   and explicitly separates the two; no "proves/demonstrates/shows" language added anywhere in the
   5 edits.
9. Scope/uncertainty language: preserved or increased. Edit 5 adds hedging, does not remove any.
10. No unsupported claim introduced via rewording: none of the 5 edits introduces a claim beyond
    what PAPER_CONTRACT.md Sec.2 already licenses (row 4 for 6b, row 6 for the causal account, row 8
    for the algorithm-selection-lineage positioning that Edits 1-3 sit inside).

No guardrail violation found in any of the 5 edits.

## 11. Regression Check

No prior E7_5_INDEPENDENT_WRITING_AUDIT_*.md report covers this exact micro-edit set; the existing
_CONDITIONAL.md, _ABSTRACT_RESTORE_PASS.md, and _PASS.md files predate this pass and reviewed
different text (the abstract and earlier passes). No regression against those found, this pass does
not touch the abstract or any previously-flagged item from those reports.

The one regression-adjacent finding of this pass is procedural, not textual: the requesting session
characterized the applied diff as exactly 5 changes, "pre-verified word-for-word... before being
applied," but the actual working-tree diff for main.tex contains at least 3 additional, undisclosed
changes: a title-lock comment, a duplicated Section-4.1-to-7.3 table-row fix, and a Reproducibility
Statement rewrite exposing a public GitHub URL and repository path, plus unrelated uncommitted
changes in references.bib, MANUSCRIPT_ARCHITECTURE.md, and MANUSCRIPT_FORMAT_RESEARCH.md.
Independently verified all of these extra changes are factually accurate and do not violate any
Step 2 guardrail, but they were not disclosed as part of "the 5 changes" and were not in the
reviewer's assigned scope, flagged for the human author's awareness so the "exactly 5,
pre-verified" framing is not taken as a complete account of what changed in this working tree.

## 12. Verdict

GREEN, PASS, for the 5 named edits as reviewed. All 5 are either pure style/register changes with
no semantic drift (Edits 1-3), a verified-safe deletion of a scientifically-empty internal-process
aside (Edit 4), or a well-hedged addition that reuses only already-canonical numbers and explicitly
avoids upgrading H1, merging 6a/6b, or claiming ADS predicts ranking (Edit 5). No Step 2 guardrail
is violated by any of the 5 edits.

Two non-blocking items for the human author to decide, neither a guardrail violation:

1. Voice consistency (Sec.6/9): Edits 1-3 convert 3 of 6 same-purpose "We do not claim.../We make
   no claim..." disclaimer sentences in Sections 2.2-2.3 to a different passive-voice register,
   leaving the other 3 unchanged. Recommend either converting the remaining 3 for consistency, or
   reverting Edits 1-3 to the original register; either is fine scientifically, but the current
   half-converted state is a minor internal-consistency wart.
2. Minor redundancy (Sec.7): Edit 5's opening clause closely restates a point made two sentences
   earlier in the same subsection (lines 1172-1176). Recommend the author confirm this is
   deliberate reinforcement bridging into the pre-emptive-objection point, or tighten it.

Separately, for transparency (Sec.1/11): the actual diff contains changes beyond the 5 described (a
Section-4.1-to-7.3 cross-reference fix, a Reproducibility Statement URL/path rewrite, and
governance-file title/license/category locks). All were independently spot-checked and found
factually correct and guardrail-compliant, but the human author should confirm these were
intentional, since they were not part of the reviewed 5-edit list as framed.
