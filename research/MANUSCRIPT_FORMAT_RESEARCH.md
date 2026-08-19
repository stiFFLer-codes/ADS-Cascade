# Manuscript Format Research — Phase E, Task 1-2

> Research-only document. Does not modify `TECHNICAL_REPORT.md`, `README.md`, `METHODOLOGY.md`, or
> any frozen evidence. Answers: what does arXiv currently require, and what manuscript-source
> format should ADS-Cascade's first draft use. All claims below are sourced from official
> `arxiv.org` / `info.arxiv.org` / `blog.arxiv.org` pages, fetched **2026-08-12**. Where an official
> page 404'd or lacked detail, that is stated explicitly rather than backfilled from memory or a
> third-party blog.

---

## 1. Current arXiv requirements (official sources only)

### 1.1 Accepted formats

- **Preferred: (La)TeX / AMS-LaTeX.** arXiv explicitly prioritizes TeX/LaTeX source over anything
  else because it is the most portable/long-term-stable format it can re-process (HTML generation,
  future re-typesetting).
- **Accepted fallback: PDF** — but only a PDF *produced directly from source* (Word, etc.). arXiv
  explicitly **rejects** "dvi, PS, or PDF created from TeX/LaTeX source" submitted as a bare PDF
  (i.e., don't compile your own LaTeX to PDF locally and upload only the PDF — upload the source),
  and rejects scanned documents outright.
- No mention anywhere in official docs of Markdown as an accepted native submission format. A
  Markdown-authored paper would need to be converted to LaTeX or PDF before submission.
- Source: [Format Requirements](https://info.arxiv.org/help/policies/format_requirements.html),
  [Submission process overview](https://info.arxiv.org/help/submit/index.html) — accessed
  2026-08-12.

### 1.2 TeX/LaTeX submission expectations

- Processed with **LaTeX2e**; engine (pdfLaTeX vs. LaTeX→DVI) is auto-detected but overridable.
- Package the whole source tree (`.tex`, `.bib`/`.bbl`, figures, custom `.sty`/`.cls` not already in
  TeX Live) into one `.tar` or `.zip`; compilation runs from the archive root.
- Naming the main file `ms.tex` forces it to be processed first; otherwise files process in
  alphanumeric order — matters for multi-file projects.
- Author **must** view/approve the arXiv-compiled PDF before the submission completes — this is the
  de facto compile check.
- Source: [Considerations for TeX Submissions](https://export.arxiv.org/help/submit_tex) — accessed
  2026-08-12.

### 1.3 Universal template requirement

- **No universal arXiv template exists or is required.** Official docs state plainly there is no
  mandated house style; "follow standard LaTeX conventions." arXiv is a preprint server, not a
  publisher — it does not typeset or reformat submissions beyond what LaTeX itself produces.
- Source: same as 1.2.

### 1.4 Source-package requirements / what to exclude

Include: `.tex`, `.bib` **or** a pre-generated `.bbl`, all figure files actually referenced, any
custom `.sty`/`.cls` not in TeX Live, and (if used) pre-generated `.ind`/`.gls`/`.nls` files — arXiv
does **not** run `makeindex`, `bibtex8`, or glossary processors itself.

Exclude: `.aux`, `.log`, `.toc`, `.dvi`, `.pdf` (of the compiled output), `.ps`, backup files, unused
figures, referee/reviewer material, hidden dot-files/dirs (auto-deleted on announcement anyway).

Bibliography backend consistency matters: the `.bbl` (if precompiled) must have been produced by the
*same* backend as the document uses (BibTeX vs. Biber — never mixed), and must match arXiv's current
TeX Live bbl-format version (3.3 only on TeX Live 2025; 3.2 or 3.3 accepted on TeX Live 2023).

- Source: [Considerations for TeX Submissions](https://export.arxiv.org/help/submit_tex) — accessed
  2026-08-12.

### 1.5 Figure requirements

| Engine | Accepted figure formats |
|---|---|
| LaTeX → DVI | `.eps`, `.ps` only |
| pdfLaTeX / LaTeX → PDF mode | `.pdf`, `.png`, `.jpg` |

Rules: use `graphics`/`graphicx` + `\includegraphics`; never mix PostScript-only and PDF-only figures
in the same document; do not rely on arXiv's own format auto-conversion — convert and visually verify
figures yourself before upload; avoid embedding JavaScript/animated content in figure PDFs (flagged
as a security concern). Filenames are case-sensitive on arXiv's Linux servers (`Fig1.PDF` ≠
`fig1.pdf`) — a common silent-failure source if authored partly on Windows.

- Source: same as 1.2/1.4.

### 1.6 Bibliography / BibTeX expectations

Covered in 1.4. Practical implication for us: **compile `references.bib` to a `.bbl` locally and
ship both**, so arXiv never has to invoke BibTeX/Biber itself — this sidesteps the TeX-Live-version
matching risk entirely and is the safer default for a first submission.

### 1.7 Submission size / file restrictions

- Hard cap: **50MB per submission** (in effect since July 2020; no official page found stating a
  more recent change, and nothing in 2026 search results contradicts it — treat as current but
  reconfirm at actual submission time via the live submission form, which enforces it directly).
- No stated per-file-type limit beyond the aggregate cap; guidance is to keep figures efficiently
  encoded (vector PDF for plots, not embedded raster where avoidable) and strip anything unused.
- This paper has no large binary assets (no video, no huge datasets bundled with the manuscript
  source) so 50MB is not expected to be a binding constraint — flagged only so figure export settings
  don't accidentally produce bloated rasters.

### 1.8 Compilation constraints relevant to LaTeX

- `ifpdf` for conditional branching if needed; do **not** hand-force `\pdfoutput=1/0` or hard-code
  `graphics`/`hyperref` driver options — let them auto-detect, since arXiv's own compilation
  environment sets the mode.
- `xr` (external document cross-references) is **unsupported** — multi-file submissions get
  concatenated/relocated on arXiv's servers, breaking `xr`'s relative paths; use `subfiles` instead
  if a multi-document structure is ever needed (not expected here — this is a single-paper
  submission).
- Escape literal `#` in URLs (`\string#` or a custom macro) to avoid PDF hyperlink corruption.
- Only packages present in arXiv's TeX Live distribution (or bundled by the author) are available —
  no custom publisher stylesheets beyond that collection; the deprecated `psfig` is explicitly listed
  as unsupported.
- Source: [Considerations for TeX Submissions](https://export.arxiv.org/help/submit_tex) — accessed
  2026-08-12.

### 1.9 HTML-generation considerations

- Since Dec 2023, arXiv auto-generates an **HTML version of every new TeX/LaTeX submission** via
  LaTeXML (NIST-maintained), for accessibility. This is now a standard, expected output, not an
  optional add-on.
- LaTeXML has explicit support for 400+ common packages; using packages/macros outside that set
  degrades HTML fidelity (not compilation — the PDF still compiles fine either way).
- Practical guidance from arXiv's own best-practices page: prefer semantic macros
  (`\emph`, `\section{}`) over manual visual formatting (`{\it ...}`, hand-rolled heading sizes);
  supply `\includegraphics[alt={...}]` alt text for figures; use standard `\title`/`\author`/
  `abstract` front matter rather than a custom title block.
- As of the most recent arXiv accessibility update found (referenced in a 2026 arXiv paper on HTML
  conversion), corpus-wide HTML conversion is at roughly 75% error-free with an internal 90% target —
  i.e., this is an actively improving but not yet perfect pipeline; expect to check our own paper's
  HTML rendering after submission rather than assume perfection.
- Sources: [HTML as an accessible format](https://info.arxiv.org/about/accessible_HTML.html),
  [LaTeX Markup Best Practices for HTML](https://info.arxiv.org/help/submit_latex_best_practices.html)
  — accessed 2026-08-12.

### 1.10 Licensing options and implications

Available at submission time (author's choice; arXiv's own perpetual non-exclusive distribution
license is applied regardless of which of these is also chosen):

- **arXiv perpetual, non-exclusive license only** (the historical default — grants arXiv the right
  to distribute; does *not* grant the public further reuse rights beyond fair use).
- **CC BY** (attribution only — maximally reusable).
- **CC BY-SA**, **CC BY-NC-SA**, **CC BY-NC-ND** (varying reuse restrictions).
- **CC0** (public-domain dedication — only option where the author gives up copyright itself; all
  others retain author copyright).
- Implication for later journal submission: **choosing a CC license now does not by itself block a
  future journal submission** — most CS/ML venues (and arXiv-friendly journals generally) permit a
  prior arXiv preprint under CC BY or the arXiv default license. What can complicate things is
  choosing **CC BY-ND / CC BY-NC-ND-style restrictions combined with a venue that requires the
  publisher hold exclusive rights** — worth checking the target journal's policy at that later stage,
  not now. Given this paper's plan (arXiv now, journal decision later, per `ROADMAP.md` Phase I), the
  safest default is **CC BY** (maximizes reuse/citation visibility, no known conflict with typical
  ML-venue preprint policies) unless a specific target journal is chosen first and requires otherwise.
- **LOCKED (E7.8.2, 2026-08-18): CC BY 4.0** selected as the arXiv distribution license.
- Source: [Licenses](https://info.arxiv.org/help/license/index.html) — accessed 2026-08-12.

### 1.11 Category/subject-class considerations for this paper

- Primary candidate: **cs.LG** (Machine Learning) — covers architecture/method papers about
  classification-system design broadly, not just model training.
- Cross-list candidates: **cs.AI** (system-design framing fits; excludes vision/robotics/NLP as
  primary but is a reasonable cross-list), **cs.CL** only if the OCR/text-classification angle is
  emphasized (it is not central to the locked contribution — see `CONTRIBUTION_LOCK.md`, which scopes
  the evidence to a synthetic product-classification generator, not NLP), **cs.SE** is also plausible
  given the "workflow/architecture decision procedure" framing STATE.md already uses ("design-time
  workflow composition").
- **Recommendation: primary cs.LG, cross-list cs.AI.** Do not cross-list cs.CL/cs.CV — the locked
  contribution (§6 of `CONTRIBUTION_LOCK.md`) is about mechanism selection given a consistency
  signal, not about document understanding/OCR, and over-broad cross-listing invites moderation
  friction (a category mismatch is one of the explicit "held for reclassification" triggers, §1.13).
- Source: [arXiv category taxonomy](https://arxiv.org/category_taxonomy) — accessed 2026-08-12.
- **LOCKED (E7.8.2, 2026-08-18): primary cs.LG, cross-list cs.AI.**

### 1.12 Authorship, ORCID, acknowledgements, conflicts

- Full real author names required (no "et al.", no anonymous submissions, no honorifics).
- Affiliations (if any) go in parentheses, city/country only — no street address.
- **Generative-AI tools must never be listed as an author**; if genAI was used substantively in
  drafting, this must be disclosed (per moderation policy, §1.13) — relevant here since this
  manuscript will be drafted with heavy Claude Code assistance. Disclosure language should go in the
  Acknowledgements or a Comments-field note, not in the Authors field.
- Special roles ("editor", "appendix author") belong in the Comments field, not the Authors field.
- ORCID: arXiv's submission form supports attaching an ORCID iD to an author record; STATE.md already
  records an ORCID-linked `CITATION.cff` — reuse the same ORCID iD for consistency across
  Zenodo/GitHub/arXiv (matches the existing "Google Scholar indexing" goal in `STATE.md`/`ROADMAP.md`
  Phase I).
- No official-doc mention of a required "conflicts of interest" field for arXiv itself (unlike a
  journal) — COI statements are a *journal-submission* concept, not an arXiv one; defer that to the
  eventual journal-migration step per `ROADMAP.md`.
- Source: fetched preparation-guidance page content (URL returned 200 but the specific canonical path
  could not be double-confirmed against a second independent official page in this pass — treat the
  authorship/ORCID rules above as **medium-confidence**, re-verify against the live submission form's
  own field help text at actual submission time, which is authoritative regardless).

### 1.13 What could cause rejection or a hold

From arXiv's official moderation policy
([Moderation](https://info.arxiv.org/help/moderation/index.html), accessed 2026-08-12):

- Category mismatch → reclassification hold (see §1.11's recommendation to keep categories tight).
- Missing scholarly-writing standards (informal tone, missing sections/references/figures prepared
  to professional norms).
- Perceived lack of "scholarly interest" — arXiv moderators can decline course-project-style or
  insufficiently substantive work; a single-experiment paper with a narrow, honestly-scoped negative
  finding (this paper's actual shape, per `CONTRIBUTION_LOCK.md` §6) is legitimate but should be
  written to read as a complete, self-contained scientific contribution, not as an internship report
  or a case study writeup — this is a real risk given the project's own engineering-heavy origin
  story, and is exactly why Task 3 (below) puts the case study in a motivating/context role rather
  than as the paper's spine.
- Falsified data, plagiarism, serious misrepresentation → rejection, not merely a hold.
- **Undisclosed substantial generative-AI authorship of the text** → policy violation. This
  manuscript is Claude-Code-assisted; the Acknowledgements/Comments must disclose AI-assistance in
  drafting per current arXiv policy, while the actual authorship (ideas, experiment design, decision
  to lock the contribution) remains human per `CONTRIBUTION_LOCK.md`'s own gate structure.
- Rights issues — must hold legal authority to submit (no client IP conflict here per
  `METHODOLOGY.md`'s confidential/public split, but worth a final explicit check at Phase E6/E7 — see
  `PUBLIC_RELEASE_BOUNDARY.md`).
- Submission-rate throttling (practical cap ~3/day) — irrelevant, this is a single submission.

### 1.14 Endorsement — the practical gate most likely to actually block this submission

Not explicitly asked for in the Phase E prompt's checklist (items 1-13 above), but surfaced during
research and material enough to flag prominently: **arXiv changed its endorsement policy on
2026-01-21**, eliminating "institutional email address alone" as sufficient for automatic
endorsement. The two current paths:

1. **Automatic:** institutional email **and** prior co-authorship on an already-accepted arXiv paper
   in the same category.
2. **Manual (personal endorsement):** an established arXiv author in the same category vouches for
   the submitter directly.

**This project's author has no prior arXiv paper and (per STATE.md's "independent researcher"
framing) no claimed institutional email for this work.** That means path 1 is unavailable and
**personal endorsement (path 2) is required** before the first submission can go through — this is
an action item for Phase E7 (arXiv submission package), not Phase E0, but it has enough lead time
risk (finding and contacting a willing cs.LG/cs.AI endorser) that it should be started well before
the draft is finished, not discovered at submission time.

- Sources: [Endorsement](https://info.arxiv.org/help/endorsement.html),
  [Attention Authors: updated endorsement policy](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/)
  — accessed 2026-08-12.

### 1.15 What should NOT be included in a public arXiv source package

Derived from 1.4 plus this project's own confidentiality posture (`METHODOLOGY.md`,
`PUBLIC_RELEASE_BOUNDARY.md`):

- Any intermediate LaTeX build artifact (`.aux`, `.log`, `.out`, `.synctex.gz`, etc.).
- Any figure source file not actually referenced by the final `.tex` (draft/discarded plot variants).
- Any confidential production data, real company/CUI identifiers, internal AWS resource names (IAM
  usernames, regions), or private-repo file paths — none currently appear in
  `TECHNICAL_REPORT.md`/`METHODOLOGY.md` (verified this pass by direct read; see
  `PUBLIC_RELEASE_BOUNDARY.md` for the full sweep), but this is the check to repeat at Phase E6.
- Reviewer/referee correspondence, internal audit reports (`research/AUDIT_REPORT.md`,
  `CONTRIBUTION_LOCK.md`, etc.) — these are process artifacts for this repository's own research
  governance, not manuscript content; they stay in the GitHub repo (methodologically transparent) but
  do not belong in the arXiv *source* package, which should contain only the paper itself.

---

## 2. Template decision

### 2.1 Options considered

| Option | Verdict |
|---|---|
| A. Generic LaTeX `article` class | **Recommended** |
| B. IEEE template | Rejected for now |
| C. ACM template | Rejected for now |
| D. Springer template | Rejected for now |
| E. Other ML/AI-specific template (e.g. NeurIPS/ICML style files) | Rejected for now |
| F. Markdown → PDF | Rejected |

### 2.2 Reasoning

- **arXiv compatibility:** arXiv does not require or reward any specific template (§1.3). A plain
  `article`-class document compiles cleanly under any TeX Live version arXiv runs, with no dependency
  on a publisher's possibly-outdated or possibly-unsupported `.cls` file (venue templates are
  sometimes *not* on arXiv's TeX Live and would need to be vendored in — extra fragility for zero
  benefit at this stage).
- **Future journal migration:** every one of B-E is a *specific venue's* house style. Adopting one now
  would either (a) need to be re-templated later anyway once an actual target journal is chosen —
  `ROADMAP.md` Phase I explicitly defers venue choice — or (b) implicitly lock the paper's visual
  identity to a venue before Gate 4's contribution lock has even been converted to prose. A generic
  `article` skeleton with clearly separated `sections/` (per Task 8) reformats faster into any target
  template later, because the prose/structure work is decoupled from the `.cls` file.
  `journal-recommender`/`peer-reviewer` skills (available in this environment) are the intended tools
  for the *later* venue-fit decision — not this phase.
  cs.LG/cs.AI conference templates would specifically be premature: this paper is explicitly framed
  as an arXiv preprint first (`STATE.md`, `ROADMAP.md`), not a conference submission with a deadline;
  no page-limit or camera-ready constraint exists yet to design around.
- **Mathematical notation:** `article` + `amsmath`/`amssymb` handles the one equation this paper
  actually needs (the ADS formula, §2.2 of `TECHNICAL_REPORT.md`) with zero friction. This paper is
  not notation-heavy (one metric definition, some accuracy/coverage percentages, a couple of
  correlation coefficients) — no need for a template chosen "for" heavy math.
- **Figures/tables:** `graphicx` + `booktabs` (both in every TeX Live, both LaTeXML-supported per
  §1.9) suffice for the figure/table plan in `PHASE_E_PLAN.md` §7 — nothing venue-specific needed.
- **References:** plain `article` + `natbib` or `biblatex` — either works; recommend `biblatex`
  with the `numeric` or `authoryear` style **only if** its bbl-version compatibility is verified
  against arXiv's current TeX Live at actual compile time (§1.4); `natbib`+BibTeX is the more
  conservative, lower-risk default for a first arXiv submission and is recommended here specifically
  to avoid the Biber/BibTeX bbl-mismatch failure mode documented in §1.4.
- **Reproducibility:** a plain-text `.tex` tree with a committed `references.bib` is maximally
  reproducible and diffable — no proprietary or binary intermediate format.
- **Version control:** `article`-class LaTeX is plain text, diffs cleanly in git, no merge-conflict-
  prone binary artifacts (unlike, e.g., a Word `.docx`).
- **Ease of collaboration with Claude Code:** plain-text `.tex` files are directly readable/editable
  by Claude Code with no special tooling; a heavier template with custom macro files or a build system
  (e.g., some publisher templates ship LuaLaTeX-only macros) adds friction for no current benefit.
- **Avoiding premature venue lock-in:** this is the deciding factor per the prompt's own instruction
  ("do not select a journal-specific template unless evidence strongly justifies doing so") — no such
  evidence exists yet; venue choice is explicitly Phase I / post-preprint per `ROADMAP.md`.
- **Why not Markdown → PDF (Option F):** arXiv's preferred and best-supported path is native
  LaTeX source (§1.1-1.2); a Markdown→PDF pipeline (via Pandoc or similar) would either (a) submit a
  bare PDF, which arXiv accepts but treats as a lesser-tier submission with no HTML generation benefit
  (§1.9 HTML generation depends on LaTeX/TeX source, not PDF) and no direct camera-ready path to a
  future LaTeX-only journal template, or (b) generate LaTeX as an intermediate step anyway, at which
  point authoring in LaTeX directly is simpler and avoids Pandoc-generated LaTeX's often poor
  HTML-conversion fidelity (§1.9's package-support caveat applies doubly to machine-generated LaTeX
  using non-standard macros).

### 2.3 Recommendation

**Option A — generic LaTeX `article` class, engine pdfLaTeX, bibliography via `natbib` + BibTeX,
`.bbl` precompiled and shipped alongside `.bib`.** Revisit only if/when a specific target journal is
chosen post-arXiv (Phase I of `ROADMAP.md`), at which point migrating prose into that journal's
`.cls` is a mechanical, low-risk step precisely because the underlying content was never coupled to a
venue-specific format in the first place.

---

## 3. Open items for the human author (not decidable by this research pass)

1. **Endorsement (§1.14).** Identify and contact a candidate arXiv endorser in cs.LG/cs.AI. This has
   external lead time and should start early, not at Phase E7.
2. **License choice (§1.10). RESOLVED (E7.8.2, 2026-08-18) — CC BY 4.0 locked.**
3. **AI-assistance disclosure wording (§1.12, §1.13).** The exact Acknowledgements/Comments-field
   sentence disclosing Claude-Code-assisted drafting needs author sign-off before Phase E7 — this
   research pass identifies the requirement, not the wording.
4. **Category/cross-list (§1.11). RESOLVED (E7.8.2, 2026-08-18) — primary cs.LG, cross-list cs.AI
   locked.**
