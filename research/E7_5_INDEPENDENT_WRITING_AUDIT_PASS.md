# E7.5 Independent Research Writing & Originality Audit

## 1. Scope

This is the final staging-readiness audit for E7.5, not a candidate review and not a dry
run. It reviews the actual, currently uncommitted diff in the working tree of
manuscript/main.tex on top of RC1 (commit f3501b6), verified fresh this session via
git status --porcelain and git diff --stat -- manuscript/main.tex before reading any prior
report or accepting any framing from the parent session. This report overwrites the prior
research/E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md at this filename (Step 5 permits overwriting
when re-running the same bounded review; this pass reviews the identical diff that prior report
covered, now specifically as a staging gate). E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md and
E7_5_INDEPENDENT_WRITING_AUDIT_ABSTRACT_RESTORE_PASS.md are left in place as historical record
of the candidate-evaluation chain; their scope (hypothetical, not-applied variant text) differs
from this reports scope (the real, currently-staged text).

Ground truth established independently, this session:

- git status --porcelain: only manuscript/main.tex is modified (tracked); all other entries
  are untracked research/*.md audit files, out of scope.
- git diff --stat -- manuscript/main.tex: 1 file changed, 8 insertions(+), 6 deletions(-).
- git diff --stat (no path filter): identical output, confirming no other file in the repository
  is touched by this diff.
- Full git diff -- manuscript/main.tex, read directly: exactly three hunks. (1) The abstracts
  closing two sentences (3 lines removed / 5 lines added). (2) Two semicolon-to-period
  conversions in the production-case-study paragraph of Section 1.1 (2 removed / 2 added). (3)
  One semicolon-to-period conversion in the general-pattern paragraph, also Section 1.1 (1
  removed / 1 added). Sum: 6 removed / 8 added, matching git diff --stat exactly. No other line
  in the 1481-line file is touched.
- Section-header structure verified via direct grep of \section/\subsection (not assumed):
  Section 1.1 is "Real-World Motivation and General Problem," spanning lines 101-147, which
  contains all three punctuation hunks. This confirms the parent sessions characterization of
  "three semicolon-to-period edits in Section 1.1" as accurate.
- Full abstract read directly (manuscript/main.tex lines 62-95), Section 1.1 in full (lines
  101-147), Results Section 5 in full (lines 872-1109, including both 6a/6b subsections and the
  Summary of Findings), Discussion "Implications for Practice and Future Selector Design" (lines
  1221-1248), Limitations in full (lines 1252-1338), Future Work Section 8.1 (lines 1342-1353),
  Conclusion (lines 1398-1421), and Reproducibility Statement (lines 1425-1441).
- research/PAPER_CONTRACT.md read in full (all 13 sections).
- research/CONTRIBUTION_LOCK.md Sections 5, 6, 7, 8, 9, 10, 11 read directly (not inherited from
  any prior reports quotations).
- research/EVIDENCE_BASELINE.md grepped directly for every canonical figure cited in the diff
  and elsewhere in the manuscript.
- All three pre-existing research/E7_5_INDEPENDENT_WRITING_AUDIT_*.md reports read in full as
  regression baseline (Section 11 below), used as a baseline, not as a substitute for
  independent re-derivation.

## 2. Independent Findings

### A. The abstract edit, read in full context

REMOVED (per git diff, confirmed matches the CURRENT text recorded in the two earlier candidate
reports as the pre-edit baseline):

"We conclude that a design-time selector built on historical consistency alone should not be
trusted to pick the better-performing mechanism without also accounting for representation
stability -- a direction for future work, not something built or tested here."

ADDED (verified by direct read of the current file, lines 81-86, not diff-inferred):

"We conclude that a design-time selector built on historical consistency alone should not be
used to predict which mechanism will win. Whether a selector that also conditions on a measured
representation-stability signal would reliably predict which mechanism wins is the direct next
hypothesis this experiment motivates: no such selector was designed, prototyped, or tested
here."

Independent semantic read of the two versions (not inherited from any prior reports framing):
the removed sentence phrases the two-feature-selector idea as a dependent clause of a "should not
be trusted to do Y without also accounting for X" construction. Read as ordinary English, this
carries a natural implicature that doing X would be sufficient to make Y trustworthy -- i.e.,
that a selector which does account for representation stability would work. The added text
removes this by restructuring the same idea into a fully separate, explicitly interrogative
sentence ("Whether X would ... is the direct next hypothesis ... : no such selector was
designed, prototyped, or tested here"), which asserts nothing about whether such a selector would
succeed and immediately forecloses the reading that it was built, prototyped, or tested. This is
a hedging strengthening on the future-direction half of the sentence, not a weakening, and the
core 6b-adjacent claim in the first sentence ("should not be used to predict which mechanism
will win") is a direct restatement of the negative finding using the manuscripts own established
idiom (see Section 8 below), not a new or different claim.

### B. Direct verification against CONTRIBUTION_LOCK.md

CONTRIBUTION_LOCK.md Sec.5, Formulation #3 (the "moderate" formulation, explicitly not the
locked contribution), "Required qualification" column, read directly: "Repeated, explicit 'not
built, not tested here' framing every time the two-feature idea is mentioned." The added
sentence satisfies this exactly: "no such selector was designed, prototyped, or tested here."

CONTRIBUTION_LOCK.md Sec.10 (Future work), first bullet, read directly: "A decision rule that
conditions mechanism selection on both realized ADS and a measured (not assumed)
lexical/representation-stability signal -- the direct next hypothesis this experiment
motivates (Formulation #3, Sec.5, deliberately not adopted as the current claim)." The added
abstract sentences phrase "is the direct next hypothesis this experiment motivates" is a
verbatim reuse of this already-locked wording, not new invented phrasing. This is a positive
terminology-fidelity finding: the abstract edit pulls its forward-looking sentence directly from
already-vetted, locked project language rather than introducing a new formulation that would need
fresh scrutiny.

CONTRIBUTION_LOCK.md Sec.11.E (locked one-sentence future direction), read directly: "A natural
next step is a decision rule that conditions on both historical consistency and a measured
representation-stability signal, though no such rule was built or tested here." Descriptive, not
prescriptive -- the added abstract sentence matches this register (a "whether X would work" open
question) rather than the removed sentences more normative "should not be trusted ... without
also accounting for."

### C. Direct verification against PAPER_CONTRACT.md forbidden-claims list

PAPER_CONTRACT.md Sec.3, row 12: "'A design-time selector should account for representation
stability' stated as demonstrated/built" is forbidden, because "The two-feature idea (Formulation
#3) was never built or tested -- explicitly NOT RECOMMENDED, named only as future work." The added
sentence is grammatically an interrogative noun clause ("Whether X would ... is the direct next
hypothesis") functioning as the subject of "is," not an assertion that X does or would predict Y.
It does not claim the two-feature selector should exist, would work, or was built -- it names an
open, explicitly unbuilt hypothesis. This is not the forbidden form.

PAPER_CONTRACT.md Sec.3, row 13: "'ADS predicts mechanism suitability' (unqualified -- collapsing
accuracy-prediction and ranking-prediction into one claim)" is forbidden. The sentence
immediately preceding the two edited closing sentences (unedited, confirmed present and unchanged
in this sessions direct read) already states the 6a/6b distinction explicitly with a contrastive
"but": "Realized historical consistency is strongly correlated with each mechanisms own accuracy
... but it does not predict which mechanism wins." The edited closing sentences address only the
6b (ranking) half and do not re-collapse it with the 6a (accuracy) half.

### D. Independent word-level check for flagged risk words

Grepped directly against the current file (not inherited): "restore" -- zero matches anywhere in
manuscript/main.tex. This confirms the added text does not contain the "restore reliable
prediction" construction that an earlier report in this chain flagged as carrying an avoidable
presupposition (that ranking-prediction was ever reliable to begin with). "reliably predict" --
one match, at line 84, sitting strictly inside the unanswered "Whether X would ..." clause, not
as a standalone assertion. "designed, prototyped" -- three matches: the abstract (line 86),
Discussion line 1229 ("was designed, prototyped, or tested anywhere in this repository"), and
Limitations line 1327 (same phrasing). The abstracts three-verb disclaimer matches the
manuscripts own established phrasing in two other sections almost verbatim.

## 3. Proposed/Implemented Edit Review

EDIT ID: E7.5-STAGING-1 (abstract closing-sentence replacement)
LOCATION: manuscript/main.tex, Abstract, lines 81-86 (currently staged, uncommitted)
ORIGINAL: "We conclude that a design-time selector built on historical
consistency alone should not be trusted to pick the better-performing
mechanism without also accounting for representation stability -- a
direction for future work, not something built or tested here."
PROPOSED (STAGED): "We conclude that a design-time selector built on
historical consistency alone should not be used to predict which
mechanism will win. Whether a selector that also conditions on a measured
representation-stability signal would reliably predict which mechanism
wins is the direct next hypothesis this experiment motivates: no such
selector was designed, prototyped, or tested here."
SEMANTIC INVARIANT:
A. Original claims: (i) a consistency-only selector should not be trusted
to pick the winner; (ii) this untrustworthiness is conditioned on
"without also accounting for representation stability," a construction
that carries a natural sufficiency implicature; (iii) a two-verb
"built or tested" hedge.
B. Proposed claims: (i) the identical core 6b finding, restated with the
manuscripts own repeated idiom "predict which mechanism wins/will win"
(used elsewhere at abstract line 73, Results Sec.5.3 line 927, Results
Sec.5.6 line ~1101, and Conclusion line 1406); (ii) the two-feature-
selector idea is moved into a fully separate, explicitly interrogative
sentence, removing the grammatical adjacency that produced the
sufficiency implicature in A(ii); (iii) a three-verb "designed,
prototyped, or tested" hedge, matching phrasing used verbatim/near-
verbatim elsewhere (Discussion line 1229, Limitations line 1327) and
lifted directly from CONTRIBUTION_LOCK.md Sec.10 locked wording.
C. Evidence: (i) is the locked 6b finding (CONTRIBUTION_LOCK.md Sec.6;
manuscript Results Sec.5.3, lines 925-938, untouched by this diff); (ii)
is supported only as an open, untested hypothesis by CONTRIBUTION_LOCK.md
Sec.10/Sec.11.E and PAPER_CONTRACT.md Sec.3 row 12 required framing,
both of which the staged text now echoes rather than diverges from.
D. Scope: unchanged. Neither sentence itself restates the generator/
lexical-model/production-case-study scope; both rely on the immediately
preceding, unedited abstract sentence for that qualifier, confirmed
present and untouched.
E. Hedging: strengthened on the future-direction half.
F. A vs B differ only on the future-direction half (ii/iii): a hedging
strengthening, not a claim, scope, or evidentiary-basis change.
EVIDENCE RELATIONSHIP: unchanged for the core claim; improved for the
future-direction claim -- now aligned with, rather than diverging from,
CONTRIBUTION_LOCK.md Sec.10/Sec.11.E locked wording.
CLAIM STRENGTH: unchanged for the core claim; weaker/more-hedged for the
future-direction claim -- the correct direction relative to
PAPER_CONTRACT.md Sec.3 row 12 named forbidden claim.
SCOPE: unchanged.
HEDGING: strengthened (three-verb disclaimer; sufficiency implicature
structurally removed).
SOURCE-OVERLAP RISK: none -- original synthesis prose restating the
papers own locked finding (6b) and its own already-published
future-work framing; the reused phrases are intra-document
self-consistency, not external-source paraphrase.
WRITING QUALITY: Splits one ~40-word sentence carrying two subordinate
clauses into two shorter, more parseable sentences; reuses the
manuscripts own established idiom for the 6b finding rather than a
one-off phrase; pulls the abstracts register into closer alignment with
the Discussion and Future Work sections already-descriptive treatment
of the same idea. Minor, non-blocking stylistic note: "predict which
mechanism wins/will win" now appears twice within the edited closing
sentences alone (plus once earlier in the same abstract paragraph, three
times total in a ~230-word abstract) -- classified as (B) useful but
stylistically repetitive per the Step-4 taxonomy, not (C) unnecessary,
given this is the papers single central finding.
VERDICT: PASS
REASON: Resolves a genuine sufficiency-implicature risk in the removed
wording, matches CONTRIBUTION_LOCK.md/PAPER_CONTRACT.md explicit
required framing for the two-feature-selector idea (open hypothesis,
explicitly not built/prototyped/tested), does not weaken the core 6b
claim, does not touch scope, and strengthens rather than loosens the
trailing hedge.

EDIT ID: E7.5-STAGING-2 (Section 1.1 punctuation conversions x3)
LOCATION: manuscript/main.tex, Section 1.1, lines 107, 112, and 138
ORIGINAL: three semicolons, each followed by a lowercase word starting a
new independent clause ("mechanism; in", "Section~3.3); no",
"(Section~2); what").
PROPOSED (STAGED): each semicolon replaced by a period with the following
word capitalized ("mechanism. In", "Section~3.3). No", "(Section~2).
What"). No word added, removed, or reordered in any of the three.
SEMANTIC INVARIANT: A-F unchanged in every respect -- purely mechanical
sentence-boundary punctuation; no claim, scope, evidence relationship, or
hedge is touched.
EVIDENCE RELATIONSHIP: unchanged. CLAIM STRENGTH: unchanged. SCOPE:
unchanged. HEDGING: unchanged. SOURCE-OVERLAP RISK: none.
WRITING QUALITY: Splits three long, semicolon-joined compound sentences
into shorter independent sentences, improving readability without
altering content.
VERDICT: PASS
REASON: Purely mechanical punctuation edit with zero semantic footprint.

## 4. Semantic-Invariant Checks

Both edit units pass the Step-3 A-F test. The abstract edits only directional change is a
hedging strengthening on the future-direction half of the sentence (removal of a sufficiency
implicature, addition of a third disclaimer verb); the core 6b claim, evidentiary basis, and
scope are unchanged in substance across both the removed and added text. The punctuation edits
carry zero semantic change of any kind. No claim anywhere in the diff is stronger, broader, or
less hedged than what it replaces.

## 5. Source-Overlap / Originality Findings

Not applicable to either edit unit. Both are the papers own synthesis prose restating its own
already-locked finding (6b, CONTRIBUTION_LOCK.md Sec.6) and its own already-published future-work
framing (CONTRIBUTION_LOCK.md Sec.10-11.E) or purely mechanical punctuation. The phrase reuse ("is
the direct next hypothesis this experiment motivates," "designed, prototyped, or tested," "predict
which mechanism wins") is intra-document self-consistency with the Discussion, Limitations, and
Future Work sections of this same manuscript and with CONTRIBUTION_LOCK.md own locked wording --
not a plagiarism or close-paraphrase risk against any external cited source. No external source
is implicated by either edit unit.

## 6. Formulaic Language Findings

The abstract edits reuse of "predict which mechanism wins/will win," "is the direct next
hypothesis this experiment motivates," and "designed, prototyped, or tested" is classified, per
the Step-4 dimension-4 taxonomy, as (A) scientifically/register-necessary repetition -- it anchors
the abstracts forward-looking sentence to the same idiom already used for the underlying finding
and the same idiom already used in Discussion, Limitations, and Future Work, aiding a readers
ability to track one concept across the document. The idiom "predict which mechanism wins" now
appears three times within the ~230-word abstract itself -- (B) useful but stylistically
repetitive, not (C) unnecessary, given its status as the papers single central negative finding.
No new instance of the "We do not claim..." disclaimer-scaffolding pattern (flagged as an
out-of-scope, still-open item in earlier reports in this chain) is introduced by either edit unit;
that item is unrelated to this diff and remains untouched.

## 7. Readability & Articulation Findings

The abstract edit splits one ~40-word sentence carrying two subordinate clauses into two shorter,
more directly parseable sentences, with no content loss. The three Section 1.1 punctuation edits
perform an analogous split at the mechanical level for three other long, semicolon-joined
sentences, each improving readability without altering content. No new unparseable construction,
ambiguous referent, or unnecessary passive voice was introduced by either edit unit. One minor
observation, noted independently in this sessions own reading rather than inherited: the
Discussions parallel sentence about the same future-direction idea (line 1238, "The natural next
step this experiment motivates is a decision rule that...") uses slightly different phrasing from
the abstracts and Future Work Sec.8.1 "is the direct next hypothesis this experiment
motivates." This is a minor, non-blocking stylistic variance across three near-parallel
restatements of the same idea, not a semantic drift -- all three convey an identical, equally
hedged, unbuilt-hypothesis framing.

## 8. Terminology Consistency

Independently re-derived via direct grep of the current file (not inherited from any prior
report): "predict which mechanism wins/will win" appears at abstract line 73 (unedited), abstract
line 82 (edited, part of the core-claim restatement), abstract line 84 (edited, inside the
open-hypothesis clause), Results Sec.5.3 line 927 ("Realized ADS does not predict which mechanism
wins"), Results Sec.5.6 line ~1101, and Conclusion line 1406 -- six total occurrences, confirming
this is the manuscripts dominant, well-anchored idiom for the 6b finding both before and after
this diff. "Designed, prototyped, or tested" now matches Discussion line 1229 and Limitations line
1327 almost exactly (three-verb form), tighter than the removed texts looser two-verb "built or
tested." "Restore" -- the specific risk word an earlier report in this chain flagged against a
hypothetical candidate -- does not appear anywhere in the staged text or elsewhere in the file. No
terminology drift identified in either edit unit; ADS, 6a/6b, H1, "empirical winner," and R3 usage
elsewhere in the file is entirely unaffected.

## 9. Authorial Voice

The abstracts closing sentences now match the strictly descriptive, hypothesis-framed register
used throughout Discussion ("Implications for Practice and Future Selector Design"), Limitations
("No Selector Fix and Limited Generalization"), and Future Work ("Representation-Stability-Aware
Selectors") for this identical idea, closing a register gap between the abstracts previously more
normative phrasing ("should not be trusted ... without also accounting for") and the rest of the
papers consistently descriptive treatment of the same open question. The Section 1.1 punctuation
edits are register-neutral. No abrupt shift in vocabulary, rhythm, or formality is introduced
anywhere in this diff; the manuscript reads as one coherent voice before and after.

## 10. Scientific Guardrail Verification

Checked directly against the current (post-diff) manuscript state, independently, not inherited
from any prior reports verdict:

1. H1 = PARTIALLY_SUPPORTED -- confirmed unchanged and untouched by this diff. Direct grep
   confirms "H1 (revised) is only partially supported, matching the pre-registered ... row of the
   falsification table exactly" (line 1262-1263) and "H1 overall is only partially supported, not
   confirmed" (Conclusion, line 1408) both survive verbatim. H1 is not named in either edited
   passage. PASS.
2. 6a/6b separation -- confirmed intact. Results Sec.5.2 ("ADS Predicts Individual Mechanism
   Accuracy," lines 899-913) and Sec.5.3 ("ADS Does Not Predict Mechanism Ranking," lines
   925-938) remain two distinct, separately-headed subsections, entirely outside any diff hunk
   (which stops at line ~139). The edited abstract sentences restate only the 6b half and rely on
   an unedited, immediately-preceding sentence in the same paragraph for the explicit 6a/6b
   contrast. PASS.
3. No claim that any signal predicts mechanism ranking -- the edited first sentence explicitly
   asserts the negative; the second sentence poses the two-feature selectors success as an
   unanswered question, immediately foreclosed by the disclaimer. No sentence anywhere in the
   file asserts that any signal, alone or in combination, does predict ranking. PASS.
4. No implication a two-feature selector would succeed if built -- the "Whether X would ... is
   the direct next hypothesis" construction is a grammatical interrogative, not a predictive
   assertion, and is immediately followed by the disclaimer. Matches PAPER_CONTRACT.md Sec.3 row
   12 required framing exactly. PASS.
5. No causal, novelty, or universal claim -- file-wide grep for
   novel/robust/generalizable/validated/superior/optimal/reliable/proves/demonstrates/establishes
   shows every self-referential instance is explicitly negated ("no claim that ADS is a novel
   metric," "not a novel contribution," "not claimed superior," "not a validated method"); the
   diff itself introduces none of these words except "reliably," which sits strictly inside the
   unanswered hypothetical clause discussed in item 4. PASS.
6. Experimental scope preserved -- the abstract sentence immediately preceding the edited
   closing sentences ("This finding is scoped to one synthetic generator, one lexical-perturbation
   model, and one motivating (non-evidentiary) production case study; it is not a deployment or
   generalization claim") is outside any diff hunk and confirmed byte-for-byte unchanged.
   PAPER_CONTRACT.md Sec.6 generator/mechanism/lexical-perturbation/factorial-design scope
   boundaries are untouched anywhere in the file. PASS.
7. Production/client data boundary intact -- the "(non-evidentiary)" qualifier survives at
   abstract line 80 and Discussion line 262 (both unedited); the confidential/
   not-independently-reproducible qualifier survives at every citation site (lines 119, 593, 822,
   1138, 1310, 1433), none of which is touched by this diff. PASS.
8. Canonical statistics unchanged file-wide -- grepped directly: 91.2%, 87.56%, 0.847, 0.964,
   32/50 (as "32 of 32" and the 64.0% aggregate), 64.0%, and Pearson r values 0.909/0.959 (rules)
   and 0.948/0.955 (retrieval) all appear exactly as specified in PAPER_CONTRACT.md Sec.7 and
   EVIDENCE_BASELINE.md. No superseded value (0.8094, 0.9310, 84.12%, or the ~55,394 mapping
   count) appears anywhere in the file (confirmed via file-wide grep, zero matches). PASS.
9. No statistical-interpretation strengthening -- neither edit unit swaps "suggests" to "shows" or
   similar; the future-direction hedge is strengthened, not weakened, by the diff. PASS.
10. No unsupported claim smuggled in via stylistic rewriting -- checked word-by-word for the
    abstract edit; the only words not already anchored elsewhere in the manuscript are minor
    connective/grammatical words, and "reliably" is the sole watch-listed term, used inside an
    unanswered hypothetical. Nothing asserts a new fact. PASS.

## 11. Regression Check

Compared directly against all three prior research/E7_5_INDEPENDENT_WRITING_AUDIT_*.md reports,
each read in full before this session drew its own conclusions:

- The prior ..._PASS.md (now overwritten by this report) independently reviewed this exact same
  8-insertion/6-deletion diff and reached GREEN -- PASS, with the same diff-stat, the same
  three-hunk breakdown, and substantively the same guardrail findings this session independently
  re-derived. No regression: this sessions independent re-derivation reaches the same conclusion
  through its own direct reads of manuscript/main.tex, PAPER_CONTRACT.md, and
  CONTRIBUTION_LOCK.md, not by inheriting that reports text.
- ..._CONDITIONAL.md raised the sufficiency-implicature risk in the pre-edit ("CURRENT") abstract
  wording ("should not be trusted ... without also accounting for X") and a word-choice
  presupposition risk ("restore"). Both are resolved in the currently staged text: the
  implicature is removed by the two-sentence restructuring, and "restore" does not appear
  anywhere in the staged text (confirmed by direct grep, zero matches).
- ..._ABSTRACT_RESTORE_PASS.md independently ranked a "Variant 2" phrasing ("...would reliably
  predict which mechanism wins is the direct next hypothesis...") as the safest, best-anchored
  candidate. Direct word-for-word comparison this session confirms the currently staged text is
  exactly this phrasing. No regression from that recommendation.
- One minor, non-blocking discrepancy independently identified in this sessions own reading, not
  present in any prior reports specific claim: the Discussions parallel sentence (line 1238)
  phrases the same future-direction idea as "The natural next step this experiment motivates is
  ...," not "is the direct next hypothesis this experiment motivates" as the abstract and Future
  Work Sec.8.1 both do. This is a pre-existing minor phrasing variance across three near-parallel
  restatements of the same idea (not introduced or worsened by this diff, since Discussion line
  1238 is entirely outside any diff hunk) and carries no semantic or guardrail consequence.

No regression found anywhere. Every item flagged as open or unresolved by the earlier reports in
this chain (the sufficiency implicature, the "restore" presupposition) is resolved in the
currently staged text; the one item those reports left carried-forward and out of scope (six
Section 2 "We do not claim..." disclaimer sentences) remains untouched by this diff and is not
re-actioned here, consistent with this tasks stated scope.

## 12. Verdict

GREEN -- PASS. This diff is safe to stage/commit from a writing-integrity standpoint.

Justification: Independent re-derivation, not inheritance, confirms git diff --stat --
manuscript/main.tex shows changes in exactly one file, exactly two categories of change (the
abstracts closing-sentence replacement and three semicolon-to-period conversions in Section
1.1), and no other line in the 1481-line manuscript is touched. The abstract edit resolves a
genuine sufficiency-implicature risk in the prior wording, matches CONTRIBUTION_LOCK.md Sec.5/
Sec.10/Sec.11.E and PAPER_CONTRACT.md Sec.3 rows 12-13 explicit requirements for how the
untested two-feature-selector idea must be framed (open hypothesis, explicitly not built,
prototyped, or tested), strengthens rather than weakens the trailing hedge, and reuses the
manuscripts own already-locked language rather than inventing new formulations. The 6a/6b
distinction and H1 PARTIALLY_SUPPORTED status are both entirely outside this diffs hunks and
confirmed unchanged. No claim anywhere in the file asserts that ADS, or any signal, predicts
mechanism ranking; no implication exists that a two-feature selector would succeed if built.
Every canonical number checked (91.2%, 87.56%, 0.847, 0.964, 32/50, 64.0%, both sets of Pearson
r values) matches PAPER_CONTRACT.md Sec.7 and EVIDENCE_BASELINE.md exactly, with zero superseded
values present anywhere in the file. The production-data confidentiality/non-reproducibility
qualifier and the "(non-evidentiary)" scope qualifier both survive intact at every citation site.
The three punctuation conversions are purely mechanical with zero semantic footprint. No
source-overlap, plagiarism, or attribution risk was identified in either edit unit -- both are
the papers own synthesis prose reusing its own already-locked wording.

No items require human decision or fix before staging; nothing in this diff is blocking. The one
carried-forward, out-of-scope item from earlier reports in this chain (the six Section 2 "We do
not claim..." disclaimer sentences) remains open but is unrelated to this diff and does not
affect this verdict.
