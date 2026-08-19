# ROADMAP — TECHNICAL_REPORT.md → arXiv preprint (HISTORICAL)

> **HISTORICAL / SUPERSEDED.** This was the original Phase A–I execution plan for turning
> `TECHNICAL_REPORT.md` / the Experiment 1 manuscript into a submittable preprint, drafted
> 2026-08-11. The manuscript work that actually happened used a different phase-numbering scheme
> (E0 through E7.9, tracked in `research/RESEARCH_GPS.md` and the dated `research/E*` audit
> reports) and has since reached a finalized release candidate at commit `464aa1b` — see
> `STATE.md` for current status. The checkboxes and "Status" line below are kept as a historical
> record of the original plan and should **not** be read as current; most of what they describe
> was completed under the E-phase sequence instead. The lone item genuinely still open — arXiv
> submission itself — is tracked in `STATE.md`'s "Next" section, not here.

## Why a Research Audit comes first

A `/grill-me` session (see STATE.md's "Literature review + paper-positioning conclusions") surfaced
that the project conflates three distinct things: what was built (code), what was observed
(production + synthetic results), and what is claimed (the research contribution). Before rewriting
any prose, those need to be separated and checked against each other — otherwise the rewrite just
launders the same unverified claims into better-sounding sentences.

```
Existing ADS-Cascade Engineering Evidence
                 │
                 ▼
Phase A — Research Audit          (claims ↔ evidence ↔ code)
                 │
                 ▼
Phase B — Literature Verification (citation ledger, not just references.bib)
                 │
                 ▼
Phase C — Contribution Positioning (what actually survives?)
                 │
                 ▼
Phase D — Minimal Reproducible Validation (synthetic robustness across determinism bands)
                 │
                 ▼
Phase E — Manuscript Rewrite
                 │
                 ▼
Phase F — Figures
                 │
                 ▼
Phase G — LaTeX
                 │
                 ▼
Phase H — Reproducibility + Claim Audit
                 │
                 ▼
Phase I — arXiv submission
```

## Phase A — Research Audit

**Status (2026-08-10): substantially complete.** Two audit passes ran — see
`research/RESEARCH_AUDIT.md` (sections A-F), `research/mapping_count_provenance.md`,
`research/determinism_provenance.md`, `research/r3_threshold_analysis.md`, and
`research/EVIDENCE_BASELINE.md` for the canonical-values output. Two items below could not be
fully closed by audit alone and are recorded as pending author decisions rather than left as
open checklist items indefinitely.

- [x] Build the **Claim–Evidence Matrix**: every claim the report makes, mapped to
      evidence / source / reproducible? / confidence / paper section. Columns:
      `Claim | Evidence | Source | Reproducible? | Confidence | Paper section`.
      Saved as `research/claim_evidence_matrix.csv` (not `research/claims/...` as originally
      sketched here — no subdirectory was needed for one file).
- [x] **Company-count discrepancy — resolved, not a bug.** 169 vs. 201 is not a contradiction:
      `TECHNICAL_REPORT.md` §2.1 already states both correctly ("201 inventoried companies (169
      with usable invoice data)"), matching `data_verification_audit.md` row 14.
- [x] / [ ] **Mapping-count discrepancy (76,843 vs. ~55,394) — investigated, partially resolved.**
      76,843 is confirmed canonical: its provenance traces exactly to
      `reports/phase1_final_report.md` §6 and is consistent everywhere it's cited. ~55,394 is
      marked **UNRESOLVED** — a complete provenance search (current tree, full git history
      including deleted files and a dangling pre-amend commit, commit messages, tags/branches)
      found it nowhere in this repository. See `research/mapping_count_provenance.md` for the full
      search log. **Pending author decision:** check the private client repo or session notes for
      the source, or approve dropping the "~55,394" framing from this document (Question F1 in
      `research/RESEARCH_AUDIT.md`).
- [x] **Architecture docs tracking status — resolved, was a false claim.** All 17
      `architecture/` docs have been tracked in git since the initial commit (`81fb74e`,
      2026-07-28); `git status` shows no pending changes to that directory. STATE.md's "written
      but untracked in git" note was stale and has been corrected. No privacy review was needed —
      these files have been public since the repository's first commit.
- [ ] Cross-check every other headline number in `TECHNICAL_REPORT.md` against
      `data_verification_audit.md`'s "Authoritative Value" column (existing numbers-discipline
      rule in STATE.md — apply it as an audit pass, not just a writing-time rule). Partially
      covered by `research/claim_evidence_matrix.csv`; not yet a row-by-row exhaustive pass
      against every line of `data_verification_audit.md`.

**New item surfaced during Phase A, fixed 2026-08-11:** a real computational bug was found
in `scripts/03_5_dataset_intelligence.py` (`product_ambiguity.csv`'s dominant-account selection
didn't merge same-account rows before comparing — see `research/determinism_provenance.md` Step
3). It did not change any of the five architecture decisions (R1/R3/R4/R5 all confirmed robust to
it, by direct re-run), but it did understate the weighted/unweighted ADS figures. **Fixed**:
regression test written first (`scripts/test_dataset_intelligence.py`), aggregation corrected,
pipeline re-run — new canonical synthetic values: weighted ADS 0.9031, unweighted ADS 0.9597,
deterministic-share 87.56% (previously 0.8094/0.9310/84.12%, now `SUPERSEDED — DO NOT CITE`). See
`research/a5_correction_analysis.md` and `research/EVIDENCE_BASELINE.md`. **Remaining sub-item**:
`TECHNICAL_REPORT.md` §3.2/§3.3 still cite the pre-fix numbers — updating them is manuscript work,
deferred to Phase E (not done here, per this pass's scope).

## Phase B — Literature Verification

Exploration is done (10 standard-depth + 5 gap-driven searches, ~28 candidate citations — see
STATE.md). Verification is not: every citation must graduate from "interesting paper found" to a
checked bibliographic record with an explicit relation to ADS-Cascade.

- [ ] Build the **Citation Ledger** at `research/literature/citation_ledger.csv`:
      `ID | Paper | Year | Venue | DOI | Area | Relevance | Relation to ADS | Verified`.
- [ ] Verify each entry's real metadata (title/authors/year/venue/DOI) against the actual paper
      page — Consensus abstracts are leads, not bibliographic records.
- [ ] For each entry, write one line on what it does *not* cover, so the Related Work section can
      state boundaries precisely instead of vaguely.
- [ ] Once verified, compile `research/literature/references.bib` from the ledger (ledger is the
      source of truth; `.bib` is a derived export for LaTeX).
- [ ] Known lineage to place correctly (already confirmed relevant, not yet ledger-verified):
      Rice 1976 (Algorithm Selection Problem, foundational) → Smith-Miles 2009 (meta-learning
      survey) → Barbudo et al. 2023 (AutoML review, ASP "superseded by workflow composition") →
      Idreos et al. 2019 (self-designed/learned data systems, closest non-ML analog) →
      Hendrickx et al. 2021 / Franc et al. 2021 / Vernon et al. 2022 (reject-option / two-stage
      classifiers, closest ML analog, inference-time not design-time).

## Phase C — Contribution Positioning

- [ ] Answer explicitly, in writing: what is already known (per the ledger), what does
      ADS-Cascade actually do, what survives as a contribution once the neighboring literature is
      assumed to exist, what can legitimately be claimed.
- [ ] Lock the framing: *"ADS-Cascade is an evidence-driven design procedure that operationalizes
      historical decision consistency as a meta-feature for composing heterogeneous decision
      mechanisms — building on established ideas in algorithm selection, meta-learning, workflow
      composition, adaptive computation, selective prediction, and human deferral."* Novelty
      question becomes: what specific combination, operationalization, and empirical demonstration
      does this add, not "is this unprecedented."
- [ ] Draft `research/RESEARCH_PROTOCOL.md` — the constraints governing what the manuscript is and
      isn't allowed to claim. Contents: Research Question, Core Preconditions (repeated historical
      decisions / observable labels / measurable consistency / sufficient historical coverage),
      Evidence Hierarchy (public reproducible synthetic > public code/artifacts > confidential
      production case study > qualitative observations), Claim Rules (never claim universal
      applicability; never claim metric novelty without evidence; never present confidential
      production results as independently reproducible; distinguish observation/proposal/
      hypothesis; report negative/boundary results; every quantitative claim traces to an
      artifact), Research Scope (in: historically supervised classification, hybrid AI
      architecture composition, design-time decision procedures — out: open-ended generation,
      general reasoning, planning, creative tasks, negotiation, exploratory analysis),
      Reproducibility (all public experiments run without client data).

## Phase D — Minimal Reproducible Validation

- [ ] Synthetic robustness sweep across determinism bands (high / medium / low), not just the
      single synthetic run already reported — check whether the R3-style boundary sensitivity
      shows up elsewhere or was a one-off at the current synthetic scale.
- [ ] Cross-company consistency and decision-stability checks on synthetic data, same spirit.
- [ ] Only add experiments that use the existing synthetic generator/pipeline — no new real data,
      no new external dependencies.

## Phase E — Manuscript Rewrite

Every claim below must trace to a row in the Phase A Claim–Evidence Matrix before it's written.

- [ ] **Abstract + §1 Introduction:** question-first pitch scoped to actual evidence (not
      "enterprise AI" broadly). State the four preconditions explicitly; name what's out of scope.
- [ ] **§3 Evaluation:** synthetic pipeline as primary/reproducible evidence; production numbers as
      illustrative case study, not proof. Keep the R3 flip discussion, add Phase D results.
- [ ] **§5 Related work:** rewrite from the verified Citation Ledger. Structure: algorithm-selection/
      meta-learning lineage → closest non-ML analog (self-tuning DBs) → closest ML analog
      (reject-option/two-stage classifiers, design-time vs. inference-time distinction) → direct
      application competitors (invoice/GL-classification systems, commercial vendors) → positioning
      statement.
- [ ] **§4 Limitations:** re-check against the narrower pitch for consistency.
- [ ] Full read-through checking every claim against the matrix — flag anything unsupported.

## Phase F — Figures

No new experiments beyond Phase D — reads from committed CSVs (`data/outputs/phase2/*.csv`, Phase 1
outputs) plus whatever Phase D adds.

- [ ] ADS distribution (unweighted vs. weighted, production).
- [ ] Tier coverage/accuracy chart (Tier-1 98.4%@42% → full cascade 98.1%@42.8%).
- [ ] Production-vs-synthetic comparison, highlighting the R3 flip.
- [ ] R1–R5 decision-procedure diagram.
- [ ] Phase D robustness-sweep chart (determinism band vs. decision stability), if Phase D ships.
- [ ] One matplotlib script generating all figures into `research/figures/`, committed alongside
      the data it reads.

## Phase G — LaTeX

- [ ] Plain `article` class skeleton (arXiv doesn't require a house template).
- [ ] Migrate rewritten prose section by section; wire `references.bib` via `\cite{}`.
- [ ] Insert Phase F figures.

## Phase H — Reproducibility + Claim Audit

- [ ] Re-run the Claim–Evidence Matrix against the final LaTeX text — every claim in the PDF must
      still map to a matrix row.
- [ ] Confirm every public experiment runs offline with no client data (existing repo convention).
- [ ] Full proofread pass.

## Phase I — arXiv submission

- [ ] Pick arXiv category **after** Phase C positioning is locked (likely cs.LG / cs.SE / cs.AI —
      don't decide early and reverse-engineer the paper to fit it).
- [ ] Submit; confirm Google Scholar indexing once live (may take days).
- [ ] Cross-link Zenodo record, GitHub README, ORCID profile to the arXiv identifier.

## Track A wrap-up (from STATE.md, unblocked by Phase I)

- [ ] Polish GitHub repo presentation.
- [ ] Confirm Zenodo DOI + ORCID prominence.
- [ ] Draft EDISS EMJM CV entry (~150 words) + video talking points, once the arXiv link exists to
      cite as evidence.

---

**Directory layout this plan assumes** (create incrementally, only as each phase actually needs
the folder — don't scaffold ahead of use):

```
research/
├── RESEARCH_PROTOCOL.md          # Phase C
├── claims/
│   └── claim_evidence_matrix.csv # Phase A
├── literature/
│   ├── citation_ledger.csv       # Phase B
│   └── references.bib            # Phase B (derived from ledger)
├── experiments/                  # Phase D
├── figures/                      # Phase F
└── manuscript/
    └── outline.md                # Phase E, optional
```
