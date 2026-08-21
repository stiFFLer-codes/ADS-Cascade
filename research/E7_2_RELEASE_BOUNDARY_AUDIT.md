# E7.2 — Final Public-Release Boundary Audit (arXiv Preprint Prep)

> Read-only gatekeeping review. Nothing in this repository was modified, staged, or committed by
> this pass. This is a **new, currently-untracked file** as of this audit — it has not been
> committed. Scope, per the brief: public GitHub safety, manuscript boundary, arXiv package
> correctness, disposition of the 12 untracked internal audit files, and a scientific-drift
> spot-check against `research/CONTRIBUTION_LOCK.md` / `research/EXPERIMENT_1_FINAL_RESULTS.md`.
> E7.1 (author metadata, AI-disclosure) is closed and was not re-litigated.

---

## 1. Repository state

- Branch: `main`. HEAD: `8c214e092f3ffe024fa38044556be1e5edbe8e1d` ("Phase E7.1: manuscript author
  metadata + AI-assistance disclosure"), committed 2026-08-17 14:34:27 +0530.
- Working tree: clean relative to HEAD except 12 untracked files, all under `research/`, all
  `E4_*`/`E5_1_*`/`E5_2_*`/`E5_3_*`/`E5_GPS_*` audit reports (see §3, §9).
- Diffed: `git ls-files` (full tracked tree, 207 files) grepped directly; `manuscript/main.tex`
  (1,472 lines) and `manuscript/references.bib` (184 lines) read in full; recent commit history
  (`git log -5 --stat`) reviewed; `research/RESEARCH_GPS.md`, `STATE.md`,
  `research/PUBLIC_RELEASE_BOUNDARY.md`, `research/CONTRIBUTION_LOCK.md`,
  `research/EXPERIMENT_1_FINAL_RESULTS.md` read/grepped for cross-checks.

## 2. Current research GPS

`RESEARCH_GPS.md`'s own "CURRENT LOCATION"/"CURRENT GATE" text is stale relative to the actual
repo state: it still describes E5.2 as the open gate. The committed history shows E5.2 through E7.1
are all done (`5c8c5b4` E5.5, `50bfad0` E6, `8c214e0` E7.1), and the task brief describes E7.2 as
current. **This is a staleness finding, not a contradiction** — GPS is not mine to rewrite (per my
own operating constraints), but it should be updated by the author/builder to reflect E5.3–E7.1
completion before the next research session relies on it. North star (defensible manuscript →
reproducibility package → arXiv preprint) is intact and this session's work (a boundary/packaging
audit) is squarely on that path, not a detour.

## 3. Changed files

Nothing was changed in this session (read-only). Relative to the last committed state, the working
tree carries only the 12 untracked `research/*.md` files listed in the task brief — all internal
audit/process reports (see §9), zero code, zero manuscript, zero experimental artifacts.

- Docs: 0 changed (this audit's own output file is new, not yet committed)
- Code: 0 changed
- Experimental artifacts: 0 changed
- Manuscript: 0 changed (E7.1 was the last manuscript touch, already closed per the brief)
- Other: 12 new untracked internal audit reports (process-only)

## 4. Research integrity

**Not applicable in the "new violation" sense — no research content changed this session.** As a
verification exercise, I independently re-checked `manuscript/main.tex` prose against every item on
the known-rejected-claims list:

- ADS-as-novel-metric: main.tex §2.1 explicitly states "we make no claim that ADS is a novel
  metric... this is a closed question" and gives the correct cluster-purity/majority-vote framing.
  Correct.
- General design-time-architecture-selection novelty: main.tex §2.2 explicitly disclaims novelty
  ("We make no claim that design-time selection from historical evidence is itself new") and scopes
  the narrower claim correctly. Correct.
- Combined-system novelty: not asserted anywhere in main.tex; no B1–B5 baseline comparison is
  claimed to exist. Correct (absence, not overclaim).
- "No comparable vendor practice" (Romanian D406 framing): main.tex §2.4 explicitly states "at
  least one industry source \citep{kenfromfinance2025}... directly contradicts that framing" — this
  is the corrected framing, not the rejected one. Correct.
- Universal/broad "enterprise AI" applicability: not present; main.tex repeatedly scopes to "this
  synthetic experiment," "this generator," explicit non-generalization language throughout §6–§7.
  Correct.
- "R3 selects the right mechanism": main.tex §5.4/§6.3 explicitly reports 0/18 (0%) exceptionless
  disagreement in the ≥0.90 band and states this "falsifies" the unconditional original hypothesis.
  The rejected claim is not resurrected — the opposite is stated. Correct.

No resurrected rejected claim found. This matches the brief's framing that E7.1 didn't touch
scientific content and my own read of the diff confirms it (`50bfad0`→`8c214e0` only touched
`manuscript/main.tex` author/date/acknowledgements block, +29/-5 lines, all in the front matter and
a new Acknowledgements section — verified via the commit's own `git show --stat` in §1's log output;
no Results/Discussion/Limitations line was touched).

## 5. Scientific consistency

Traced main.tex's full argument chain (RQ → H1 → design → results → interpretation → contribution)
end to end while reading it in full for this audit. It holds together: H1 stated pre-registered
(§4.1), PARTIALLY_SUPPORTED verdict stated without softening in Discussion (§6.3) and Limitations
(§7.1, deliberately promoted to lead per E5.1's own documented reordering), and the accuracy/ranking
(6a/6b) separation is maintained in every section that touches it (Problem Setting §3.3, Results
§5.2 vs §5.3, Discussion §6.1, Conclusion). No A5/A6-shaped drift (script behavior vs. documented
behavior, or aggregation changing without re-derivation) was found in this pass — no code changed,
so there was no new opportunity for that class of bug to be introduced this session.

## 6. Evidence/claim traceability

Independently re-derived/cross-checked every headline quantitative claim in main.tex against the
frozen evidence docs (not against another document's restatement of it):

| main.tex claim | Cross-checked against | Result |
|---|---|---|
| Pearson r = 0.909/0.959 (rules), 0.948/0.955 (retrieval) | `EXPERIMENT_1_FINAL_RESULTS.md` L165-166 | Exact match |
| 32/32 (100%) realized 0.70–0.90 band, 0/18 (0%) realized ≥0.90 band | `EXPERIMENT_1_FINAL_RESULTS.md` L72-73, `CONTRIBUTION_LOCK.md` L408 | Exact match |
| Overall 32/50 = 64.0%, CI [50.14%, 75.86%], p=0.0649 | `EXPERIMENT_1_FINAL_RESULTS.md` L22, L123, L130 | Exact match (CI bound rounding 50.1%/50.14% consistent) |
| By-target 30/30 p=1.9×10⁻⁹, 2/20 p=4.0×10⁻⁴ | `CONTRIBUTION_LOCK.md` L72-73 | Exact match |
| PARTIALLY_SUPPORTED verdict | `CONTRIBUTION_LOCK.md` L75, `EXPERIMENT_1_FINAL_RESULTS.md` L172 | Exact match |
| Table T5 per-band gap values (+0.0048...-0.1851) | Cited to `EXPERIMENT_1_POSTHOC_ANALYSIS.md` §5, "reproduced verbatim, not re-derived" per main.tex's own comment | Traceable; not independently re-derived from raw CSV this pass (out of scope — no experimental artifact changed) |

No number in main.tex was found presented as settled without a frozen-artifact anchor.

## 7. Code review

**Not applicable — no code changed this session.** `generate_figures.py` and the four figure PDFs
are unchanged since the last commit (`8c214e0` touched only `main.tex`); their file timestamps
(Aug 14/17, matching prior commits E5.4/E5.5) are consistent with no silent regeneration having
occurred outside a committed checkpoint.

## 8. Experimental integrity

**Not applicable — no experimental artifacts changed this session.** Frozen evidence under
`data/outputs/experiments/*/final/` was not touched, read for modification, or otherwise
interacted with beyond citation-cross-check in §6.

## 9. Scope/GPS alignment

The 12 untracked files are all internal, read-only, process/checkpoint audit reports covering
already-closed phases (E4 checkpoint staging, E5.1 GPS closeout, E5.2 citation audits, E5.3
reproducibility audits, E5.0 GPS housekeeping) — confirmed by reading each file's header and a
verdict-line grep. Every one self-describes as read-only, "no file modified, staged, or committed."
None contains a scientific claim, a manuscript edit, or a code change — they are meta-audits of
prior audits (the project's convention of running 2-4 independent verification passes per
checkpoint before a human commits). They correctly stay out of both the arXiv package (never in
scope for that — per `PUBLIC_RELEASE_BOUNDARY.md` §3.B, internal research-governance docs are
explicitly excluded from the arXiv source tarball) and, for now, out of git (staging/committing them
is a human decision this audit does not make). A quick secret/local-path scan of all 12 found
nothing (§10). This is in-scope, expected artifact accumulation for the project's own audit
convention, not scope creep or a detour from the north star.

## 10. Git hygiene

- `git status --porcelain`: exactly the 12 untracked files named in the brief, nothing else
  unexplained. No unstaged modifications to any tracked file.
- Secret/credential scan of the full tracked tree (`git ls-files` + `git grep`): zero AWS key
  patterns (`AKIA...`), zero private-key headers, zero live Groq/API key literals (the two `gsk_...`
  hits are prose describing the env-var format in `STATE.md`/`p2_06_llm_tail.py`'s own help text and
  a pattern-description in `PUBLIC_RELEASE_BOUNDARY.md` — not literal secrets, consistent with four
  prior audits' independent confirmation of the same false positive), zero `amazonaws.com`/`s3://`
  hits, zero generic `password=`/`bearer <token>`/`secret=` assignments.
- Real-email scan: only `maitreyasapariya@gmail.com` (intentional, author's own, per E7.1), in
  `manuscript/main.tex` and one audit report quoting it. No other email found.
- Local-path/username scan: zero `C:\Users\...` or `/Users/<name>/...` hits in any *tracked* file
  content (the string `MaitreyaSapariya` and `C:\Users\Maitreya` appear only inside prior audit
  reports' own prose *describing the grep pattern they searched for*, already independently
  confirmed false-positive by four earlier audits — re-confirmed here, not re-litigated blindly).
- AWS IAM username `contai-textract` + region `ap-south-1`: **confirmed still the only such
  internal-infrastructure identifier**, still only in `STATE.md` (Phase 2 OCR provisioning
  history), still not referenced anywhere in `manuscript/main.tex`
  (`TECHNICAL_REPORT.md`/manuscript both describe the OCR provider generically). No new instance,
  no worse instance, found. This matches `PUBLIC_RELEASE_BOUNDARY.md`'s prior finding exactly.
- Real-company-name scan: `Rompetrol`/`OMV Petrom` appear only as pattern-descriptions inside audit
  prose (`METHODOLOGY.md`, `PUBLIC_RELEASE_BOUNDARY.md`, `artifact_inventory.csv`) describing what
  was anonymized, not as live content. `docs/demo/index.html` and `STATE.md` contain "PETROMAX" /
  "CARPATGAS" (explicitly labeled "vendor names anonymized (fictitious)" in the demo HTML's own
  inline comment, `docs/demo/index.html:637`) and the generic fuel-product-type string "omv
  maxxmotion 95" (a real product/brand name, not a client identity — the same category as citing
  "Coca-Cola" as a line-item description). This is pre-existing, already-public content predating
  this session (present since the original Phase 2 demo commit), already covered by
  `METHODOLOGY.md`'s public/confidential boundary and not part of the manuscript or arXiv package.
  Flagged as an observation, not a new finding — see §11 F1.
- No `.aux`/`.log`/`.bbl`/`.blg`/build-artifact files tracked. No `.bak`/`.swp`/`.orig`/`.tmp` files
  tracked. `.gitignore` correctly excludes `.env`, `*.key`, `*_secret*`, `aws_credentials*`,
  `__pycache__/`. Note: `manuscript/figures/__pycache__/` exists on disk (from running
  `generate_figures.py`) but is correctly gitignored and not tracked — confirmed via `git ls-files
  manuscript/` showing no `__pycache__` entries.
- `README.md`/`TECHNICAL_REPORT.md`/`METHODOLOGY.md`: no uncommitted changes present; this pass
  made none.
- Nothing should be `git add`-ed as a result of this audit — it produced only this new report file,
  which is itself an internal document out of scope for commit-or-not decisions per the audit
  agent's own constraints.

## 11. Findings

**F1 (OPTIONAL FUTURE WORK).** `docs/demo/index.html`/`STATE.md` contain the real fuel-brand
product-type string "omv maxxmotion 95" and fictitious-but-real-sounding vendor names
("CARPATGAS", "PETROMAX") in a Phase-2 stakeholder-demo worked example. Already public since before
this session, already anonymized at the company-identity level per `METHODOLOGY.md`, and outside
both the manuscript and the arXiv package scope. Not a new leak. If the author wants a stricter
bar, replacing the specific real product-type string is a one-line optional cleanup, not required
for arXiv submission since neither file ships in the arXiv tarball or is cited by the manuscript.

**F2 (REQUIRED NOW — before arXiv submission, not before this checkpoint).**
`manuscript/references.bib`'s `dawidskene1979` entry has `volume = {TODO}`, `number = {TODO}`,
`pages = {TODO}`, `doi = {TODO}` as literal field values (lines 60-63), not omitted fields. Under
standard `plainnat`/BibTeX semantics, a field that is *present* with a literal string value renders
that literal string in the compiled bibliography — there is no BibTeX convention that treats the
text "TODO" as "omit this field." Because `main.tex` uses `\nocite{*}` (line 1467), every bib entry
including this one is forced to render in the compiled reference list regardless of whether it's
cited in-text elsewhere. The predictable, verifiable consequence: the compiled PDF's bibliography
will show the literal word "TODO" repeated four times in the Dawid & Skene (1979) entry — a
concretely embarrassing, unprofessional rendering defect in a document intended for arXiv
distribution. I could not root-compile to visually confirm (no pdflatex/bibtex/MiKTeX on this
machine, consistent with the environment gap the requester already found), but this conclusion
follows directly from documented BibTeX field-rendering behavior, not speculation. **Fix before
packaging for arXiv:** either resolve the real volume/number/pages/DOI (Dawid & Skene 1979, JRSS
Series C, is a well-known, easily-verified citation — vol. 28, no. 1, pp. 20-28,
doi:10.2307/2346806, but this audit does not independently verify that value; a human/researcher
pass should confirm before entering it) or remove the three placeholder fields entirely (BibTeX
gracefully omits missing optional fields for `@article`).

**F3 (OPTIONAL FUTURE WORK, but recommended before final arXiv polish).**
`rankgpt2023`'s `author = {Sun and Yan and Ma and others}` field (line 97) is syntactically valid
BibTeX (the `and others` construct is a real, standard convention in `plain`/`plainnat`-family
`.bst` files that triggers an "et al." rendering) and will **not** render broken — but it will
render as three bare surname-only entries plus "et al." (no given names/initials, since none were
supplied), which is noticeably less complete than every other entry in the same bibliography. Not
a rendering defect, just a completeness gap already self-flagged in the file's own inline comment
("expand before E5" — that milestone has since passed per the git log without this being resolved).
Low priority, does not block arXiv submission, but worth closing before final polish since it is
publicly visible in the same reference list as F2.

**F4 (OPTIONAL FUTURE WORK).** `research/RESEARCH_GPS.md`'s "CURRENT LOCATION"/"CURRENT GATE"
sections describe E5.2 as open/current, but committed history (`git log`) shows E5.3 through E7.1
are already done. This is stale-pointer drift in a document the project explicitly says is "not
mine to rewrite" — flagging for the human/builder to update, not fixing.

**F5 (informational, not a finding).** No pdflatex/bibtex/MiKTeX is installed on this machine, so
the arXiv package's actual compilability could not be root-verified end-to-end (e.g., whether
`\nocite{*}` plus 14 entries compiles cleanly, whether `natbib`+`plainnat` resolves without warning
beyond the F2/F3 items identified by static inspection). This is a genuine environment gap, not a
repository defect — consistent with what the requester already found. Recommend the author either
install a minimal TeX Live/MiKTeX locally or use arXiv's own compilation-preview step (arXiv
recompiles from source on submission and will surface any remaining LaTeX error) before finalizing.

**F6 (confirms no issue — stated for completeness).** The arXiv package's minimal correct file set
is `manuscript/main.tex` + `manuscript/references.bib` + the 4 figure PDFs in
`manuscript/figures/` (`f1_design_flow.pdf`, `f2_ads_vs_accuracy.pdf`, `f3_r3_agreement_by_band.pdf`,
`f4_ranking_constancy.pdf`). `generate_figures.py` and its `__pycache__/` should not be bundled (the
figures are pre-rendered PDFs referenced by `\includegraphics`, the generator script is
reproducibility-package material, not paper source). Confirmed via `\usepackage` grep: only
`amsmath`, `amssymb`, `graphicx`, `booktabs`, `natbib[round]` — all in every standard TeX Live/MiKTeX
distribution, no custom `.sty`/`.cls` needed. `research/*.md`, `data/`, `scripts/`, `architecture/`
etc. correctly stay out of the arXiv tarball per `PUBLIC_RELEASE_BOUNDARY.md` §3.B's own explicit
list — confirmed still accurate on independent re-read.

## 12. Required fixes

1. **F2** — resolve or remove the `TODO` placeholder fields in `references.bib`'s `dawidskene1979`
   entry before the arXiv source package is assembled. This is the only REQUIRED-NOW item; it does
   not block this session's read-only checkpoint (nothing is being committed or packaged right
   now), but it must be closed before `manuscript/` is actually bundled into an arXiv tarball.

## 13. Verdict

🟡 **PASS_WITH_NOTES.**

No research-integrity violation, no resurrected rejected claim, no scientific drift, no secret,
credential, client data, or new confidentiality leak was found anywhere in the tracked tree or the
12 untracked audit files. Every headline number in `manuscript/main.tex` independently traces
byte-for-byte to `EXPERIMENT_1_FINAL_RESULTS.md`/`CONTRIBUTION_LOCK.md`. Git hygiene is clean and
the arXiv package's minimal file set and dependency list are both confirmed correct. The one
concrete, verifiable defect found (F2, the literal "TODO" strings that `\nocite{*}` will force into
the rendered bibliography) is real and will visibly embarrass the submission if not fixed, but it
is narrow, mechanical, already self-flagged in the source file's own comments, and does not touch
any scientific claim, evidence chain, or public-safety boundary — hence PASS_WITH_NOTES rather than
CONDITIONAL or BLOCK. The GPS staleness (F4) and demo-file product-name specificity (F1) are
pre-existing, low-severity, and correctly deferred to the author's judgment rather than blocking
anything now.
