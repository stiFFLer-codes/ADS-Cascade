# E5.3 — Public Reproducibility Audit

> Read-only audit. No file was modified. No experiment was run. No manuscript, script, or
> documentation was changed. Central question: could an independent, technically competent
> researcher, starting only from the public GitHub repository, reproduce the Experiment 1 evidence
> reported in `manuscript/main.tex` and understand how it was generated — without this conversation,
> Claude Code, private production data, or undocumented assumptions?

---

## 1. Executive verdict

**The Experiment 1 evidence itself is genuinely, deterministically reproducible from committed public
artifacts — the science checks out.** But an external researcher cannot currently get there by
following this repository's own documented path, for three independent, concrete, verifiable reasons:

1. **Discoverability failure.** `README.md` and `docs/INDEX.md` — the repository's only two
   navigation entry points — contain **zero** mention of `manuscript/`, `scripts/experiments/exp1/`,
   or the `research/` directory (60 files). Both explicitly route a reader toward `TECHNICAL_REPORT.md`
   and `STATE.md`, artifacts of the *original* production-engineering narrative (Phase 1/2), not the
   arXiv-track manuscript this audit concerns. A researcher who does exactly what the README says —
   "Start here: 1. Read TECHNICAL_REPORT.md" — will never learn Experiment 1 exists.
2. **README self-contradicts on this exact point** (found by the independent auditor pass, §11
   below): README's own "Folder map" table asserts `requirements.txt` contains "rapidfuzz, requests,
   boto3, pypdf" — it does not; the file contains only `pandas`, `requests`, `tqdm`. The public
   document doesn't just omit the gap, it asserts the opposite of the true state.
3. **Undocumented dependency.** The single documented reproduction command
   (`python scripts/experiments/exp1/run_final.py`, stated verbatim in the manuscript's own
   Reproducibility Statement) imports `rapidfuzz` via `mechanisms.py`. `rapidfuzz` is **not listed
   anywhere in `requirements.txt`** (which contains only `pandas`, `requests`, `tqdm` — a file whose
   own header, "Step 1 — build_inventory," shows it was written for the original Phase 1 pipeline and
   never updated for Phase 2 or Experiment 1). A clean-environment researcher who runs
   `pip install -r requirements.txt` then the documented command hits an immediate
   `ModuleNotFoundError`.

Both defects are independently fixable without touching any scientific content, frozen evidence, or
the manuscript's claims — they are pure documentation/packaging gaps, not integrity problems. Once
fixed, the underlying evidence chain (config → seeds → code → frozen CSVs → headline statistics)
is tight, internally consistent, and genuinely Tier-1-reproducible.

---

## 2. External-researcher walkthrough (simulated clean checkout)

Starting at `README.md`, knowing nothing about this project in advance:

| # | Question | What actually happens | Required inference/search? |
|---|---|---|---|
| 1 | What is this paper about? | README describes ADS-Cascade as a "data-driven method for deciding how much of a classification problem actually needs a model," pointing to `TECHNICAL_REPORT.md` as "the paper." | No inference needed — but this is the *wrong* paper for this audit's subject (`manuscript/main.tex`), and README never mentions the latter exists. |
| 2 | Where is Experiment 1? | Not mentioned anywhere in README, `docs/INDEX.md`, or the README's own "Folder map" (which lists `scripts/` only as "Phase 1 pipeline (01-04) and Phase 2 (phase2/...)"). | **Yes — a researcher must independently browse the GitHub file tree and notice `scripts/experiments/exp1/` exists**, with no textual pointer anywhere telling them to look. |
| 3 | What command runs it? | Once `scripts/experiments/exp1/` is found (by browsing, not being told), `run_final.py`'s own docstring says `Run: python scripts/experiments/exp1/run_final.py` — clear once you're in the right file. | Yes, to get there; no, once there. |
| 4 | What environment is required? | No `README.md` inside `manuscript/` or `scripts/experiments/exp1/`. Top-level `requirements.txt` exists but omits `rapidfuzz` (required) and `matplotlib` (required only for figures, and already self-documented as missing inside `generate_figures.py`'s own docstring). | **Yes — the researcher discovers the gap only by attempting to run the script and reading the resulting `ModuleNotFoundError` traceback.** |
| 5 | Where is the synthetic generator? | `scripts/00_generate_synthetic.py`, loaded via `_loader.py`'s `importlib` shim (its own docstring explains why: the filename isn't a valid Python identifier). Discoverable once inside `scripts/experiments/exp1/`. | Minor — the loader shim itself is well-commented. |
| 6 | Where is the frozen configuration? | `run_final.py` embeds it directly as module-level constants with `assert` statements, and writes it to `data/outputs/experiments/exp1/final/final_frozen_config.json` on every run. Very clear once the script is found. | No, once found. |
| 7 | Where are the seeds? | `SEEDS = list(range(31001, 31021))` in `run_final.py`; also persisted to `final_seed_manifest.csv` (241 lines = 240 rows + header, independently verified this pass). | No. |
| 8 | Where are the final results? | `data/outputs/experiments/exp1/final/final_condition_results.csv` — matches the manuscript's stated "240 conditions" exactly (241 lines including header, independently counted this pass). | No, once the `scripts/experiments/exp1/` directory is found. |
| 9 | How are the headline statistics computed? | `stats.py` (whole-set accuracy, paired bootstrap, R3 rule) — stdlib only, no numpy/scipy, confirmed by direct read (`import random`, no other imports). The manuscript's Results section cites the exact same numbers. Understanding the *derivation* of Wilson CIs / binomial p-values from the raw CSV, however, requires reading `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md` (not linked from anywhere public-facing). | Partial — raw stats are transparent in code; the specific banding/aggregation logic behind the manuscript's headline framing (§5.4) is documented only in an unlinked `research/*.md` file. |
| 10 | How are figures regenerated? | `manuscript/figures/generate_figures.py` exists, reads only the frozen CSV, and its own docstring honestly discloses matplotlib was never actually run in the authoring environment. Not listed in `requirements.txt` either. | Yes — same undocumented-dependency pattern as #4. |

**Summary of inference points**: 2 (Q2, Q4/Q10) are genuine discoverability/dependency gaps requiring
the researcher to either browse blindly or debug an import error. 1 (Q9) requires reading unlinked
internal documentation to fully understand (not to reproduce) the headline statistic's exact framing.
The remaining 7 are clear once the researcher is in the right file.

---

## 3. Reproducibility tier classification

| Artifact / claim | Tier | Rationale |
|---|---|---|
| `final_condition_results.csv` (the 240-row raw results, the manuscript's primary evidence artifact) | **T2** | Deterministically regenerable from public code + stdlib config — *but* the one required non-stdlib import (`rapidfuzz`) is undocumented, so "ordinary tooling" (`pip install -r requirements.txt`) does not suffice as currently written. Downgraded from T1 for this reason alone; the science/determinism itself is not in question. |
| `final_seed_manifest.csv`, `final_frozen_config.json`, `final_run_metadata.json` | **T1** | Byproducts of the same script; once the dependency gap is closed, these regenerate trivially and are also already present for direct inspection today. |
| Headline statistics (32/50=64.0%, 32/32, 0/18, 30/30 @ p=1.9e-9, 2/20 @ p=4.0e-4, Wilson CI, Pearson r ranges) | **T2** | Computable from the T2 raw CSV via `stats.py` (stdlib-only, no additional dependency) — same one-dependency caveat as the parent artifact. The *specific banding/framing* logic (realized-ADS bands vs. nominal-target bands) is implemented in `research/*.md`-described post-hoc analysis, not a single runnable script — verifiable by direct CSV inspection but not "one command" regenerable for the exact narrative framing. |
| Calibration artifacts (`ads_calibration_raw.csv`, `retrieval_cutoff_calibration.json`, pilot outputs) | **T3** | Present and inspectable, but regenerating them requires running separate, non-final-run scripts (`calibrate_ads.py`, `calibrate_retrieval_cutoff.py`, `run_pilot.py`) whose own role (calibration vs. final run) is explained only in `research/EXPERIMENT_1_CALIBRATION_REPORT.md`, not in any public-facing README. Not required to reproduce the headline numbers (the final run is self-contained), but a researcher trying to understand *why* cutoff=75 or δ=0.02 were chosen needs these. |
| Figures F1–F4 | **T2** | `generate_figures.py` reads only public frozen data and is fully deterministic — but `matplotlib` is undocumented in `requirements.txt` (same pattern as `rapidfuzz`), and the script's own docstring already discloses it has never actually been executed in the authoring environment. Additionally, `main.tex` currently uses captioned placeholder boxes, not `\includegraphics{}`, for all four figures — expected and explicitly permitted at this phase (`PAPER_CONTRACT.md` §11; figure generation is E5.4, not yet reached), not scored as a defect here. |
| Production case-study figures (91.2% deterministic, weighted ADS 0.847, unweighted ADS 0.964, cross-company alignment 0.695) | **T4** | Correctly and consistently labeled throughout the manuscript as "cited from a confidential engagement, not independently reproducible from this repository." Verified: this qualifier appears at every occurrence checked (Introduction §1.1, Discussion §6.2, Limitations §7.3, Reproducibility Statement). No leak or implied reproducibility found. |
| Repository-wide discoverability of the manuscript/Experiment-1 track from `README.md`/`docs/INDEX.md` | **T5** | The public entry points make no reproducibility claim about Experiment 1 at all (they don't mention it), so there is no *false* claim here — but per the audit brief's own framing, an artifact a competent researcher cannot find is not meaningfully "publicly reproducible" in practice, regardless of what exists three directories deep. Scored T5 to make this gap visible in the tier system, not because any manuscript sentence is factually false. |

---

## 4. 56-question audit results (grouped; full detail folded into sections above/below to avoid repetition)

**A. Discovery (Q1–6):** Frozen config (Q4), seed manifest (Q5), and raw results (Q6) are all
unambiguously identifiable **once inside `scripts/experiments/exp1/`**. The entry point itself (Q1)
and the pilot/calibration/final distinction (Q3) are **not discoverable from any public-facing
document** — only from `research/EXPERIMENT_1_CALIBRATION_REPORT.md` and `run_final.py`'s own
docstring ("FINAL frozen run") once found. Pilot vs. calibration vs. final is clear *within* the code
(`run_pilot.py`, `calibrate_ads.py`, `calibrate_retrieval_cutoff.py`, `run_final.py` — self-explanatory
filenames) but nothing outside `research/` explains this progression to a newcomer.

**B. Experiment execution (Q7–18):** ✅ Single documented command exists (`run_final.py`'s docstring
and the manuscript's Reproducibility Statement both state it identically). ✅ Matches the manuscript's
reported experiment (independently cross-checked: `final_frozen_config.json`'s `TOTAL_CONDITIONS: 240`,
targets, lexical conditions, seeds 31001–31020, cutoff 75, R3 thresholds 0.90/0.70 all match
`manuscript/main.tex` §4 verbatim). ✅ All parameters specified as `assert`-guarded module constants,
not inferred at runtime — genuinely tamper-evident. ⚠️ The command as documented does not run to
completion in a clean environment following only `requirements.txt` (see §1, finding 2).

**C. Dependencies (Q19–24):** ✅ `requirements.txt` exists. ❌ Not sufficient for Experiment 1
(`rapidfuzz` missing) or figure generation (`matplotlib` missing) — both independently confirmed by
direct import-statement inspection of `mechanisms.py` and `generate_figures.py`. ✅ `stats.py` and
`consistency.py` deliberately avoid numpy/scipy (confirmed: stdlib only) — this part of the dependency
story is genuinely minimal, just incompletely documented. No Python-version constraint is stated
anywhere (not scored as a separate defect — the code uses no version-specific syntax found during this
pass, but this is unverified beyond inspection).

**D. Data (Q25–30):** ✅ No confidential production data required anywhere in the Experiment 1 path —
independently confirmed via `mechanisms.py`, `consistency.py`, `stats.py`, `run_final.py` import
graphs; `00_generate_synthetic.py` is the only data source and is itself synthetic/public. ✅ Frozen
results are clearly distinguished from what a fresh run would produce (both the manuscript's
Reproducibility Statement and `run_final.py`'s own header comment state the exact frozen commit,
`3c6b581178aa7cd3598e112f96f1321d61d60aa9`, that produced the currently-committed artifacts).

**E. Result reproduction (Q31–39):** The raw artifacts (`final_condition_results.csv`,
`final_summary.csv`, `final_bootstrap_results.csv`) are all present and, once the dependency gap is
closed, regenerate byte-for-byte from the same frozen config and seeds (deterministic RNG per
condition, confirmed by `run_final.py`'s `gen.gen_dataset(seed=seed, ...)` call pattern — no shared
mutable global generator). The specific headline percentages (32/50=64.0%, 32/32, 0/18, etc.) require
the post-hoc banding logic described in `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`, which is not
itself a single runnable script producing exactly that framing — a researcher can recompute the
underlying numbers from the CSV directly (the columns needed, e.g. `realized_det_pct`,
`r3_agrees_with_empirical`, are all present) but must do their own aggregation to reproduce the exact
banded presentation, or read that internal document to see how it was done. Not a blocker, but a real
gap between "the CSV is here" and "the manuscript's Table 4/5 numbers, at a glance, one command away."

**F. Figures (Q40–45):** See tier table above (§3) and the dedicated figure audit (§8 below).

**G. Manuscript↔repository consistency (Q46–52):** ✅ Verified directly: `scripts/experiments/exp1/run_final.py` exists at the exact path the manuscript cites; `final_condition_results.csv` exists at the exact path cited in the Reproducibility Statement; every number spot-checked in `final_frozen_config.json` against `manuscript/main.tex` §4 matches. ✅ Confidential production statistics are consistently, correctly labeled at every occurrence found. No instance found of a manuscript sentence implying the *entire* study (rather than specifically the synthetic Experiment 1 evidence) is reproducible.

**H. External-researcher experience (Q53–56):** Answered in full in §2 above. On Q56 specifically —
**no, a researcher cannot currently reproduce or even discover Experiment 1 without independently
browsing the repository tree or reading internal `research/*.md` files**; there are 60 files in
`research/` and zero index or README pointing into that directory from any public-facing entry point.
`docs/INDEX.md` — the repository's own stated navigation index — does not mention `research/`,
`manuscript/`, or `scripts/experiments/` even once.

---

## 5. Reproducibility scorecard

| Area | Tier | Evidence | Problem | Severity | Required action |
|---|---|---|---|---|---|
| Experiment discovery | T5 (discoverability only — no false claim) | `README.md`, `docs/INDEX.md` full-text read, zero hits for "Experiment 1," "manuscript," "arXiv," or `scripts/experiments` | No public entry point links to the arXiv-track manuscript or Experiment 1 at all | **HIGH** | Add a pointer from `README.md` (and/or `docs/INDEX.md`) to `manuscript/main.tex` and the Experiment 1 reproduction command — a documentation-only fix |
| Configuration | T1 | `final_frozen_config.json` cross-checked field-by-field against `manuscript/main.tex` §4 — exact match | None found | INFO | None |
| Seeds | T1 | `final_seed_manifest.csv` (241 lines = 240+header), `SEEDS = range(31001, 31021)` in `run_final.py`, matches manuscript | None found | INFO | None |
| Synthetic generator | T2 | `scripts/00_generate_synthetic.py` exists, loaded via documented `_loader.py` shim; generator itself uses no confidential data | Loader mechanism (importlib shim for a non-identifier filename) is non-obvious to a newcomer without reading `_loader.py`'s own docstring | LOW | Optional: a one-line README note in `scripts/experiments/exp1/` (out of scope for this audit to add) |
| Final execution | T2 | `run_final.py` is single-command, fully parameterized, asserts its own frozen config | `rapidfuzz` import (via `mechanisms.py`) fails on a clean `pip install -r requirements.txt` environment | **HIGH** | Add `rapidfuzz` to `requirements.txt` (or a scoped `requirements-exp1.txt`) |
| Result artifacts | T1 | `final_condition_results.csv`/`final_summary.csv`/`final_bootstrap_results.csv`/`final_run_metadata.json` all present, internally consistent, row counts match manuscript's "240 conditions" claim exactly | None found | INFO | None |
| Statistics | T2 | `stats.py` is stdlib-only (verified: no numpy/scipy import), computes whole-set accuracy, paired bootstrap, R3 rule | The exact realized-ADS-band vs. nominal-target-band framing behind the manuscript's headline numbers lives only in an unlinked `research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`, not a single script a reader can just run | MEDIUM | Optional: a short public-facing note (or script) showing the banding derivation from the raw CSV — not required for the numbers to *exist* publicly, only for one-command reproduction of the exact table framing |
| Figures | T2 | `generate_figures.py` reads only public frozen data, deterministic, self-documents its own untested status | `matplotlib` undocumented in `requirements.txt`; figures not yet wired into `main.tex` via `\includegraphics{}` | MEDIUM (dependency) / INFO (wiring — explicitly deferred to E5.4, not a defect now) | Add `matplotlib` to `requirements.txt` (dependency fix only; figure-wiring is E5.4's job) |
| Dependencies | T2 | Direct import-statement inspection of every exp1 module + `generate_figures.py` | `requirements.txt` is stale (header comment shows it predates Phase 2/Experiment 1 entirely); missing `rapidfuzz` and `matplotlib` | **HIGH** | Update `requirements.txt` to include both, or add a scoped file |
| Documentation | T3 | `docs/INDEX.md` full read; `research/` directory has 60 files, no internal index | No public-facing document explains the Phase A–E research pipeline, Experiment 1's existence, or how to navigate `research/` | **HIGH** | A short public pointer document or README section (out of scope to add during this read-only audit) |
| Manuscript consistency | T1 | Direct cross-check of every path/number cited in the Reproducibility Statement against actual repo state | None found — every cited path exists, every cited number matches | INFO | None |
| Production boundary | T4 (correctly scoped) | Grepped all four production numbers (91.2%, 0.847, 0.964, 0.695) across the manuscript; every occurrence carries the "cited... not independently reproducible" qualifier | None found | INFO | None |

---

## 6. Manuscript reproducibility-claim audit

Full text of the manuscript's Reproducibility Statement (`manuscript/main.tex` §"Reproducibility
Statement", quoted verbatim above in §1) plus every other `reproduc*`/`regenerat*`/`frozen`/
`deterministic`/`public`/`artifact` occurrence (17 total, grepped exhaustively) was checked. **No
instance found** of language implying "the entire study is reproducible" — every reproducibility claim
is already correctly scoped to "the generator, both mechanisms, the lexical perturbation model, and
the calibration and analysis code," with the production case study explicitly and separately carved
out as "confidential and not reproducible from this repository in any sense" in the same paragraph.

**The one imprecision found**: the claim "re-running `python scripts/experiments/exp1/run_final.py`
reproduces `final_condition_results.csv` exactly" is **true given a correctly-provisioned
environment**, but the sentence doesn't state what "correctly-provisioned" requires, and the one thing
it silently requires (`rapidfuzz`) isn't documented anywhere the sentence points to (`requirements.txt`).
This is a completeness gap in an otherwise accurate claim, not a false statement — the manuscript never
says "no dependencies beyond `requirements.txt`" outright, but a reader would reasonably assume it,
and the actual gap only surfaces via a failed run.

---

## 7. Production/confidentiality boundary audit

| Statistic | Occurrences checked | Every occurrence labeled confidential/non-reproducible? | Tier |
|---|---|---|---|
| 91.2% deterministic products | §1.1 (Introduction), §7.3 (Limitations) | ✅ Yes, both times ("cited from a confidential engagement, not independently reproducible from this repository" / "generated by an earlier version of the measurement pipeline... likely understated and unverified") | T4 |
| Weighted ADS 0.847 | §7.3 (Limitations) | ✅ Yes | T4 |
| Unweighted ADS 0.964 | §7.3 (Limitations) | ✅ Yes | T4 |
| Cross-company alignment 0.695 | §4.2 (Experimental Design, as the fixed generator parameter) | ✅ Yes — "the production-observed value, cited from a confidential engagement and not independently reproducible from this repository" | T4 (as a cited motivating constant; the synthetic generator's *use* of this fixed value is itself T1/T2 — the value's *provenance* is T4) |

**No case found** of the manuscript implying confidential production data can be independently
regenerated, or of production evidence appearing inside the Results section (§5, confirmed empty of
all four numbers by direct grep — same check performed during the E5.2 audit, reconfirmed here).

---

## 8. Figure reproducibility audit

`manuscript/figures/generate_figures.py`, read in full (not executed — running it would require
installing an undocumented dependency, matplotlib, which itself is one of this audit's findings; not
run here to keep this pass strictly read-only and avoid any environment side effects):

1. **What figures does it generate?** F1 (experimental design flow, a static schematic, not
   data-driven), F2 (ADS vs. mechanism accuracy scatter, both lexical conditions), F3 (R3 agreement by
   realized-ADS band, VARIED only), F4 (mechanism-ranking constancy, rules−retrieval accuracy gap vs.
   realized ADS). Matches the four figures (`fig:f1`–`fig:f4`) referenced in `manuscript/main.tex`.
2. **Does it read only public frozen evidence?** ✅ Yes — `RESULTS_CSV` points exclusively to
   `data/outputs/experiments/exp1/final/final_condition_results.csv`; no other data source.
3. **Are all required inputs present?** ✅ Yes — that CSV exists and was independently verified
   present with 240 data rows this pass.
4. **Does it produce the four manuscript figures?** ✅ Structurally yes (F1–F4, matching labels/content
   described in each `make_fN` docstring against the corresponding manuscript figure caption).
5. **Are generated filenames aligned with manuscript references?** ⚠️ **Not yet** — the script writes
   `f1_design_flow.pdf` through `f4_ranking_constancy.pdf`, but `main.tex`'s current figure blocks are
   captioned placeholder `\fbox{}` boxes, not `\includegraphics{}` commands referencing these paths.
   This is expected and explicitly permitted at the current phase (`PAPER_CONTRACT.md` §11: "a
   captioned placeholder without a rendered image is a valid slot"), and figure generation/wiring is
   E5.4, not yet reached — **not scored as a defect of this audit**, noted for completeness only.
6. **Are the outputs deterministic?** ✅ Yes — purely reads a frozen CSV and computes scatter/bar
   plots with no randomness; two runs would produce byte-identical (or near-identical, modulo
   matplotlib's own PDF-metadata timestamping, a common and expected exception) output.
7. **Is matplotlib actually documented as a dependency?** ❌ **No** — absent from `requirements.txt`;
   the script's own docstring self-discloses this ("matplotlib is not installed here... the gap is
   reported explicitly rather than faked") — an honest, pre-existing acknowledgment, not a new finding,
   but still an actionable dependency-documentation gap.
8. **Can a researcher run it from a clean environment?** ❌ Not from `pip install -r requirements.txt`
   alone — same gap as finding 2 in §1.

**Not executed this pass** — running it would install/require an undocumented dependency and produce
new output files, which falls outside this audit's strictly read-only, no-file-modification mandate;
noting this explicitly per the task's own instruction rather than silently running it.

---

## 9. Missing-information inventory

Information that currently exists only in internal `research/*.md` planning/audit documents, not in
any public-facing documentation:

- That `manuscript/main.tex` (the arXiv-track paper) exists at all, and supersedes/differs from
  `TECHNICAL_REPORT.md` (the original production-engineering report) in framing and locked contribution.
- That Experiment 1 exists, what it tested, and where its code lives.
- The pilot → calibration → final progression and why each stage exists (`research/EXPERIMENT_1_CALIBRATION_REPORT.md`, `research/EXPERIMENT_1_REDESIGN_REVIEW.md` — neither linked publicly).
- The exact banding/framing logic behind the manuscript's headline statistics (`research/EXPERIMENT_1_POSTHOC_ANALYSIS.md`).
- That `rapidfuzz` and `matplotlib` are required beyond `requirements.txt`.
- The Phase A–E research/audit trail's existence and purpose (60 files in `research/`, zero index).

---

## 10. Required fixes, ranked by severity

| Rank | Severity | Fix | Scope |
|---|---|---|---|
| 1 | **HIGH** | Add `rapidfuzz` to `requirements.txt` (blocks the one documented reproduction command from completing) | `requirements.txt` only |
| 2 | **HIGH** | Add a discoverability pointer from `README.md` and/or `docs/INDEX.md` to `manuscript/main.tex` + the Experiment 1 reproduction command | `README.md` / `docs/INDEX.md` only |
| 3 | **HIGH** | (Same root cause as #1, listed separately in the scorecard as its own "Documentation" row) — no public document explains the Phase A–E pipeline exists | Documentation only |
| 4 | MEDIUM | Add `matplotlib` to `requirements.txt` (figure generation, not yet on the critical reproduction path since figures aren't wired into `main.tex` yet) | `requirements.txt` only |
| 5 | MEDIUM | Optional: a short public note or script showing the exact realized-ADS-band derivation from the raw CSV, so the manuscript's Table 4/5 framing is one-command reproducible, not just the underlying numbers | New, small, optional |
| 6 | LOW | Optional: a one-line note on the `_loader.py` importlib shim for newcomers | Documentation only |

**None of these are BLOCKER-severity** — the underlying science, frozen evidence, and code are sound
and internally consistent; every gap found is a documentation/packaging completeness issue, fixable
without touching any number, claim, or frozen artifact. Per this task's explicit no-fix mandate, none
of the above has been applied.

---

## 11. Auditor disagreement/reconciliation

Independent `research-code-auditor` pass (`research/E5_3_INDEPENDENT_REPRODUCIBILITY_AUDIT.md`,
verdict 🟠 ORANGE/CONDITIONAL) formed its own judgment from primary sources before reading this
report, then reconciled. **Full agreement on every dimension checked**: same discoverability failure,
same broken clean-install command, same solid frozen-artifact integrity, same pre-authorized
(not-yet-reached) figure-wiring gap, same clean production/confidentiality boundary, same
"documentation/packaging gap, not a research-integrity issue" characterization.

**Two findings the independent pass surfaced that this report missed:**

1. **README self-contradicts on the exact defect.** `README.md`'s own "Folder map" table states
   `requirements.txt       Python dependencies (standard library first; rapidfuzz, requests, boto3,
   pypdf)` — but `requirements.txt` as actually written contains only `pandas`, `requests`, `tqdm`.
   README claims the very package (`rapidfuzz`) that this audit independently proved is missing is
   present. This is a sharper, more directly citable piece of evidence than anything in this report's
   §1/§10 — the discoverable public document doesn't just fail to mention the gap, it asserts the
   opposite of the true state.
2. **`STATE.md`'s own "How to run / resume" section (lines 197–207)** — the exact section README's
   §3 promises covers "how to run the pipeline" — lists only the Phase 1/2 production scripts and
   omits Experiment 1 entirely. Stronger, more specific evidence for the discoverability finding
   (§1/§5/§10) than this report's more general "STATE.md is written for AI session handoff" framing.

**One item the independent pass could not verify**: this report's §3/§4/§5 claim that the exact
realized-ADS-band framing behind the manuscript's headline numbers requires reading
`research/EXPERIMENT_1_POSTHOC_ANALYSIS.md` (not a single runnable script) was outside the
independent pass's six targeted checks — flagged by that pass as *unverified by them*, not
contradicted. Retained as-is in this report; would benefit from a third-pass confirmation before
being treated as fully settled, though it does not change the overall verdict either way.

No disagreement found on severity ranking, tier classification, or the "no BLOCKER, no
research-integrity violation" conclusion.

---

## 12. Final recommendation

Do not proceed to E5.4 (figure generation) or E6 under the assumption that reproducibility is already
solid — it is *substantively* solid (the science reproduces) but *practically* blocked for an external
researcher by two small, mechanical, non-scientific fixes (§10, ranks 1–2). Recommend those two fixes
be scoped as their own bounded, human-approved correction checkpoint (mirroring E5.2's pattern) before
E6's final adversarial review, since E6 will otherwise inherit the same discoverability/dependency
gaps found here.
