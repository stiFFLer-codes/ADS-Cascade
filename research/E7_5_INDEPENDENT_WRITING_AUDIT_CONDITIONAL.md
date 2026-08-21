# E7.5 Independent Research Writing & Originality Audit

## 1. Scope

This report supersedes the prior E7.5 CONDITIONAL report at the same filename
(overwritten per Step 5, which permits overwriting when re-running the same
bounded review -- the abstract closing sentence is the same unit of prose
that prior report's Part B and Section 12 item 1 left open). This pass
evaluates two hypothetical candidate rewrites of the abstract's closing
sentence, drafted by the parent session but **not applied to
manuscript/main.tex**. No manuscript edit exists in the working tree beyond
the pre-existing three-line punctuation diff in Section 1.1 (the "E7.5-A"
diff, previously reviewed and passed in
research/E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md, left in place unmodified
since it is a different, narrower unit).

Verified directly, this session: `git status --porcelain` shows only
`manuscript/main.tex` modified; `git diff --stat manuscript/main.tex` shows
exactly `3 insertions(+), 3 deletions(-)`, i.e. still only the E7.5-A
punctuation diff. Neither candidate sentence appears anywhere in the file --
grepped for `"restore"` (zero matches) and confirmed by direct read that the
abstract at lines 62-85 still reads exactly as CURRENT, unedited.

Ground truth read fresh this session: the full abstract
(`manuscript/main.tex` lines 62-85), the Results 6a/6b subsections (lines
897-936), the Discussion's "Mechanistic Explanation: Representation
Stability" subsection (lines 1173-1198), "Relationship to Algorithm
Selection and Meta-Learning" (lines 1204-1217), "Implications for Practice
and Future Selector Design" (lines 1219-1246), the Contribution Statement
(lines 226-247), Future Work Sec.8.1 "Representation-Stability-Aware
Selectors" (lines 1344-1349), H1-status lines (569, 1254-1260, 1406),
`research/CONTRIBUTION_LOCK.md` Sec.5 (all four formulations, rows 187-190),
Sec.6 (locked wording, lines 194-227), Sec.10 (Future work, lines 331-341),
and Sec.11 (One-sentence paper pitch, lines 358-382, all five sub-items
A-E). The prior `research/E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md` was
read in full before being overwritten and is the direct baseline for the
regression check in Section 11, since it is the report that first raised the
specific risk these two candidates were drafted to address.

This pass does **not** re-review the six Section 2 disclaimer sentences
(Part A of the prior CONDITIONAL report) -- that item was independently
resolved KEEP-all-six in the prior pass and is outside the scope of this
task, which is explicitly the abstract closing sentence and the two named
candidates. It is carried forward unchanged in Section 11.

## 2. Independent Findings

### A. The three sentences under comparison, read side by side

CURRENT (manuscript/main.tex, lines 81-84, verified verbatim):
"We conclude that a design-time selector built on historical consistency
alone should not be trusted to pick the better-performing mechanism without
also accounting for representation stability -- a direction for future
work, not something built or tested here."

CANDIDATE 1 (hypothetical, not in file):
"We conclude that a design-time selector built on historical consistency
alone should not be used to predict which mechanism will win. Whether a
selector that also conditions on a measured representation-stability signal
would restore reliable prediction is the direct next hypothesis this
experiment motivates: no such selector was designed, prototyped, or tested
here."

CANDIDATE 2 (hypothetical, not in file):
"We conclude that a design-time selector built on historical consistency
alone should not be trusted to predict which mechanism will win; whether
conditioning on a measured representation-stability signal as well would
restore that reliability is an open question this experiment motivates but
does not test, prototype, or answer here."

### B. Independently located parallel language already in the manuscript

Three phrases recur verbatim or near-verbatim across the body of the paper
and are the correct comparison points for judging whether either candidate
better matches the paper's own established, already-vetted register for
this exact idea:

- "does not predict which mechanism wins" -- appears three times, word-for-
  word identical: abstract line 73, Results Sec.5.3 line 925, Discussion
  line 1099.
- "is the direct next hypothesis this experiment motivates" -- Discussion
  line 1236-1237 and Future Work Sec.8.1 line 1346-1347, word-for-word
  identical between those two locations.
- "designed, prototyped, or tested" / "designed, prototyped, or partially
  tested" -- Discussion line 1227 ("designed, prototyped, or tested
  anywhere in this repository") and Future Work Sec.8.1 line 1348-1349
  ("designed, prototyped, or partially tested here").

Independently checked via grep: the word "restore" does not appear anywhere
in the current manuscript. Both candidates introduce it; CURRENT does not
use it either. This is a genuinely new word choice in both candidates, not
present anywhere else in the document to anchor its register.

### C. CONTRIBUTION_LOCK.md Sec.5, Formulation #3, read directly

Row 3 (moderate formulation, explicitly not the locked contribution): claim
text is "...suggesting design-time selectors for hybrid classification
systems should account for representation stability alongside label
consistency." Limiting evidence column: "The prescriptive 'should account
for representation stability' clause was never built or tested -- no
two-feature selector exists anywhere in this repository." Reviewer-attack-
risk column: "Medium-high -- biggest risk is a reviewer conflating 'found a
limitation' with 'proposed and validated a fix.'" Required qualification
column: "Repeated, explicit 'not built, not tested here' framing every time
the two-feature idea is mentioned."

This is the specific named risk against which both candidates must be
judged, and is the same risk the prior CONDITIONAL report (Section 4B)
independently found CURRENT to be exposed to via a sufficiency implicature
in the "without also accounting for X" construction.

### D. CONTRIBUTION_LOCK.md Sec.11.E, the locked one-sentence future direction

"A natural next step is a decision rule that conditions on both historical
consistency and a measured representation-stability signal, though no such
rule was built or tested here." This is descriptive/hypothesis-framed, not
prescriptive ("should account for"), and both candidates' second
clause/sentence are structurally much closer to this locked phrasing than
CURRENT is.

## 3. Proposed/Implemented Edit Review

```
EDIT ID: E7.5-B-1 (CURRENT vs CANDIDATE 1)
LOCATION: manuscript/main.tex, Abstract, lines 81-84 (hypothetical replacement, not applied)
ORIGINAL: "We conclude that a design-time selector built on historical
consistency alone should not be trusted to pick the better-performing
mechanism without also accounting for representation stability -- a
direction for future work, not something built or tested here."
PROPOSED: "We conclude that a design-time selector built on historical
consistency alone should not be used to predict which mechanism will win.
Whether a selector that also conditions on a measured representation-
stability signal would restore reliable prediction is the direct next
hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
SEMANTIC INVARIANT:
A. Original claims: (i) the tested, consistency-only selector should not be
trusted to identify the winning mechanism; (ii) this untrustworthiness
holds specifically "without also accounting for representation stability"
-- a necessity construction that, per the prior audit's independent
reading, carries a natural conversational implicature that accounting for
representation stability would be sufficient to fix the problem; (iii)
trailing hedge disclaims that a two-feature selector was "built or tested."
B. Proposed claims: (i) identical core finding, restated using the exact
phrase used three times elsewhere in the paper ("predict which mechanism
will win" / "wins"), replacing "pick the better-performing mechanism"; (ii)
the two-feature-selector idea is moved into a fully separate sentence,
reframed as an explicit open question ("Whether X would restore Y is the
direct next hypothesis") rather than a dependent clause of the "should not
be trusted" claim -- this removes the grammatical adjacency that produced
the necessity/sufficiency implicature in ORIGINAL; (iii) the "designed,
prototyped, or tested" disclaimer is retained and now uses the exact
three-verb phrasing already used at Discussion line 1227 and near-exactly
at Future Work line 1348-1349, rather than the looser "built or tested" of
ORIGINAL.
C. Evidence: (i) is the locked 6b finding (CONTRIBUTION_LOCK.md Sec.6,
`manuscript/main.tex` lines 923-936); (ii) is explicitly, and only,
supported as an open/untested hypothesis by Discussion lines 1236-1242 and
Future Work Sec.8.1 lines 1344-1349 -- both of which the proposed sentence
now echoes near-verbatim rather than diverging from in register.
D. Scope: unchanged -- neither sentence restates generator/lexical-model/
production-case-study scope; both rely on the immediately preceding abstract
sentence ("This finding is scoped to one synthetic generator...") for that,
exactly as CURRENT does.
E. Hedging: strengthened, not weakened. ORIGINAL's hedge ("not something
built or tested here") is retained in substance and made more specific
(the three-verb "designed, prototyped, or tested" triplet, matching the
paper's own established phrasing) and, more importantly, the sufficiency
implicature flagged in the prior audit's Section 4B is structurally removed
by moving the two-feature idea out of the "without also accounting for"
subordinate-clause position into its own explicitly interrogative sentence.
F. A-E differ: (ii)/(iii) under A vs B show a genuine, deliberate
semantic-scope narrowing of the future-direction claim (from implied
necessity-with-sufficiency-flavor to explicit unanswered-question), which
is a hedging strengthening, not a claim strengthening or a fact change. The
core 6b-adjacent finding in (i) is unchanged in substance and, if anything,
now phrased closer to the paper's own repeated canonical wording.
EVIDENCE RELATIONSHIP: unchanged for the core claim; improved for the
future-direction claim, which now aligns with (rather than diverges from)
the locked Sec.11.E wording and the Discussion/Future-Work sections' own
phrasing of the identical idea.
CLAIM STRENGTH: unchanged for the core (i) claim; weaker (more hedged) for
the future-direction (ii) claim, in the correct direction relative to the
named Formulation #3 risk.
SCOPE: unchanged.
HEDGING: strengthened (see E above) -- this is the specific dimension the
prior CONDITIONAL audit flagged as deficient in CURRENT.
SOURCE-OVERLAP RISK: none identified -- this is the paper's own synthesis
sentence, not paraphrase of an external cited source.
WRITING QUALITY: The word "restore" is not used anywhere else in the
manuscript and carries a mild, arguably inaccurate presupposition that
mechanism-ranking prediction was reliable prior to this finding and would
be "restored" -- in fact Experiment 1 shows R3 agreed with the empirical
winner in 100% of one ADS band and 0% of another, which is not obviously a
prior state of "reliability" to restore. This is a minor precision note,
not a guardrail violation (it appears inside an explicitly hypothetical,
untested "whether X" question, not as an assertion), but is worth the human
author's attention as an optional word-choice improvement (e.g. "achieve
reliable prediction" avoids the presupposition). Otherwise the two-sentence
split is easier to parse than the original's single ~40-word sentence with
two subordinate clauses, and the reuse of "is the direct next hypothesis
this experiment motivates" and "designed, prototyped, or tested" pulls the
abstract's register into alignment with the Discussion and Future Work
sections, improving cross-section authorial-voice consistency (a specific
gap the prior CONDITIONAL report's Section 9 identified).
VERDICT: PASS
REASON: Resolves the specific sufficiency-implicature risk the prior
CONDITIONAL audit identified against Formulation #3's named risk, without
weakening the core 6b-adjacent claim, without touching scope, and while
improving terminology alignment with three other passages in the document.
The "restore" word choice is a minor, non-blocking precision note.
```

```
EDIT ID: E7.5-B-2 (CURRENT vs CANDIDATE 2)
LOCATION: manuscript/main.tex, Abstract, lines 81-84 (hypothetical replacement, not applied)
ORIGINAL: (same as E7.5-B-1)
PROPOSED: "We conclude that a design-time selector built on historical
consistency alone should not be trusted to predict which mechanism will
win; whether conditioning on a measured representation-stability signal as
well would restore that reliability is an open question this experiment
motivates but does not test, prototype, or answer here."
SEMANTIC INVARIANT:
A. Original claims: as in E7.5-B-1.
B. Proposed claims: (i) same core-claim wording improvement as Candidate 1
("predict which mechanism will win," matching the paper's thrice-repeated
phrase, in place of "pick the better-performing mechanism"); (ii) the
two-feature-selector idea is reframed as "an open question... but does not
test, prototype, or answer here" rather than a "without also accounting
for" dependent clause -- same directional fix as Candidate 1, but the two
halves remain a single semicolon-joined sentence rather than two full
sentences, preserving closer grammatical/rhetorical proximity between the
"should not be trusted" claim and the "would restore" question than
Candidate 1's full-stop break provides.
C. Evidence: same as E7.5-B-1 for (i). For (ii): same grounding in
Discussion 1236-1242 / Future Work 1344-1349, though the specific verb
triplet used ("test, prototype, or answer") is not an exact match to any
single instance elsewhere in the manuscript -- "designed, prototyped, or
(partially) tested" appears twice verbatim; "answer" is a new fourth verb
not used in either instance, introduced because this candidate frames the
future direction as a "question" (which can be "answered") rather than a
"hypothesis" or "selector" (which is "designed/prototyped/tested").
Internally consistent with its own "open question" framing, but a
terminology near-miss relative to the manuscript's two existing anchor
sentences.
D. Scope: unchanged, same reasoning as E7.5-B-1.
E. Hedging: strengthened relative to CURRENT, same direction as Candidate
1 -- the "without also accounting for" necessity/sufficiency construction
is removed and replaced with an explicit "open question... does not...
answer" framing. Marginally less complete a break than Candidate 1 because
the semicolon keeps both clauses in one sentence (a softer syntactic break
than a full stop), which retains slightly more of the "should not be
trusted [without X]" cadence of CURRENT than Candidate 1's two-sentence
form does -- though the explicit "open question... does not... answer"
language still substantively closes the sufficiency-implicature gap
regardless of the punctuation choice.
F. A-E differ in the same direction as E7.5-B-1 (weaker/more-hedged
future-direction claim, unchanged core claim, unchanged scope), with two
minor differences from Candidate 1: (a) marginally closer syntactic
proximity between the two clauses (semicolon vs. period), and (b) a
verb-triplet ("test, prototype, or answer") that is a near-miss rather than
an exact match to the manuscript's existing "designed, prototyped, or
tested" anchor phrase.
EVIDENCE RELATIONSHIP: unchanged for the core claim; improved for the
future-direction claim, same as Candidate 1, marginally less precisely
anchored to the manuscript's own existing wording.
CLAIM STRENGTH: unchanged for the core claim; weaker (more hedged) for the
future-direction claim, same direction as Candidate 1.
SCOPE: unchanged.
HEDGING: strengthened, same direction as Candidate 1, marginally softer
break between clauses.
SOURCE-OVERLAP RISK: none identified.
WRITING QUALITY: Retains "should not be trusted" from CURRENT (Candidate 1
changes this to "should not be used"), which is arguably a smoother,
lower-friction edit relative to CURRENT's existing wording and preserves
slightly more surface continuity with the original sentence. "Restore" has
the same minor precision note as in Candidate 1 (not used elsewhere in the
manuscript). The single-sentence, semicolon-joined structure is denser than
Candidate 1's two-sentence structure and reintroduces some of the same
"long sentence with subordinate clause" density the prior baseline audit
flagged generically as a readability note for the abstract.
VERDICT: PASS
REASON: Resolves the same core sufficiency-implicature risk as Candidate 1
and does not weaken any guardrail, but is a marginally less complete fix
than Candidate 1 on two dimensions: (a) the semicolon retains closer
clause-adjacency to CURRENT's problematic construction than a full sentence
break would, and (b) its verb triplet is a near-miss rather than an exact
match to the manuscript's own already-established "designed, prototyped, or
tested" phrasing used twice elsewhere for this identical idea.
```

## 4. Semantic-Invariant Checks

Both candidates leave the core 6b-adjacent claim (A) semantically identical
to CURRENT, and both leave scope (D) untouched. The material difference
between CURRENT and both candidates lies entirely in E (hedging) for the
future-direction half of the sentence: CURRENT expresses the two-feature-
selector idea as a dependent clause of a "should not be trusted without X"
construction, which independently (this pass, and the prior CONDITIONAL
pass) reads as carrying a natural-language implicature that X would be
sufficient to restore trust -- a reading that, if a reader stops at the
abstract, risks exactly the "conflating a found limitation with a validated
fix" failure mode CONTRIBUTION_LOCK.md Sec.5 row 3 names as Formulation #3's
biggest risk. Both candidates restructure the future-direction half into an
explicit, syntactically separated "whether X would work is an untested
open question / hypothesis" construction, which removes that implicature
by construction rather than by relying on a trailing hedge alone. Neither
candidate strengthens the core claim, narrows or broadens scope, or removes
any existing hedge; both add a layer of hedging precision to the part of
the sentence the prior audit specifically found under-hedged.

The one shared, minor semantic-precision issue in both candidates is the
verb "restore" (Section 2B), which was not independently identified by the
task framing and is flagged here as this pass's own finding: it mildly
presupposes a prior state of reliable ranking-prediction that Experiment 1
itself did not establish existed (R3 agreed with the empirical winner in
100% of one band and 0% of another -- not obviously "reliable" to begin
with, in either direction). This sits inside a hypothetical, explicitly
unanswered "whether" clause in both candidates, so it does not by itself
assert anything false; it is a word-choice precision note for the human
author, not a guardrail violation.

## 5. Source-Overlap / Originality Findings

Not applicable to either candidate. Both are original synthesis sentences
restating the paper's own locked finding and its own already-published
future-work framing (CONTRIBUTION_LOCK.md Sec.10-11); no external cited
source's phrasing is implicated. The reuse of "is the direct next
hypothesis this experiment motivates" and "designed, prototyped, or tested"
in Candidate 1 is intra-document self-consistency (reusing this paper's own
already-vetted phrasing from Discussion/Future Work), not a source-overlap
risk in the external-plagiarism sense that Section 5 of the audit framework
addresses.

## 6. Formulaic Language Findings

Neither candidate introduces new instances of the "We do not claim..."
disclaimer-scaffolding pattern flagged in the prior baseline/CONDITIONAL
audits' Section 6. Candidate 1's reuse of two exact phrases from the
Discussion/Future Work sections is a deliberate, load-bearing terminology
anchor (Section 4 above), not decorative templating -- classified (A)
scientifically/register-necessary repetition under the Step 4 dimension-4
taxonomy, not (C) unnecessary.

## 7. Readability & Articulation Findings

Candidate 1 splits CURRENT's single ~40-word sentence (with two subordinate
clauses) into two shorter sentences -- consistent with, and a natural
extension of, the prior baseline audit's generic recommendation to split
the manuscript's longest, most qualification-dense sentences where doing so
loses no content (baseline PASS report Section 7 and Section 12 item 3;
also the E7.5-A diff already reviewed and passed in Section 1.1 for an
analogous split). Candidate 2 keeps a single semicolon-joined sentence,
comparable in density to CURRENT. Neither introduces an unparseable
construction; both remain readable on a single pass.

## 8. Terminology Consistency

Both candidates replace CURRENT's one-off "pick the better-performing
mechanism" with "predict which mechanism will win" (Candidate 1) / "predict
which mechanism will win" (Candidate 2, identical wording in this clause),
which is a direct terminology-consistency improvement: this exact phrase
("does not predict which mechanism wins" / "predict which mechanism will
win") already appears three times elsewhere in the manuscript (lines 73,
925, 1099) and CURRENT's "pick the better-performing mechanism" was the one
outlier phrasing for this same idea. Candidate 1's "is the direct next
hypothesis this experiment motivates" and "designed, prototyped, or tested"
are exact or near-exact matches to Discussion line 1236-1237/1227 and
Future Work line 1346-1349. Candidate 2's "test, prototype, or answer" is a
near-miss (introduces "answer" as a fourth, novel verb for this concept
rather than matching the existing two-instance "designed, prototyped, or
(partially) tested" anchor). Net: Candidate 1 achieves marginally tighter
cross-section terminology alignment than Candidate 2.

## 9. Authorial Voice

CURRENT's closing sentence is measurably more normative/prescriptive in
register ("should not be trusted... without also accounting for") than
every other place in the manuscript that states the identical idea
(Contribution Statement lines 226-247, Discussion lines 1236-1242, Future
Work lines 1344-1349), all of which use strictly descriptive/hypothesis
framing -- this is the exact register gap the prior CONDITIONAL audit's
Section 9 independently identified. Both candidates pull the abstract's
register toward that same descriptive framing used everywhere else in the
paper ("is the direct next hypothesis" / "is an open question... this
experiment motivates"), closing the voice gap. Candidate 1 closes it more
completely, via near-verbatim phrase reuse; Candidate 2 closes it
substantively but with slightly more distinct (not anchor-matching)
vocabulary.

## 10. Scientific Guardrail Verification

Checked directly against the current manuscript state (unedited) and both
hypothetical candidates:

1. H1 = PARTIALLY_SUPPORTED -- confirmed unchanged at lines 1260, 1406; not
   mentioned in the abstract's closing sentence in CURRENT or either
   candidate. PASS.
2. 6a/6b separation -- confirmed intact at lines 897-936 (Sec.5.2 "ADS
   Predicts Individual Mechanism Accuracy" / Sec.5.3 "ADS Does Not Predict
   Mechanism Ranking"); neither candidate merges or blurs these -- both
   candidates' core clause restates only the 6b half (ranking-prediction
   failure), matching CURRENT's scope exactly. PASS for both.
3. No "ADS predicts mechanism ranking" claim -- neither candidate asserts
   this; both explicitly assert the opposite ("should not be used/trusted
   to predict which mechanism will win"). PASS for both.
4. No universal/general-purpose mechanism-selection claim -- neither
   candidate broadens scope beyond the tested selector; both retain "here"
   / rely on the preceding abstract sentence's explicit generator/lexical-
   model/production-case-study scoping. PASS for both.
5. No novelty inflation -- not implicated by either candidate; neither uses
   "novel," "robust," "generalizable," "validated," "superior," "optimal,"
   "reliable" (as an assertion, rather than inside an explicitly-hedged
   "whether... would restore reliable/that reliability" question), "proves,"
   "demonstrates," or "establishes." Both candidates' one appearance of
   "reliable"/"reliability" sits strictly inside an unanswered "whether X
   would restore Y" clause, not as an assertion that reliability exists or
   would be achieved. PASS for both, with the "restore" word-choice note
   from Section 4 recorded as a precision item, not a guardrail violation.
6. Production/client data boundary -- not implicated; neither candidate
   mentions production data. PASS for both.
7. Canonical numbers -- not implicated; neither candidate contains a
   number. PASS for both.
8. No statistical-interpretation strengthening -- neither candidate swaps
   "suggests"->"shows" or similar; if anything both candidates add a layer
   of explicit hedging ("is the direct next hypothesis" / "is an open
   question... does not... answer") to the future-direction half that
   CURRENT expressed with a comparatively terser trailing hedge. PASS for
   both, hedging strengthened not weakened.
9. Scope/uncertainty language survives -- both candidates retain and, per
   Section 4 above, structurally reinforce (not merely repeat) the "not
   built or tested here" disclaimer; this is an improvement over CURRENT
   on exactly the dimension the prior CONDITIONAL audit flagged as
   deficient. PASS for both.
10. No unsupported claim smuggled in via stylistic rewriting -- checked
    word-by-word; the only genuinely new word in either candidate not
    traceable to existing manuscript language is "restore" (Section 2B,
    Section 4), which sits inside an explicitly unanswered question and
    does not itself assert a fact. No number, mechanism label, or citation
    changed. PASS for both, "restore" flagged as a precision note.

## 11. Regression Check

Compared directly against the prior
`research/E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md` (read in full
before being overwritten -- see Section 1). That report's Section 12 item 1
was the specific open item this task addresses: "Re-examine the abstract
closing sentence specifically for the sufficiency implicature identified in
Section 4B... consider whether the trailing hedge should extend beyond 'not
something built or tested here' to also foreclose the 'would work if
built' inference -- for example taking a cue from the Discussion's own 'it
does not follow that a fix exists' framing or Section 8.1's 'is the direct
next hypothesis, named only' framing." Independently verified here: both
candidates do exactly this, restructuring the future-direction half of the
sentence into an explicit "whether X would work is an untested open
question/hypothesis" form rather than a "without also accounting for X"
dependent clause, and Candidate 1 specifically reuses the Section 8.1 "is
the direct next hypothesis this experiment motivates" phrase the prior
report suggested drawing on. This is a direct, independently-confirmed
resolution of that prior report's Section 12 item 1, not a reopening or
regression of it.

No new regression found elsewhere: `git diff --stat manuscript/main.tex`
still shows only the same 3-line E7.5-A punctuation diff already reviewed
and passed in `research/E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md`; that PASS
verdict remains valid and unaffected by this pass. The prior CONDITIONAL
report's Section 12 item 2 (the six Section 2 disclaimer sentences, KEEP-
all-six with item 365 flagged as the weakest-justified) is outside this
task's scope and is carried forward unchanged, still open, still not
re-actioned.

## 12. Verdict

ORANGE -- CONDITIONAL.

Justification: Both candidates are, independently, genuine and directionally
correct fixes for the specific sufficiency-implicature risk the prior
CONDITIONAL audit identified in CURRENT, matching CONTRIBUTION_LOCK.md
Sec.5 Formulation #3's own named "biggest risk" (conflating a found
limitation with a validated fix). Neither candidate strengthens the core
scientific claim, alters scope, weakens H1's PARTIALLY_SUPPORTED status,
blurs the 6a/6b distinction, or removes any existing hedge -- both add
hedging precision specifically to the part of CURRENT that was under-hedged,
and both improve terminology alignment with three other passages in the
document ("predict which mechanism will win/wins"). No Step 2 guardrail is
violated by either candidate. This clears the specific risk to a PASS-level
outcome on the science and hedging dimensions.

The verdict is CONDITIONAL rather than a clean GREEN for two reasons, both
requiring a human decision rather than being blocking defects: (1) a choice
between two viable candidates is still open, and my independent assessment
is that Candidate 1 is the marginally safer and better-anchored of the two
(full sentence break rather than a semicolon, and near-verbatim reuse of
the manuscript's own already-vetted "is the direct next hypothesis this
experiment motivates" / "designed, prototyped, or tested" phrasing from
Discussion 1236-1237/1227 and Future Work 1346-1349, versus Candidate 2's
close-but-not-exact "test, prototype, or answer" triplet); (2) both
candidates introduce the word "restore" ("restore reliable prediction" /
"restore that reliability"), which does not appear anywhere else in the
manuscript and carries a mild, avoidable presupposition that ranking
prediction was reliable prior to this finding and would be "restored" --
this sits inside an explicitly unanswered hypothetical clause in both
candidates and is not a guardrail violation, but is a precision issue
neither candidate resolves and the task framing did not flag.

For the human author to decide/fix, in priority order:

1. (Requires a decision) Choose between Candidate 1 and Candidate 2, or a
   hybrid. Recommended direction: Candidate 1, on the strength of (a) the
   full sentence break more completely severing the necessity/sufficiency
   implicature than Candidate 2's semicolon, and (b) its closer textual
   alignment with the manuscript's own already-vetted Discussion/Future-
   Work phrasing for this identical idea.
2. (Optional, low priority, applies to whichever candidate is adopted)
   Consider replacing "would restore reliable prediction" / "would restore
   that reliability" with phrasing that does not presuppose a prior state
   of reliability -- e.g. language closer to "would predict the winning
   mechanism reliably" or "would close this gap" -- since Experiment 1 as
   reported does not establish that ranking prediction was ever reliable
   in the first place. Not a guardrail violation as currently worded
   (it sits inside an unanswered "whether" clause in both candidates), but
   an avoidable precision gap neither candidate currently closes.
3. (Carried forward, unaffected by this task, still open) The prior
   CONDITIONAL report's item on the six Section 2 "We do not claim..."
   disclaimers (item 365 as the single lowest-priority candidate for
   optional variation) remains open and unactioned; out of scope for this
   pass.
