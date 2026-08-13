# E4.1 Resolution Audit — F3/F4 Surgical Fix Pass

> Resolves exactly the two REQUIRED NOW findings from Phase E4
> (`research/E4_SCIENTIFIC_AUDIT.md` Part L; `research/E4_ARTIFACT_AUDIT.md` Findings F3/F4). No
> other content in `manuscript/main.tex` was touched. No frozen evidence, `PAPER_CONTRACT.md`,
> `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`, or `manuscript/references.bib` was modified. No
> experiment was run or regenerated.

---

## 1. Original E4 findings

**F3 (production-data confidentiality qualifier).** `manuscript/main.tex`, §4.2 ("Synthetic
Generator"), the cross-company-alignment parameter (0.695) was introduced as "the
production-observed value" without the confidentiality/reproducibility qualifier that every other
production-sourced figure in the manuscript carries at its point of use, and that
`research/PAPER_CONTRACT.md` §5 requires at "every" appearance of a production number.

**F4 (retrieval terminology ambiguity).** `manuscript/main.tex`, §1.1 ("Real-world motivation"), the
phrase "the same rule selected a retrieval-based mechanism instead" described the production/
synthetic architecture-decision procedure's `EMBEDDING_PRIMARY` output using language that overlaps
with, but does not name, Experiment 1's own "retrieval" mechanism — which §3.4 explicitly and
carefully defines as *not* an embedding model. This risked implying a production↔Experiment-1
mechanism identity that does not exist.

---

## 2. Exact change made

**F3** — one inline qualifying clause inserted into the existing sentence at `manuscript/main.tex`
line ~603 (§4.2), reusing the manuscript's own already-established phrase for this exact purpose
("cited from a confidential engagement, not independently reproducible from this repository," used
identically in §1.1, §6.2, and the Reproducibility Statement) rather than inventing new wording.

**F4** — the phrase "a retrieval-based mechanism instead" was replaced with a clause that (a) names
the actual production decision-procedure output, `\texttt{EMBEDDING\_PRIMARY}`, matching the
manuscript's existing `\texttt{}` convention for code-level identifiers (`\texttt{rules}`,
`\texttt{retrieval}`, `\texttt{random.Random(seed)}`, etc.), (b) explicitly states it is "a different
mechanism from the lexical-similarity `\texttt{retrieval}` mechanism this paper's Experiment~1
tests," cross-referencing §3.4, and (c) adds one explicit closing clause, "no embedding-based
mechanism is evaluated anywhere in this paper," to foreclose the misreading directly rather than
leaving it to be inferred from the cross-reference alone.

---

## 3. Before / after wording

### F3 — `manuscript/main.tex` §4.2 ("Synthetic Generator")

**Before:**
> Cross-company alignment -- the rate at which different companies agree on a shared product's
> dominant account -- is fixed at 0.695, the production-observed value, so that it does not become
> a second, uncontrolled independent variable alongside the consistency sweep itself.

**After:**
> Cross-company alignment -- the rate at which different companies agree on a shared product's
> dominant account -- is fixed at 0.695 -- the production-observed value, cited from a confidential
> engagement and not independently reproducible from this repository -- so that it does not become a
> second, uncontrolled independent variable alongside the consistency sweep itself.

Numerical value (0.695) and its meaning (a fixed generator nuisance parameter, not evidence) are
unchanged. Nothing was strengthened or weakened about what the number means or how it is used.

### F4 — `manuscript/main.tex` §1.1 ("Real-world motivation")

**Before:**
> ...in an independently generated synthetic reproduction of the same pipeline, the analogous
> statistic was measured at 87.56\% and the same rule selected a retrieval-based mechanism instead.

**After:**
> ...in an independently generated synthetic reproduction of the same pipeline, the analogous
> statistic was measured at 87.56\% and the same rule selected its embedding-based branch
> (\texttt{EMBEDDING\_PRIMARY}) instead -- a different mechanism from the lexical-similarity
> \texttt{retrieval} mechanism this paper's Experiment~1 tests (Section~3.4); no embedding-based
> mechanism is evaluated anywhere in this paper.

The 87.56\% figure, its production/synthetic framing, and the surrounding paragraph's motivating
role are all unchanged. No embedding dependency was introduced (no code was written or run); the
change is a naming/scoping correction only.

---

## 4. Why each change resolves the finding

**F3:** the manuscript's own established pattern (used identically three other times, §1.1/§6.2/
Reproducibility Statement) for flagging a production-sourced number is now applied at this fourth
location too, closing the one gap Part F of the E4 artifact audit found in an otherwise-consistent
compliance sweep. `PAPER_CONTRACT.md` §5's "every appearance" rule is now satisfied for every
production-sourced number in the manuscript, not three of four.

**F4:** the sentence no longer uses vocabulary ("retrieval-based") that is also the name of
Experiment 1's own tested mechanism to describe an untested production-system output. A reader of
§1.1 now sees, in the same sentence, both the correct production-decision label
(`EMBEDDING_PRIMARY`) and an explicit statement that it is not the mechanism this paper's experiment
evaluates — directly closing the "reader could conflate the case study's untested outcome with
Experiment 1's actually-tested mechanism" risk identified as Part K, Objection 5 in the E4 scientific
audit, without needing the reader to independently recall §3.4's distinction to avoid the
misreading.

---

## 5. Whole-manuscript terminology sweep

Searched the entire staged `manuscript/main.tex` for every occurrence of `retrieval`, `retrieval-`
(hyphenated compounds), `embedding`, and `EMBEDDING` (57 lines matched). Read every match in context.
Findings:

- Every occurrence of "retrieval" outside §1.1 refers unambiguously to Experiment 1's own
  lexical-similarity mechanism, the general research-area term "information retrieval" (§2.7, in
  "commodity information-retrieval technique," a different sense, clearly disambiguated by context),
  or a Related Work citation's own use of the term (§2.3's "workflow composition" discussion) — no
  other location conflates it with an embedding model.
- Every occurrence of "embedding" outside the new §1.1 clause is either (a) §3.4's own original,
  unmodified distinction ("We deliberately call this mechanism 'retrieval,' not 'embedding'... no
  embedding model was trained, downloaded, or evaluated... 'embedding-primary' would misstate what
  was actually tested"), or (b) an explicit, correctly-hedged Discussion/Limitations/Future-Work
  statement that embedding-based retrieval is untested here and named only as a future direction
  (§6.6: "not a claim about fuzzy or embedding-based retrieval in general, which this experiment does
  not test"; §7.4 Limitations: "Only exact-match rules and rapidfuzz-based retrieval were compared --
  not embedding-based retrieval"; §8.3 Future Work: "other retrieval implementations such as
  embedding-based retrieval, is untested here").
- `EMBEDDING_PRIMARY` (the production/synthetic decision-procedure label) now appears exactly once,
  at the corrected §1.1 location, and nowhere else — it is not used as a stand-in for, or conflated
  with, Experiment 1's own `retrieval` mechanism anywhere in the document.

**Confirmed: the manuscript never states or implies that Experiment 1 evaluated `EMBEDDING_PRIMARY`
or any embedding-based mechanism.** Every mention of embedding-based approaches is either the §3.4
disclaimer, a correctly-scoped Limitations/Future-Work statement that it was not tested, or the new,
now-correctly-labeled §1.1 reference to the production system's own (untested-by-this-paper)
decision output.

---

## 6. Production-data scope sweep

Searched the entire manuscript for `0.695`. **Exactly one occurrence**, at the corrected §4.2
location, now carrying the required qualifier. (The other three production-sourced figures already
in the manuscript — 91.2%, weighted ADS 0.847, unweighted ADS 0.964 — were previously verified
correctly qualified at every one of their locations by the E4 artifact audit's Part F and were not
touched by this pass; re-confirmed unchanged by the diff in §9 below.)

No new production claim was introduced. No production number's qualifier was removed or weakened
elsewhere. No production number appears inside the Results section (re-confirmed: a scan restricted
to `\section{Results}`'s line range found zero occurrences of `91.2`, `0.847`, `0.964`, or `0.695`,
matching the E4 artifact audit's prior finding, unchanged by this pass).

---

## 7. Scientific invariants verified

- **H1 remains PARTIALLY\_SUPPORTED**, stated identically in the same 3 locations (§4.11, §7.10,
  Conclusion) as before this pass — text of these statements was not touched, and a count of
  `PARTIALLY_SUPPORTED`/`PARTIALLY\_SUPPORTED` occurrences before and after this pass is unchanged.
- **Formulation #2 remains unchanged** — the 6a/6b synthesis sentence (§6.1, Conclusion) and the
  Contribution Statement (§1.7) were not edited by this pass; both still read exactly as they did at
  the E3 checkpoint commit.
- **No statistic changed** — 32/32, 0/18, 30/30, 2/20, 64.0%, the Wilson CI, and both p-values
  (1.9×10⁻⁹, 4.0×10⁻⁹) appear the same total number of times (16) before and after this pass, all at
  their original locations; neither edit touched Results (§5) or any table.
- **No new experiment was run and no frozen evidence was regenerated** — this pass consisted of two
  `Edit` operations on `manuscript/main.tex` only; no script under `scripts/` was executed except the
  existing test suite (§8) and the pre-existing LaTeX-balance checker (a static text check, not a
  scientific computation).

---

## 8. Test results

```
python -m pytest scripts/experiments/exp1/ -q
30 passed in 11.84s
```

30/30, matching the expected count and every prior checkpoint this session.

---

## 9. Frozen-evidence integrity

- `git diff 6fb6188 -- data/outputs/experiments/exp1/final/` → **empty**. Byte-identical to the Phase
  D freeze commit.
- `git diff --stat HEAD -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md
  research/contribution_lock.csv manuscript/references.bib` → **empty**. All four confirmed
  untouched; no citation defect was discovered, so `references.bib` was correctly left unmodified
  per the task's conditional instruction.
- LaTeX environment/brace balance re-checked after both edits: `abstract`, `cases`, `document`,
  `equation`(×2), `figure`(×4), `table`(×4), `tabular`(×4) all balanced; final brace depth 0; no
  issues.

---

## 10. Auditor verdict

Independent second audit performed by the `research-code-auditor`, from scratch, against
`manuscript/main.tex` directly (not by trusting this document's own claims). Full report:
`research/E4_RESOLUTION_AUDIT_INDEPENDENT.md`.

## 🟢 PASS

Both F3 and F4 independently confirmed resolved. The diff (`git diff -- manuscript/main.tex`) was
independently verified to be exactly the two described hunks (9 insertions / 5 deletions); nothing
in Results, Discussion, Limitations, the Contribution Statement, the Abstract, or any table was
touched; the whole-document retrieval/embedding sweep independently confirms no remaining location
implies Experiment 1 tested `EMBEDDING_PRIMARY` or any embedding-based mechanism; no production
number appears inside Results; frozen evidence and all locked-contract files confirmed unchanged;
git hygiene clean; test suite 30/30.

**Two non-blocking cosmetic notes** (do not affect the verdict): (a) the new §4.2 qualifier reads
"...engagement **and** not independently reproducible..." rather than the contract's exact canonical
phrasing ("...engagement**,** not independently reproducible..." — a comma, not "and"); the required
substantive elements are both present regardless. (b) This document's §2 claim that the fix reuses
the manuscript's established phrase "identically" in three other locations is itself slightly
imprecise — the Reproducibility Statement instance is a materially different paraphrase, not the
same sentence pattern; §1.1 and §6.2 do match closely. Neither note requires a further edit under
this pass's scope.

---

## 11. Remaining non-blocking issues

Unchanged from `research/E4_SCIENTIFIC_AUDIT.md` Part L's "Recommended, non-blocking" list — none
were addressed in this pass, per the explicit scope restriction (surgical F3/F4 fix only): the
Dawid–Skene precision note (F1), the realized-ADS-range self-consistency wording (F2), the stale
84.1% figure in `PAPER_CONTRACT.md`/`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` (F6, outside this
manuscript's own scope), the ~65-subsection over-segmentation, the un-preempted "expected by
construction" objection, and the four unrendered figure placeholders. None of these were touched by
this pass and none are required before E4 GREEN per the original verdict.
