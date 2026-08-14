# E5.4 — Figure Generation + Visual Scientific Audit

> Figure rendering and manuscript integration only. No frozen evidence, statistical methodology,
> threshold, seed, generator parameter, mechanism, hypothesis, or contribution wording touched. Not
> yet committed — this is the pre-commit evidence trail for that decision.

---

## 1. Scope

Generate the four planned figures (F1-F4) from the frozen Experiment 1 evidence using the existing,
already-written `manuscript/figures/generate_figures.py`, inspect the actual rendered images (not
just the plotting code), fix any misleading rendering found, and wire the results into
`manuscript/main.tex`'s existing captioned figure slots (per `research/PAPER_CONTRACT.md` Sec.11,
those slots were valid placeholders at E3; this pass fills them, it does not create them).

## 2. Tooling gap and remediation

`matplotlib` is not installed in this repository's own environment (`ModuleNotFoundError`, confirmed
again this pass) and remains intentionally commented out in `requirements.txt` (E5.3's own decision —
`research/E5_3_CORRECTION_AUDIT.md` Sec.2 — since it is needed only for this figure step, not for
reproducing Experiment 1's own results). Per this pass's explicit instruction not to install anything
globally or silently change project dependencies: created an isolated, scratchpad-only virtualenv
(outside the repository), installed only `matplotlib` (and its own transitive deps) into it, and ran
the existing, unmodified-except-for-the-F3-fix-below `generate_figures.py` with that venv's Python.
This exactly mirrors the isolated-venv verification pattern already used and independently audited in
E5.3 for `rapidfuzz` (`research/E5_3_CORRECTION_AUDIT.md` Sec.3). `requirements.txt` itself was **not**
touched by this pass — the commented-out `matplotlib` line already documents the manual step, and the
figure script's own docstring already instructed `pip install matplotlib`.

Result: `matplotlib 3.11.1` resolved cleanly; all four PDFs rendered successfully:
```
Wrote f1_design_flow.pdf, f2_ads_vs_accuracy.pdf, f3_r3_agreement_by_band.pdf,
f4_ranking_constancy.pdf to manuscript/figures
```

## 3. Data source for every figure

All four figures read exclusively `data/outputs/experiments/exp1/final/final_condition_results.csv`
(the frozen, 240-row evidence artifact, byte-identical to commit `6fb6188` — verified again this pass,
`git diff --quiet 6fb6188 -- data/outputs/experiments/exp1/final/` exits 0). No other data source, no
recomputation of any statistic beyond what that CSV already contains via simple aggregation
(band membership, Pearson-style visual scatter, agreement counts) — no new experiment, no re-tuned
threshold, no new number that doesn't already appear in `CONTRIBUTION_LOCK.md`/`PAPER_CONTRACT.md`.

## 4. Adversarial visual audit — findings

Inspected the actual rendered PDFs (not only the generation code):

- **F1 (design flow)** — static schematic, four boxes (generator, lexical condition, two mechanisms,
  falsification table), matches `EXPERIMENT_1_REDESIGN_REVIEW.md` Sec.6/Sec.18 and Table T3's frozen
  configuration. No data-fidelity risk (not data-driven). **Pass, no changes.**
- **F2 (ADS vs. accuracy)** — CLEAN panel shows rules and retrieval tracking closely together, rising
  with ADS (near-equivalence, matches Table T5's +0.005/+0.006 CLEAN gap); VARIED panel shows
  retrieval consistently above rules across the full ADS range, with the gap visually widening at
  higher ADS (matches Table T5's VARIED gap: -0.137 to -0.185). Axes, legend, shared y-scale, and
  faceting by lexical condition are all correct and match the caption's stated scope (Sec.5.2,
  correlational, explicitly not yet a ranking claim — the surrounding prose in `main.tex` already
  defers the ranking question to Sec.5.3). **Pass, no changes.**
- **F3 (R3 agreement by band) — SUBSTANTIVE ISSUE FOUND AND FIXED.** The original script computed
  `rate = 0.0` for any band with zero defined R3-vs-empirical comparisons, identical to a band with a
  defined 0% agreement rate. The `<0.70` band has 70/70 rows with `r3_selected_mechanism=llm_required`
  and a blank `r3_agrees_with_empirical` (verified directly against the frozen CSV this pass) — R3
  makes no rules/retrieval prediction there at all, so there is no agreement/disagreement concept to
  plot. The original rendering showed a bare 0%-height bar for `<0.70`, visually indistinguishable
  from the `>=0.90` band's genuine, defined, exceptionless 0/18 disagreement — collapsing
  "structurally not evaluated" and "evaluated and failed" into the same mark. This is exactly the kind
  of visual risk this audit step exists to catch: a reviewer skimming the figure could read
  "0% - 100% - 0%" as three comparable data points, when `main.tex`'s own prose and caption (Sec.5.3,
  Table T4's footnote) only ever report agreement for the two bands that have a defined comparison at
  all. **Fixed** in `manuscript/figures/generate_figures.py`'s `make_f3()`: the `<0.70` band now
  renders as a distinct hatched/grey box labeled "N/A (R3 excludes this band)" instead of a bar, and
  the two defined bands are now labeled with their exact counts (`32/32`, `0/18`) directly on the
  chart — both changes make the figure state only what the frozen CSV actually supports, introducing
  no new number (both counts already appear in `CONTRIBUTION_LOCK.md` Sec.2 step 7 and `main.tex`
  Sec.5.3/Table T4) and removing a misleading implicit one. Regenerated after the fix; re-inspected the
  new rendering to confirm the fix renders as intended.
- **F4 (ranking constancy)** — CLEAN points cluster at/near zero across the full ADS range (near-
  equivalence); VARIED points sit consistently below zero (rules-minus-retrieval negative, i.e.
  retrieval wins) across the full ADS range, with the offset from zero widening as ADS rises — again
  matching Table T5 exactly. The zero-line never crosses within either lexical-condition series
  regardless of ADS, which is precisely the exceptionless winner-constancy claim this figure exists to
  visualize (Sec.5.3/`CONTRIBUTION_LOCK.md` Sec.4). **Pass, no changes.**

## 5. Central scientific-risk checks (per this pass's explicit brief)

- **"Higher ADS selects the correct mechanism" implied visually?** No. F3 (post-fix) shows the
  *opposite* pattern is what actually happened: agreement is 100% in the *middle* band and 0% in the
  *highest* band — a non-monotonic reversal, not a "higher ADS is better" story. F2/F4 show accuracy
  rising with ADS for *both* mechanisms without the ranking ever flipping — exactly the 6a/6b
  distinction, not a collapse of it.
- **F2 does not collapse accuracy-prediction and ranking-prediction into one concept:** F2's caption
  and the surrounding Sec.5.2 prose (unedited by this pass) explicitly state the correlational,
  per-mechanism scope and explicitly defer the ranking question to Sec.5.3/F4 — the figure shows two
  series on shared axes (necessary to visualize "each mechanism's own accuracy"), but does not label,
  caption, or annotate a "winner," which stays exclusively F3/F4's job.
- **64.0% aggregate not overemphasized:** no figure plots the flat aggregate at all; F3 shows only the
  band structure, matching `main.tex` Sec.5.3's explicit "report the band structure before the
  aggregate" ordering decision (`research/MANUSCRIPT_ARCHITECTURE.md` Sec.4).
- **H1 PARTIALLY_SUPPORTED, 6a/6b distinction:** unaffected — no figure states or implies a stronger or
  weaker verdict than `main.tex`'s existing prose, which this pass did not edit.

## 6. Manuscript integration

Replaced exactly the four `\fbox{\parbox{...}}` TODO placeholder blocks in `manuscript/main.tex` with
`\includegraphics[width=0.85\linewidth]{figures/<file>.pdf}`, one per figure (F1/F2/F3/F4, at their
existing locations). **No caption, label, surrounding prose, table, or section text was changed** —
verified by diff: `git diff manuscript/main.tex` shows exactly four four-to-six-line replacements, all
within existing `\begin{figure}...\end{figure}` blocks, nothing else. `graphicx` was already loaded
(`main.tex` line 35); no new package added. No `\graphicspath` override exists, so the relative paths
resolve correctly from `main.tex`'s own directory.

`manuscript/figures/generate_figures.py`'s header docstring was also updated (in addition to the F3
fix) to state accurately that the script has now been run (in the isolated venv described in Sec.2),
replacing a now-stale note that said it "could not be executed in the current environment" — a
documentation-accuracy correction, not a scientific-content or data change.

## 7. Toolchain limitation (unresolved, pre-existing, out of scope for this pass)

No `pdflatex`/`bibtex` is available in this environment (`which pdflatex`/`which bibtex` both fail) —
a pre-existing gap already noted in `research/MANUSCRIPT_SKELETON_AUDIT.md` for a prior phase. This
pass could not compile `main.tex` to a PDF to visually confirm final in-document figure placement,
page breaks, or float positioning. This is reported as a known limitation, not silently worked around
or claimed resolved. `\includegraphics` paths and package requirements were verified by direct
inspection instead (Sec.6).

## 8. Protected/frozen-file verification

```
git diff --stat -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md manuscript/references.bib \
  data/outputs/experiments/exp1/final/ scripts/experiments/exp1/
→ (empty — clean)

git diff --quiet 6fb6188 -- data/outputs/experiments/exp1/final/  → exit 0 (byte-identical to freeze)
```
`git status --porcelain` confirms the only tracked-file changes are `manuscript/main.tex` and
`manuscript/figures/generate_figures.py`; the only new tracked-candidate files are the four rendered
PDFs. No Experiment 1 source file, frozen artifact, contract/lock document, or bibliography entered
the working tree as changed.

## 9. Test results

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed** (unchanged — no Experiment 1 code was
touched). `python scripts/experiments/exp1/analyze_posthoc.py --demo` → reproduces the frozen 32/50
agreement, Wilson CI, and binomial p exactly, same as before this pass.

## 10. Exact proposed staging list (not yet staged, pending human approval)

```
manuscript/main.tex
manuscript/figures/generate_figures.py
manuscript/figures/f1_design_flow.pdf
manuscript/figures/f2_ads_vs_accuracy.pdf
manuscript/figures/f3_r3_agreement_by_band.pdf
manuscript/figures/f4_ranking_constancy.pdf
research/E5_4_FIGURE_GENERATION_AUDIT.md
```

Explicitly **not** part of this proposed staging list:
- `requirements.txt` — untouched by this pass (matplotlib deliberately stays commented out per E5.3;
  the isolated-venv pattern makes an uncommitted dependency change unnecessary for this step).
- `research/AUDIT_REPORT.md` — modified locally by the E5.3-checkpoint auditor run earlier this
  session; unrelated to E5.4, not part of this pass's work.
- The ~11 pre-existing untracked historical `research/*.md` audit files from earlier phases (E4/E5.1/
  E5.2/E5.3) — unrelated to this checkpoint.
