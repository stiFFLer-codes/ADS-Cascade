# E7.5 Independent Research Writing & Originality Audit

## 1. Scope

This report is scoped narrower than either existing E7.5 report in this
directory and does not overwrite either of them. It evaluates exactly three
hypothetical replacement clauses ("Variant 1/2/3") for a single sub-clause
inside Candidate 1 of the abstract's closing sentence -- the clause
"would restore reliable prediction" -- proposed to fix a specific precision
issue (an unwanted presupposition that a prior reliable ranking-prediction
state existed) that `research/E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md`
Section 12 item 2 raised against Candidate 1 as originally drafted. None of
this text -- Candidate 1, Candidate 2, or any of the three new variants --
is present in `manuscript/main.tex`; this is a review of hypothetical prose
only.

Filename choice, explained per this task's instruction to address
distinguishability: this review's scope (a single-clause word-choice fix
inside the abstract's closing sentence) partially overlaps the existing
`E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md` (same sentence, same
underlying risk item 2) but does not overlap
`E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md` at all (that report covers an
unrelated, already-committed-to-working-tree punctuation diff in Section
1.1, referred to there as "E7.5-A"). Overwriting the CONDITIONAL report
outright would destroy its still-partially-open item 1 (the Candidate 1 vs.
Candidate 2 choice, not re-litigated by this task) and its still-fully-open,
out-of-scope item 3 (the six Section 2 disclaimer sentences). Overwriting
the PASS report would incorrectly imply this review re-examined the
punctuation diff, which it did not. This report is therefore written under
a new, distinguishable filename that still carries the required verdict
suffix. The existing CONDITIONAL report's item 2 should be considered
resolved by this report's findings (Section 12 below); its items 1 and 3
remain open and are carried forward unchanged, not re-actioned here.

Ground truth verified fresh, this session, independent of the parent
session's framing: `git status --porcelain` and `git diff --stat
manuscript/main.tex` (still exactly `3 insertions(+), 3 deletions(-)`, the
same pre-existing E7.5-A punctuation diff, nothing else changed); a grep for
`"restore"`, `"achieve reliable prediction"`, `"would reliably predict"`,
`"succeed at predicting"`, and `"would restore"` across
`manuscript/main.tex` (zero matches for all -- confirms none of Candidate 1,
its "restore" clause, or any of the three new variants exists in the file);
the full abstract (`manuscript/main.tex` lines 62-85); the full section
header structure (grep for `\section`/`\subsection`, used to independently
verify subsection numbering rather than trusting any claimed location);
Results Sec.5.2/5.3 (lines 897-936) and Sec.5.6 "Summary of Findings" (lines
1096-1106); Discussion "Mechanistic Explanation" (lines 1173-1198) and
"Implications for Practice and Future Selector Design" (lines 1219-1242);
Future Work Sec.8.1 (lines 1344-1349); the Conclusion (lines 1396-1414);
`research/CONTRIBUTION_LOCK.md` Sec.5 (all four formulations, lines 183-190,
Formulation #3 row 3 read in full) and Sec.10-11 (lines 331-382); and both
prior E7.5 reports (`E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md` and
`E7_5_INDEPENDENT_WRITING_AUDIT_CONDITIONAL.md`), read in full as the
regression baseline for Section 11 below.

## 2. Independent Findings

### A. The base sentence and the three variants under review

CANDIDATE 1, as previously reviewed (unchanged base, not re-litigated):
"We conclude that a design-time selector built on historical consistency
alone should not be used to predict which mechanism will win. Whether a
selector that also conditions on a measured representation-stability signal
would restore reliable prediction is the direct next hypothesis this
experiment motivates: no such selector was designed, prototyped, or tested
here."

Only the clause "would restore reliable prediction" is replaced by each
variant; every other word in Candidate 1 is held constant across all three:

- VARIANT 1: "...would achieve reliable prediction is the direct next
  hypothesis this experiment motivates: no such selector was designed,
  prototyped, or tested here."
- VARIANT 2: "...would reliably predict which mechanism wins is the direct
  next hypothesis this experiment motivates: no such selector was designed,
  prototyped, or tested here."
- VARIANT 3: "...would succeed at predicting the winning mechanism is the
  direct next hypothesis this experiment motivates: no such selector was
  designed, prototyped, or tested here."

### B. Independent fact-check of the task framing's phrase-count claim

The task framing states the phrase "predict which mechanism wins" (or close
variants) "appears 3 times: abstract, Results, Discussion." This claim was
independently checked via grep and via the manuscript's actual
`\section`/`\subsection` structure, not accepted on faith. It is **not
accurate as stated**, on two counts:

1. The exact phrase "predict which mechanism wins" (in some inflection)
   actually appears **four** times, not three: abstract line 73 ("but it
   does not predict which mechanism wins"), Results Sec.5.3 line 925
   ("Realized ADS does not predict which mechanism wins"), Results Sec.5.6
   ("Summary of Findings") line 1099 ("it does not predict which mechanism
   wins"), and Conclusion line 1404 ("It does not predict which mechanism
   wins"). The task framing's count of 3 omits the Conclusion occurrence.
2. The location breakdown is also wrong: line 1099, which the task framing
   implicitly counts as "Discussion" (matching its 3-location list of
   abstract/Results/Discussion), is verified via the section-header grep
   (Section 2 findings above) to sit inside `\subsection{Summary of
   Findings}`, the last subsection of Section 5 (**Results**), immediately
   *before* `\section{Discussion}` begins two lines later at line 1108 --
   not inside the Discussion section at all. The phrase's actual
   distribution is: Abstract (1), Results (2: Sec.5.3 and Sec.5.6), Discussion
   (0), Conclusion (1).

This does not change any safety conclusion below -- if anything it
strengthens the case that "predict which mechanism wins" is the
manuscript's single, dominant, well-anchored idiom for the 6b finding (used
even more pervasively, and in one more section, than the task framing
claimed) -- but the human author should have the correct count and location
breakdown before relying on the "3 times" framing elsewhere.

### C. Independent vocabulary check for each variant's new words

Grepped directly against the full manuscript (not inferred):

- `"restore"`: zero matches anywhere in the current manuscript (confirms the
  prior CONDITIONAL report's finding, independently re-verified this
  session).
- `"reliab"` (matches reliable/reliably/reliability): two matches, both
  adverbial ("estimated reliably," lines 171 and 465), both about ADS
  measurement precision, not about ranking prediction. Neither is an
  assertion of ranking-prediction reliability.
- `"achieve"`: zero matches anywhere else in the manuscript. Variant 1
  introduces this as a genuinely new word for the document.
- `"succeed"`: two matches elsewhere ("succeeds and where it fails," line
  247; "R3 succeeds only where its own ADS-driven recommendation happens,"
  line 1044), both already used to describe exactly this kind of
  rule-performance framing. Variant 3's "succeed at predicting" reuses an
  already-established verb, though not in the exact "succeed at
  [gerund]-ing" construction.
- `"winning mechanism"`: zero matches anywhere else in the manuscript. The
  manuscript's own established term for this concept is "empirical winner"
  (ten occurrences: lines 240, 650, 721, 741, 756, 926, 928, 931, 934, 959)
  and the verb-phrase "predict which mechanism wins" (four occurrences).
  Variant 3's noun phrase "the winning mechanism" is a new construction
  that matches neither established form exactly.
- `"predict which mechanism wins"` (Variant 2's core reused phrase): four
  matches elsewhere (Section 2B above), including one in the very same
  abstract paragraph, two sentences earlier (line 73). Variant 2 is the only
  one of the three that reuses this exact phrase verbatim.

## 3. Proposed/Implemented Edit Review

```
EDIT ID: E7.5-C-1 (Candidate 1 restore clause vs. VARIANT 1)
LOCATION: manuscript/main.tex, Abstract closing sentence (hypothetical, not applied)
ORIGINAL: "...would restore reliable prediction is the direct next
hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
PROPOSED: "...would achieve reliable prediction is the direct next
hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
SEMANTIC INVARIANT:
A. Original claims: whether a two-feature selector, not built or tested,
would restore reliable prediction, lexically presupposing a prior state of
reliable ranking-prediction that would be brought back.
B. Proposed claims: whether the same untested selector would achieve
reliable prediction, a forward/creation-oriented verb carrying no
before-state presupposition. The predicate object (reliable prediction) is
unchanged; only the governing verb changes.
C. Evidence: sits inside an explicit Whether X ... is the direct next
hypothesis this experiment motivates scaffold, textually parallel to
Discussion lines 1236-1242 and Future Work Sec.8.1 lines 1344-1349. Neither
version is contradicted by any evidence here, since neither asserts a fact.
D. Scope: unchanged in both.
E. Hedging: unchanged in substance -- trailing not-built-or-tested
disclaimer is identical, word for word, in both.
F. A vs B differ only in whether the predicate verb carries a prior-state
presupposition; a precision correction, not a claim, scope, or hedging
change.
EVIDENCE RELATIONSHIP: unchanged.
CLAIM STRENGTH: unchanged.
SCOPE: unchanged.
HEDGING: unchanged; presupposition risk removed.
SOURCE-OVERLAP RISK: none.
WRITING QUALITY: achieve reliable prediction is a new two-word combination
for this document, grammatically clean and unambiguous in context, but the
least textually anchored of the three variants to existing vocabulary.
VERDICT: PASS
REASON: Removes the flagged presupposition without semantic drift on claim,
scope, or hedging; introduces one new, low-risk, unanchored word, a minor
stylistic cost, not a scientific or guardrail risk.
```

```
EDIT ID: E7.5-C-2 (Candidate 1 restore clause vs. VARIANT 2)
LOCATION: manuscript/main.tex, Abstract closing sentence (hypothetical, not applied)
ORIGINAL: "...would restore reliable prediction is the direct next
hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
PROPOSED: "...would reliably predict which mechanism wins is the direct
next hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
SEMANTIC INVARIANT:
A. Original claims: as in E7.5-C-1.
B. Proposed claims: whether the same untested two-feature selector would
reliably predict which mechanism wins -- no prior-state presupposition (the
adverb reliably modifies a forward-looking, hypothetical verb, not a
return-to verb), and the object of the verb is now the manuscript's own
four-times-repeated idiom for the 6b finding rather than a paraphrase of it.
C. Evidence: same scaffold as E7.5-C-1. Predict which mechanism wins is
independently verified (Section 2B/2C above) to be the document's own
established phrase for exactly this concept, used in the same abstract
paragraph two sentences earlier (line 73) and three further times in
Results/Conclusion -- the strongest internal-consistency anchor available.
D. Scope: unchanged, same reasoning as E7.5-C-1.
E. Hedging: unchanged in substance; the reliably adverb sits inside the
same untested whether-clause hypothetical as Candidate 1's original wording
and Variant 1, which the prior CONDITIONAL report already found not to be a
guardrail violation for the structurally identical case, since it does not
assert reliability, only poses it as an open question immediately followed
by an explicit not-built-or-tested disclaimer. Same reasoning applies here.
F. A vs B differ only in verb choice and object phrasing; precision and
anchoring improvement, not claim, scope, or hedging drift.
EVIDENCE RELATIONSHIP: unchanged; marginally improved traceability, since
the reused phrase points a reader directly back to the exact 6b finding
(Results Sec.5.3, line 925) rather than requiring anaphoric inference.
CLAIM STRENGTH: unchanged.
SCOPE: unchanged.
HEDGING: unchanged; presupposition risk removed, same as Variant 1.
SOURCE-OVERLAP RISK: none.
WRITING QUALITY: Introduces zero new vocabulary -- reuses reliably (already
used twice elsewhere) and predict which mechanism wins (already used four
times elsewhere) verbatim. Tightest cross-document terminology anchor of
the three variants and the only one requiring no anaphoric inference to
resolve its referent.
VERDICT: PASS
REASON: Removes the flagged presupposition, introduces no new vocabulary,
and achieves the strongest internal terminology consistency of the three
variants by reusing the manuscript's own dominant phrase for the 6b
finding, including within the same abstract paragraph two sentences prior.
```

```
EDIT ID: E7.5-C-3 (Candidate 1 restore clause vs. VARIANT 3)
LOCATION: manuscript/main.tex, Abstract closing sentence (hypothetical, not applied)
ORIGINAL: "...would restore reliable prediction is the direct next
hypothesis this experiment motivates: no such selector was designed,
prototyped, or tested here."
PROPOSED: "...would succeed at predicting the winning mechanism is the
direct next hypothesis this experiment motivates: no such selector was
designed, prototyped, or tested here."
SEMANTIC INVARIANT:
A. Original claims: as in E7.5-C-1.
B. Proposed claims: whether the same untested selector would succeed at
predicting the winning mechanism -- no prior-state presupposition (parallel
reasoning to Variants 1-2); notably the only one of the three that avoids
the Step-2 watch-listed word reliable/reliably entirely.
C. Evidence: same scaffold as E7.5-C-1/C-2. Succeed already appears twice
elsewhere in closely analogous rule-performance framing (line 247, line
1044), though not in the exact succeed-at-gerund construction used here.
The winning mechanism does not appear anywhere else in the manuscript; the
document's established terms for this concept are empirical winner (ten
occurrences) and which mechanism wins (four occurrences) -- this variant's
noun phrase is a near-miss relative to both.
D. Scope: unchanged, same reasoning as E7.5-C-1.
E. Hedging: unchanged in substance, same reasoning as E7.5-C-1/C-2. By
avoiding reliable altogether, this variant has zero exposure to the Step-2
watch-word list for this specific clause, a marginal additional safety
margin, though not one required by any actual guardrail violation in the
other two variants either.
F. A vs B differ only in predicate phrasing; precision improvement, not
claim/scope/hedging drift.
EVIDENCE RELATIONSHIP: unchanged.
CLAIM STRENGTH: unchanged.
SCOPE: unchanged.
HEDGING: unchanged; presupposition risk removed, same as Variants 1-2.
SOURCE-OVERLAP RISK: none.
WRITING QUALITY: Reuses an existing verb (succeed) but pairs it with a new
noun phrase (the winning mechanism) that does not match the manuscript's
two existing established terms for this concept -- a mild terminology
near-miss, comparable in kind (though smaller in degree) to the near-miss
the prior CONDITIONAL report flagged for Candidate 2's test-prototype-or-
answer triplet. Reads slightly more circuitous than Variant 2 for the same
propositional content.
VERDICT: PASS
REASON: Removes the flagged presupposition and avoids the Step-2 reliable
watch-word entirely, at the cost of a mild, non-blocking terminology
near-miss (the winning mechanism vs. the manuscript's established empirical
winner / which mechanism wins).
```

## 4. Semantic-Invariant Checks

All three variants are structurally identical at the Step-3 level: each
replaces only the governing verb (and, for Variants 2-3, minor complement
phrasing) inside a clause that was already, in Candidate 1, framed as an
explicitly unanswered "Whether X... is the direct next hypothesis this
experiment motivates: no such selector was designed, prototyped, or tested
here" question. None of the three touches the first sentence of Candidate 1
(the actual 6b restatement, "should not be used to predict which mechanism
will win"), none touches the trailing not-built-or-tested disclaimer, and
none touches anything outside this one clause. Claim strength, scope, and
the substance of hedging are unchanged across all three relative to
Candidate 1's original "restore" wording; the only thing that changes,
identically in direction across all three, is removal of "restore"'s
lexical presupposition that a prior reliable ranking-prediction state
existed -- a presupposition independently verified (via Results line 240
and the Conclusion, line 1406, "H1 overall is only partially supported, not
confirmed") to not be supported by the tested rule's actual performance
(100% agreement in one realized-ADS band, 0% in another -- not a state of
"reliability" in either direction to begin with). This is a pure precision
correction, confirmed to hold for all three variants, with no semantic
drift by the Step-3 A-F test.

## 5. Source-Overlap / Originality Findings

Not applicable to any of the three variants. All three are the paper's own
synthesis prose restating its own already-locked finding (6b) and its own
already-published future-work framing (CONTRIBUTION_LOCK.md Sec.10-11); no
external cited source's phrasing is implicated. Variant 2's reuse of
"predict which mechanism wins" and Variant 3's reuse of "succeed" are
intra-document self-consistency, not external-source overlap.

## 6. Formulaic Language Findings

None of the three variants introduces a new instance of the "We do not
claim..." disclaimer-scaffolding pattern flagged in the prior baseline/
CONDITIONAL audits. Variant 2's exact-phrase reuse is classified, per the
Step 4 dimension-4 taxonomy, as (A) scientifically/register-necessary
repetition -- it anchors the abstract's forward-looking hypothesis to the
same idiom used for the finding itself, aiding reader tracking of a single
concept across the document rather than being decorative padding. Variant
3's reuse of "succeed" is milder repetition, also (A)/(B) borderline-useful
rather than (C) unnecessary.

## 7. Readability & Articulation Findings

All three variants preserve Candidate 1's already-reviewed two-sentence
structure. Sentence length and clause count are essentially unchanged
across all three relative to Candidate 1's "restore" wording -- the edits
are single-clause word swaps, not restructuring. Variant 2 is the most
directly parseable (no anaphoric resolution required, since it names the
predicted object explicitly); Variant 1 requires the reader to resolve
"reliable prediction" back to the prior sentence's "predict which mechanism
will win," unambiguous in context but a small additional parsing step;
Variant 3's "succeed at predicting the winning mechanism" is the most
verbose of the three for equivalent content.

## 8. Terminology Consistency

Independently re-derived counts (Section 2B/2C above, not inherited from
the task framing) show "predict which mechanism wins" is the manuscript's
dominant idiom for the 6b finding (four occurrences: abstract, Results
Sec.5.3, Results Sec.5.6, Conclusion) and "empirical winner" is the
dominant noun-phrase term (ten occurrences, all in Results). Variant 2
matches the first exactly. Variant 3 matches neither exactly ("the winning
mechanism" is new). Variant 1 introduces "achieve," used nowhere else, as a
new but low-risk verb. Net: Variant 2 achieves materially tighter
cross-document terminology alignment than either Variant 1 or Variant 3, a
finding independently derived from this session's own greps rather than
from the parent session's (partially inaccurate) phrase-count claim.

## 9. Authorial Voice

No voice or register shift in any of the three -- all sit inside the same
already-reviewed hypothetical-question scaffold that the CONDITIONAL report
found (for Candidate 1 overall) to close the register gap between the
abstract and the Discussion/Future Work sections' consistently
descriptive/hypothesis-framed treatment of this same idea. That
register-alignment finding is unaffected by which of the three single-verb
substitutions is chosen; all three remain in the same descriptive,
non-prescriptive register as Candidate 1's base sentence.

## 10. Scientific Guardrail Verification

Checked directly against the current (unedited) manuscript state and all
three hypothetical variants:

1. H1 = PARTIALLY_SUPPORTED -- confirmed unchanged at Conclusion line 1406
   ("H1 overall is only partially supported, not confirmed"); not mentioned
   by name in Candidate 1 or any variant. PASS for all three.
2. 6a/6b separation -- confirmed intact at Results Sec.5.2/5.3 (lines
   897-936); none of the three variants merges or blurs these -- all three
   touch only the future-hypothesis clause, not the 6a/6b restatement in
   Candidate 1's first sentence. PASS for all three.
3. No "ADS predicts mechanism ranking" claim -- none of the three asserts
   this; Candidate 1's first sentence (unchanged by any variant) explicitly
   asserts the opposite. PASS for all three.
4. No universal/general-purpose mechanism-selection claim -- none of the
   three broadens scope; all retain "here" and the untested-hypothesis
   framing. PASS for all three.
5. No novelty inflation -- the Step-2 watch-word "reliable"/"reliably"
   appears in Variants 1 and 2 (not in Variant 3), in each case strictly
   inside an unanswered "whether X would [verb]" clause immediately
   followed by "no such selector was designed, prototyped, or tested here."
   This is the identical structural placement the CONDITIONAL report
   already independently evaluated for Candidate 1's original "restore
   reliable prediction"/"restore that reliability" and found not to be a
   guardrail violation, since it poses reliability as an open question
   rather than asserting it. Same reasoning applies unchanged to Variants 1
   and 2; Variant 3 avoids the word entirely and has zero exposure on this
   specific guardrail. PASS for all three, Variant 3 requiring the least
   reliance on this precedent-based reasoning.
6. Production/client data boundary -- not implicated by any variant. PASS
   for all three.
7. Canonical numbers -- not implicated by any variant; none contains a
   number. PASS for all three.
8. No statistical-interpretation strengthening -- none of the three swaps
   "suggests"->"shows" or similar; the not-built-or-tested hedge is
   identical, verbatim, in Candidate 1 and all three variants. PASS for all
   three.
9. Scope/uncertainty language survives -- the not-built-or-tested
   disclaimer is untouched by construction in all three. PASS for all
   three.
10. No unsupported claim smuggled in via stylistic rewriting -- checked
    word-by-word for each variant (Section 3 above); the only new words
    introduced are "achieve" (Variant 1), "reliably" plus reused "predict
    which mechanism wins" (Variant 2, no genuinely new word), and "succeed
    at" plus "the winning mechanism" (Variant 3). None asserts a new fact;
    all sit inside the same unanswered hypothetical. PASS for all three.

## 11. Regression Check

Compared directly against research/E7_5_INDEPENDENT_WRITING_AUDIT_
CONDITIONAL.md (read in full in Section 1 above before this narrower
review). That report's Section 12 item 2 was the specific open item this
task addresses: "Consider replacing 'would restore reliable prediction' /
'would restore that reliability' with phrasing that does not presuppose a
prior state of reliability... Not a guardrail violation as currently
worded, but an avoidable precision gap neither candidate currently closes."
Independently verified here: all three of the newly proposed variants close
this specific gap, each by removing "restore" and substituting a
forward-looking (non-presupposing) verb, while leaving every other word in
Candidate 1 -- including the first sentence's 6b restatement and the
trailing not-built-or-tested disclaimer -- untouched. This resolves that
report's Section 12 item 2. That report's Section 12 item 1 (the choice
between its Candidate 1 and Candidate 2, i.e. full-stop break vs.
semicolon) was already resolved by the parent session choosing Candidate 1
as the base for all three of this task's variants, consistent with this
session's own independent reading -- not re-litigated here since the task
explicitly holds Candidate 1's structure fixed and varies only the one
flagged clause. That report's Section 12 item 3 (the six Section 2 "We do
not claim..." disclaimers) is unrelated to this task and remains open,
carried forward unchanged.

No new regression found: git diff --stat manuscript/main.tex still shows
only the same pre-existing 3-line E7.5-A punctuation diff, independently
re-verified this session (Section 1 above); that diff's own PASS verdict in
research/E7_5_INDEPENDENT_WRITING_AUDIT_PASS.md is unaffected and not
re-litigated here, since it is a disjoint unit of prose (Section 1.1, not
the abstract).

## 12. Verdict

GREEN -- PASS for the "restore"-clause fix as a category. A specific
variant choice among the three remains an open, non-blocking style
preference for the human author, addressed below.

Justification: All three variants independently and correctly resolve the
one precision issue this task was scoped to fix -- Candidate 1's "restore"
clause presupposing a prior reliable ranking-prediction state that neither
the manuscript's own 6b finding nor its H1-partially-supported verdict
establishes existed. None of the three strengthens the core 6b-adjacent
claim, alters scope, weakens H1's PARTIALLY_SUPPORTED status, blurs the
6a/6b distinction, or removes any existing hedge; the not-built-or-tested
disclaimer is verbatim-identical across Candidate 1 and all three variants.
No Step 2 guardrail is violated by any of the three, including the
watch-listed word "reliable"/"reliably" present in two of the three, which
sits strictly inside an unanswered hypothetical clause in the same
structural position the prior CONDITIONAL report already evaluated and
cleared for Candidate 1's original wording. This session also independently
fact-checked and corrected the task framing's claim that "predict which
mechanism wins" appears "3 times: abstract, Results, Discussion" -- the
actual count is four occurrences (abstract, two in Results, one in
Conclusion; zero in Discussion), a correction that, if anything, further
supports Variant 2 as the best-anchored choice rather than undermining any
verdict.

Among the three, this review's independent assessment ranks Variant 2 as
the safest and best-anchored: it introduces zero new vocabulary, reuses the
manuscript's own four-times-repeated idiom for the exact concept being
discussed (including within the same abstract paragraph, two sentences
earlier), and requires no anaphoric inference to resolve its referent.
Variant 1 is also safe but introduces one low-risk, unanchored new word
("achieve"). Variant 3 is also safe and is the only one of the three with
zero exposure to the Step-2 "reliable" watch-word, but introduces a mild
terminology near-miss ("the winning mechanism" vs. the manuscript's
established "empirical winner"/"which mechanism wins").

For the human author to decide/fix, in priority order:

1. (Requires a decision, non-blocking -- all three pass) Choose among
   Variant 1, 2, or 3. Recommended direction: Variant 2, on the strength of
   (a) zero new vocabulary, (b) exact reuse of the manuscript's own
   four-times-repeated "predict which mechanism wins" idiom, and (c) no
   anaphoric-resolution burden on the reader. This recommendation is this
   review's own independently derived judgment, not inherited from any
   prior session's stated preference.
2. (Informational, no action required) The task framing's claim that
   "predict which mechanism wins" appears "3 times: abstract, Results,
   Discussion" is inaccurate -- the correct count is four occurrences
   (abstract line 73, Results line 925, Results line 1099, Conclusion line
   1404), and the third location the task framing implicitly attributed to
   Discussion is actually still inside Results Sec.5.6 ("Summary of
   Findings"), two lines before Discussion begins. This does not change any
   verdict above but the human author's mental model of the phrase's
   distribution should be corrected.
3. (Carried forward from the prior CONDITIONAL report, unrelated to this
   task, still open) The six Section 2 "We do not claim..." disclaimer
   sentences remain unactioned; out of scope for this pass.
