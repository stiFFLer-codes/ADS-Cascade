# E4.1 Resolution Audit — Independent Verification (F3/F4 Fix Pass)

> Independent re-verification of the surgical F3/F4 fix pass described in
> `research/E4_RESOLUTION_AUDIT.md`. Performed from scratch against `manuscript/main.tex` and repo
> state directly; the claims in `E4_RESOLUTION_AUDIT.md` were used only as a checklist of things to
> verify, not as evidence in themselves. No file this task was told not to touch was modified.
> Nothing was staged or committed.

---

## 1. Repository state

- Branch: `main`. HEAD: `95c2b18` ("Phase E3: complete first manuscript draft").
- Working tree: exactly one tracked file modified — `manuscript/main.tex` (9 insertions, 5
  deletions, confirmed via `git diff --numstat`). Nothing staged (`git diff --cached --stat` empty).
- Untracked files present are all new audit-report `.md` files under `research/` (E0/E2/E3/E4
  checkpoint audits, manuscript-architecture docs, this pass's own inputs) — expected, not flagged.
- `git diff 6fb6188 -- data/outputs/experiments/exp1/final/` → empty (byte-identical to freeze).
- `git diff --stat HEAD -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md research/contribution_lock.csv manuscript/references.bib` → empty.
- `git log --oneline -1` on those four locked files → `b776a5e` (Phase E.2), i.e. untouched by
  this fix pass or the E3 draft commit.

## 2. F3 verification (§4.2, 0.695 confidentiality qualifier)

Read `manuscript/main.tex` lines 594–608 directly. Current text (lines 602–606):

> "...is fixed at 0.695 -- the production-observed value, cited from a confidential engagement and
> not independently reproducible from this repository -- so that it does not become a second,
> uncontrolled independent variable alongside the consistency sweep itself."

Confirmed: the qualifier clause is present, inline, at point of use. **F3 is substantively
resolved.**

One precision note, found independently (not surfaced by `E4_RESOLUTION_AUDIT.md`'s own
self-verification, which claims the phrase is used "identically" three other times): the canonical
phrase, as fixed by `research/PAPER_CONTRACT.md` line 113, is exactly *"cited from a confidential
engagement, not independently reproducible from this repository"* (comma). The three pre-existing
instances in the manuscript match this near-exactly:
- §1.1, line 113–114: "...are **drawn** from a confidential engagement, not independently
  reproducible from this repository." (comma; "drawn" not "cited")
- §6.2, line 1175–1176: "...are **cited** from a confidential engagement, not independently
  reproducible from this repository" (comma; matches contract verbatim)
- Reproducibility Statement, line 1492–1494: "...is confidential and not reproducible from this
  repository **in any sense**..." — this one is a materially different paraphrase, not the same
  sentence pattern at all.

The new §4.2 clause reads "...cited from a confidential engagement **and** not independently
reproducible..." — substituting "and" for the contract's comma. This is a trivial grammatical
variant that does not change meaning or weaken the qualifier, but it means the claim in
`E4_RESOLUTION_AUDIT.md` §2 that the fix is "reusing the manuscript's own already-established
phrase... identically" is slightly overstated: it is consistent in substance with §1.1/§6.2 and
close in wording, but not byte-identical, and the Reproducibility Statement instance it's grouped
with is a different sentence entirely. This does not affect PAPER_CONTRACT.md §5 compliance (the
required elements — "confidential engagement" + "not independently reproducible from this
repository" — are both present), so it is **non-blocking**, but the self-audit's precision claim
should not be taken as literally verified.

## 3. F4 verification (§1.1, EMBEDDING_PRIMARY / retrieval disambiguation)

Read `manuscript/main.tex` lines 95–115 directly. Current text (lines 100–114):

> "...that statistic was measured at 91.2\% and the rule selected a rules-first, exact-match
> mechanism; in an independently generated synthetic reproduction of the same pipeline, the
> analogous statistic was measured at 87.56\% and the same rule selected its embedding-based branch
> (\texttt{EMBEDDING\_PRIMARY}) instead -- a different mechanism from the lexical-similarity
> \texttt{retrieval} mechanism this paper's Experiment~1 tests (Section~3.4); no embedding-based
> mechanism is evaluated anywhere in this paper. Both figures sit within a few percentage points of
> the rule's own 90\% threshold..."

Confirmed against all four sub-requirements:
- No longer says "retrieval-based mechanism" for the production output — confirmed, that phrase is
  gone from §1.1 (verified by grep across the full file: "retrieval-based mechanism" does not
  appear anywhere in the current file).
- Names `EMBEDDING_PRIMARY` explicitly, in `\texttt{}`, consistent with the manuscript's existing
  code-identifier convention — confirmed.
- Explicitly distinguishes it from Experiment 1's own `retrieval` mechanism, with a correct
  cross-reference — confirmed. Verified independently that Section~3.4 is in fact
  "Fuzzy/Similarity Retrieval Mechanism" (subsection numbering traced from `\section` counts:
  `\section{Problem Setting and Signal Definition}` is Section 3, and its 4th `\subsection` —
  Historical Decisions (3.1), ADS (3.2), Exact-Match Rules (3.3), Fuzzy/Similarity Retrieval (3.4)
  — is exactly the retrieval-mechanism definition at line 536, which itself independently states
  "no embedding model was trained, downloaded, or evaluated anywhere in this experiment." The
  cross-reference is correct.
- Closing clause "no embedding-based mechanism is evaluated anywhere in this paper" is present —
  confirmed.

**F4 is resolved**, fully matching all four sub-requirements in the task.

## 4. Whole-manuscript terminology sweep (independent)

Ran `grep -in "retrieval|embedding|EMBEDDING"` against the entire current `manuscript/main.tex`
(57 matches) and read every one in context (not merely trusting the count). Categorized:

- Abstract (line 60) and General Problem (line 130): generic framing ("rules, retrieval, a trained
  model") — no mechanism-identity claim, not scoped to Experiment 1 specifically.
- §2 Related Work (lines 166, 236, 239, 309, 382, 394, etc.): all refer to Experiment 1's own
  `retrieval` mechanism or the general term "information retrieval" (line 394, clearly a different
  sense — "commodity information-retrieval technique"). No conflation found.
- §3.4 (lines 536–550): the mechanism's own original definition, explicitly stating it is not an
  embedding model. Unmodified by this pass (outside the diff's touched line ranges).
- §4 Experimental Design (lines 661–821, 881–928): all refer to the `retrieval` mechanism as
  actually tested (cutoff, thresholds, calibration) — consistent usage, no embedding claim.
- §5 Results (lines 943–1118): all refer to the tested `retrieval` mechanism's measured accuracy —
  consistent, no embedding claim, and (separately verified in §5 below) no production number
  appears in this range either.
- §6 Discussion (lines 1233–1268): explicitly scoped statements — "not a claim about fuzzy or
  embedding-based retrieval in general, which this experiment does not test" (line 1239–1240) — the
  paper's own hedge, unmodified by this pass.
- §7 Limitations (lines 1327–1328, 1421–1424): "not embedding-based retrieval" and "other retrieval
  implementations such as embedding-based retrieval, is untested here" — both correctly framed as
  untested/future, unmodified by this pass.
- §1.1 (lines 100–106): the newly corrected passage — the only place `EMBEDDING_PRIMARY` appears in
  the document (confirmed via a separate grep for the literal string — exactly one occurrence).

**Independently confirmed: no sentence anywhere in the current manuscript states or implies that
Experiment 1 evaluated `EMBEDDING_PRIMARY` or any embedding-based mechanism.**

## 5. No other scientific claims changed

`git diff -- manuscript/main.tex` shows exactly two hunks, both already quoted above (lines
~100–114 and ~600–606), 9 insertions / 5 deletions total, and nothing else. This alone is
sufficient proof that Results (§5, lines 895–1147), Discussion (§6), Limitations (§7), the
Contribution Statement (§1.7), the Abstract, and every table are byte-for-byte unchanged from the
E3 checkpoint commit `95c2b18` — none of those line ranges intersect the diff.

Spot-checks performed independently rather than only relying on that inference:
- `grep -c "32/32|0/18|30/30|2/20|64\.0"` → 14 combined matches in the current file (not
  individually re-verified against a pre-fix count since the diff already proves no touch to these
  ranges, but presence confirmed).
- H1 "partially supported" language appears at lines 817–819, 1187, 1380–1383, 1468 — none within
  the diff's touched ranges. (Note: `E4_RESOLUTION_AUDIT.md` §7 states H1 status appears "identically
  in the same 3 locations" — the actual count of locations discussing H1's partial-support status is
  higher than 3 depending on how one counts prose vs. literal `PARTIALLY_SUPPORTED` string mentions,
  but this is an undercount in the self-audit's bookkeeping, not a discrepancy that matters: all of
  them are outside the diff's touched lines and therefore unchanged regardless.)
- Both production p-values, Wilson CI language, and the Formulation #2 synthesis sentence were not
  re-typed out here but are confirmed untouched by the same diff-range argument.

## 6. No production evidence inside Results

`grep -n "91.2|0.847|0.964|0.695"` across the whole file returns matches only at lines 100, 122,
603, 1344, 1345 — all outside the Results section's line range (895–1147, confirmed from the
`\section`/`\subsection` line listing: `\section{Results}` at 895, `\section{Discussion}` at 1147).
**Confirmed: no production number appears inside `\section{Results}`.**

## 7. Frozen artifacts / locked files

- `data/outputs/experiments/exp1/final/`: no diff against the Phase D freeze commit `6fb6188`.
- `research/PAPER_CONTRACT.md`, `research/CONTRIBUTION_LOCK.md`, `research/contribution_lock.csv`,
  `manuscript/references.bib`: no diff against HEAD; all last modified at commit `b776a5e`
  (Phase E.2), predating both the E3 draft and this fix pass.

## 8. Git hygiene

- Nothing staged.
- Tracked-file modifications: exactly `manuscript/main.tex`.
- Untracked files: all new `research/*.md` audit-report files, consistent with an audit-heavy
  session; no stray temp/backup files (`.bak`/`.swp`/`.orig`/`.tmp`) observed.
- Secrets/credentials scan of the diff (`grep -iE "api[_-]?key|secret|password|bearer|token|BEGIN
  (RSA|OPENSSH|PGP)|C:\\Users"`) → no matches.
- No local Windows paths or usernames found introduced into `manuscript/main.tex`'s diff content.
  (The `LF will be replaced by CRLF` message seen during `git diff`/`git log` invocations is a
  pre-existing Windows line-ending-normalization warning from this checkout's `git config`, not a
  change introduced by the fix pass — it appears on read-only commands too.)
- Independent LaTeX structural check (`\begin{}`/`\end{}` environment-count balance, and raw
  `{`/`}` brace-count balance) run against the full current file: all environments balanced, brace
  count balanced (0). Corroborates (independently, not by re-trusting) the resolution audit's own
  §9 claim.

## 9. Test suite

Ran independently:
```
python -m pytest scripts/experiments/exp1/ -q
30 passed in 10.50s
```
Matches the expected 30/30 and the resolution audit's own reported result.

---

## 10. Findings

- **REQUIRED NOW:** none. Both F3 and F4 are substantively resolved; no scope violation, no
  resurrected rejected claim, no frozen-evidence change, no unsafe git state.
- **OPTIONAL FUTURE WORK:** the new §4.2 qualifier clause uses "cited from a confidential engagement
  **and** not independently reproducible..." rather than the contract's exact canonical phrasing
  ("...engagement**,** not independently reproducible..." — comma, not "and"). Purely cosmetic; the
  required substantive elements (confidential engagement + not independently reproducible from this
  repository) are both present and the requirement is met. Worth a one-word tidy (comma for "and")
  only if the manuscript goes through another full copyedit pass — not worth a dedicated fix cycle
  on its own.
- **OPTIONAL FUTURE WORK:** `E4_RESOLUTION_AUDIT.md`'s own description of the F3 phrase as reused
  "identically" in three other locations is imprecise — the Reproducibility Statement instance is a
  materially different paraphrase ("is confidential and not reproducible... in any sense"), not the
  same sentence pattern. Does not affect the fix's correctness, only the self-audit's internal
  precision. Not required to be fixed since it lives in a non-frozen audit-trail document, not the
  manuscript itself.
- All other items in `research/E4_RESOLUTION_AUDIT.md` §11 ("Remaining non-blocking issues": F1
  Dawid–Skene precision note, F2 realized-ADS-range wording, F6 stale 84.1% figure outside this
  manuscript, section over-segmentation, unpreempted objection, unrendered figure placeholders)
  were out of scope for this verification pass (they were never claimed to be fixed) and are
  correctly still open per that document — not re-adjudicated here.

## 11. Verdict

**PASS.**

Both REQUIRED NOW findings from Phase E4 (F3, F4) are independently confirmed resolved by direct
inspection of `manuscript/main.tex`, not by trusting `research/E4_RESOLUTION_AUDIT.md`'s narrative.
The diff is exactly the two described edits (9 insertions / 5 deletions, both hunks accounted for);
no other prose, statistic, table, or scientific claim in the manuscript was touched; no frozen
evidence or locked-contract file was modified; no production number leaked into Results; the
whole-document retrieval/embedding terminology sweep independently confirms no remaining place
implies Experiment 1 tested an embedding-based mechanism; git hygiene is clean; and the exp1 test
suite passes 30/30. The two items noted above are cosmetic precision gaps in wording/self-reporting,
not integrity issues, and do not block E4 GREEN.
