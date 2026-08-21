# E5.2 — Citation + Claim Audit

> Verification pass, not a new literature-research phase. Cross-checks every citation and every
> literature-facing claim in `manuscript/main.tex` (post-E5.1, 43 subsections) against the already-
> verified Phase B/C evidence base (`citation_ledger.csv`, `ads_metric_prior_art.{md,csv}`,
> `llm_advisory_prior_art.{md,csv}`, `prior_art_map.md`, `terminology_map.md`,
> `contribution_status.md`) and the locked contract (`PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`,
> `contribution_lock.csv`, `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`). No new source was searched. No
> manuscript edit was made by this pass. `git status` is unchanged except for this new file.

---

## Part 1 — Citation inventory

All `\citep{}`/`\citet{}` keys in `manuscript/main.tex`, grepped exhaustively (`\\cite[pt]\{[^}]+\}`).
14 distinct keys, 17 in-text occurrences (one key, `dawidskene1979`, appears twice; `rice1976`,
`smithmiles2009`, `barbudo2023` each appear twice, once individually in §1.2/§2.2 and once together
in §6.5).

| Key | Manuscript location(s) | Ledger source | Ledger status | What the source actually supports | Verdict |
|---|---|---|---|---|---|
| `rice1976` | §1.2 (L146), §2.2 (L288), §6.5 (L1216) | B1-01 | VERIFIED | Originates the Algorithm Selection Problem; per-instance, single-algorithm selection, no determinism metric | FULLY_SUPPORTED |
| `smithmiles2009` | §1.2 (L147), §2.2 (L290), §6.5 (L1216) | B2-01 | VERIFIED | Foundational unification of meta-learning with Rice 1976 | FULLY_SUPPORTED |
| `barbudo2023` | §1.2 (L148), §2.2 (L306), §6.5 (L1216) | B2-02 | VERIFIED | Documents the field's shift from single-algorithm selection to automated workflow composition (verbatim-quote-verified) | FULLY_SUPPORTED — manuscript phrasing echoes the ledger's own verbatim quote |
| `manning2008` | §2.1 (L268), §3.2 (L475) | G1-01 (`ads_metric_prior_art.csv`) | VERIFIED | Cluster purity, Ch. 16.3 — identical closed-form expression to ADS | FULLY_SUPPORTED |
| `amigo2009` | §2.1 (L268), §3.2 (L475) | G1-02 | VERIFIED | Formal axiomatic treatment of purity, same formula | FULLY_SUPPORTED |
| `dawidskene1979` | §2.1 (L274), §3.2 (L477) | G1-04 | VERIFIED (metadata incomplete — see Part 7) | Raw majority-vote-agreement proportion is the standard naive baseline in the descendant literature; mathematically identical to ADS | FULLY_SUPPORTED |
| `idreoskraska2019` | §2.2 (L323) | B7-01 | VERIFIED | Strongest non-ML structural analog; workload-frequency evidence, continuous self-adaptation (opposite temporal structure) | FULLY_SUPPORTED |
| `chow1970` | §2.3 (L343) | B4-01 | VERIFIED | Originates single-threshold accept/reject on live posterior confidence | FULLY_SUPPORTED |
| `elyaniv2010` | §2.3 (L344) | B4-02 | VERIFIED | Formalizes risk-coverage tradeoffs | FULLY_SUPPORTED |
| `hendrickx2024` | §2.3 (L346) | B4-05 | VERIFIED | Most comprehensive recent reject-option survey (72 citations) — manuscript's "surveyed comprehensively" echoes ledger's own description | FULLY_SUPPORTED |
| `mozannarsontag2020` | §2.3 (L358) | B5-02 | VERIFIED | Establishes the modern learning-to-defer framework the sub-literature builds on | FULLY_SUPPORTED |
| `frugalgpt2023` | §2.3 (L372) | B3-02 | VERIFIED | Closest structural match to a historically-calibrated multi-tier cascade | FULLY_SUPPORTED |
| `rankgpt2023` | §2.3 (L374) | G2-01 (`llm_advisory_prior_art.csv`) | VERIFIED (author list abbreviated — see Part 7) | LLM-reranks-a-pre-fetched-list is commodity IR technique since 2023 | FULLY_SUPPORTED — manuscript's "commodity information-retrieval technique" is drawn directly from the ledger's own wording |
| `jorgensenigel2021` | §2.4 (L389) | B8-01 | VERIFIED | Empirically demonstrates the same cross-company generalization gap in the same domain | FULLY_SUPPORTED |

**No UNUSED entries**: `references.bib` contains exactly these 14 entries and no others; every entry is
cited at least once (independently cross-checked, see Part 7).

**No MISATTRIBUTED or OVERSTATED entries found.** Every citation's claim strength matches its
ledger-recorded status, including two cases (`barbudo2023`, `rankgpt2023`) where the manuscript's
prose reuses phrasing the ledger/`prior_art_map.md` itself already vetted as accurate — not
independently paraphrased in a way that could drift from the source.

**Three sources used substantively in prose but never formally cited** — see Part 6 (this is the
audit's most actionable finding).

---

## Part 2 — Claim-strength audit

Grepped the full manuscript for every trigger word in the brief
(`establishes|introduced|demonstrates|shows|proves|closest|first|novel|under-explored|widely|
generally|established|state-of-the-art|conventional|commodity|since|pioneered|formalized`) and
checked each substantive hit against its cited source.

**Clean matches (claim strength = source strength), verified individually:**

| Manuscript text | Verb used | Source | Verdict |
|---|---|---|---|
| "the Algorithm Selection Problem... has an established name" | established | B1-01 | Accurate — Rice 1976 is the field's own acknowledged root term |
| "\citet{mozannarsontag2020} establishes the modern learning-to-defer framework" | establishes | B5-02 | Matches ledger verbatim: "Establishes the theoretically-grounded... framework" |
| "RankGPT... establishes that... is commodity information-retrieval technique" | establishes / commodity | G2-01 | Matches `llm_advisory_prior_art.md`: "commodity technique in information retrieval since 2023" |
| "\citet{jorgensenigel2021} empirically demonstrates... that a global classifier generalizes far worse" | demonstrates | B8-01 | Matches ledger: "Empirically demonstrates the EXACT phenomenon" |
| "\citet{barbudo2023} documents the field's shift... describing the field as having moved from the algorithm selection problem toward... composing an entire processing workflow" | documents | B2-02 | Matches the ledger's own verbatim-verified quote |
| "\citet{idreoskraska2019} describes the strongest non-machine-learning structural analog" | describes / strongest | B7-01, `prior_art_map.md` | The "strongest... analog" characterization is the *ledger's own* assessment, correctly attributed as positioning, not claimed as the cited paper's self-description |
| "formalized further by \citet{elyaniv2010}'s risk-coverage framework" | formalized | B4-02 | Matches ledger: "Formalizes risk-coverage tradeoffs... with theoretical guarantees" |
| "surveyed comprehensively by \citet{hendrickx2024}" | comprehensively | B4-05 | Matches ledger: "Comprehensive 2024 survey (72 citations, most recent found)" |
| "This paper operates at the architecture/workflow level those literatures describe the field moving toward, not at the per-instance level Rice originally posed" | — | `terminology_map.md` | Near-verbatim reuse of that document's own recommended framing sentence |
| "cluster purity... is defined as... the identical closed-form expression as ADS" | — | `ads_metric_prior_art.md` | Matches the verdict section exactly: "identical closed-form expression" |

**No instance found of**: "proves," "pioneered," "under-explored," "widely" (unqualified), "generally"
(unqualified), "conventional," or "state-of-the-art" applied to any of this paper's own claims. Every
occurrence of "first" and "novel" in the document is either (a) part of an unrelated phrase ("first
tier," "the first is...," ordinal list markers) or (b) a **negated** novelty claim (see Part 3). No
overclaiming trigger word was found attached to an unhedged assertion.

**Verdict: no claim in the manuscript reads stronger than its cited source.** This is consistent with
the pattern already established at E3/E4: every substantive positioning sentence is paired with an
explicit "we do not claim..." / "we make no claim that..." disclaimer (11 such disclaimers counted
across §1–§2 and §6 alone).

---

## Part 3 — Novelty guardrail

**ADS-not-a-novel-metric framing: intact.** Grepped for `novel` (7 hits) — every one is a negation:
"we therefore make no claim that ADS is a novel metric" (§2.1), "this general pattern is well
established" (§1.2, i.e. explicitly *not* new), "not presented as a novel contribution" (§3.2 comment
+ prose), "much weaker than any claim of methodological novelty" (§2.4), "not a new metric... not a
new architecture" (§1.4). No positive novelty assertion for ADS exists anywhere in the document.

**Broad "no prior work" framing: not found, and the specific forbidden pattern is explicitly
pre-empted.** Grepped for `no prior|no previous|no existing work|unprecedented|no comparable|
nothing (measures|anticipat)|has not been (measured|studied|explored)`. One hit, and it is the
*correct*, negated form: §2.4 (L397) reads "We do not claim that the application domain itself is
unprecedented, **or that no vendor measures historical consistency before choosing a mechanism** —
at least one industry source directly contradicts that framing." This is precisely the guardrail the
brief asked for — the exact forbidden sentence pattern ("no previous work measures historical
consistency before selecting an architecture") appears in the manuscript *only* inside its own
negation, with the contradicting evidence (B8-04, though not formally cited — see Part 6) named
alongside it.

**Verdict: PASS. No novelty-language violation found.**

---

## Part 4 — Contribution Lock compliance

Checked each of the seven items the brief specified, directly against `CONTRIBUTION_LOCK.md`:

| Requirement | Manuscript location | Status |
|---|---|---|
| Formulation #2 remains adopted | Abstract, §1.4 (Contribution Statement), §6.1/§6.3 | ✅ 6a/6b wording matches `CONTRIBUTION_LOCK.md` §6 near-verbatim throughout |
| C1 (ADS novelty) remains rejected | §2.1, §3.2 | ✅ "closed question, not an open one" — substance matches REJECTED status; no manuscript text needs to use the literal word |
| C2b remains conditional (unconditional form falsified, narrower form supported) | §1.4, §5 (untouched), §6.3–6.4 | ✅ explicit "unconditional form... falsified... narrower... conditional form... evidence-supported" framing throughout |
| H1 remains PARTIALLY_SUPPORTED | §7.1 (Limitations, now leading — see E5.1) | ✅ literal subsection title and body text |
| Mechanism-level accuracy ≠ mechanism ranking | §3.4, §5.2/§5.3 (untouched), throughout Discussion | ✅ the paper's entire organizing distinction; never collapsed anywhere found |
| Representation stability scoped to the tested synthetic setting | §6.4, §7.2–7.5 | ✅ every mention carries "in this experiment" / "this specific perturbation model and this specific retrieval implementation" qualifiers |
| No universal architecture-selection claim | whole document | ✅ none found; §7.5 explicitly states "no deployment or generalization claim" |

**Verdict: PASS, no drift from Gate 4's locked wording.**

---

## Part 5 — Related Work structure (post-E5.1)

Four subsections, evaluated individually:

| §2.X | Genuinely distinct? | Positioning accurate? | Overclaims novelty? | Further mergeable? |
|---|---|---|---|---|
| 2.1 Cluster Purity and Majority-Vote Agreement | Yes — metric-level (C1) | Yes | No | No — distinct axis (metric construction vs. metric use) |
| 2.2 Design-Time Algorithm and Architecture Selection | Yes — general pattern (C2) | Yes | No | No — see below |
| 2.3 Inference-Time Selection and Escalation | Yes — design-time/runtime boundary | Yes | No | No — see below |
| 2.4 Domain-Specific Practice | Yes — application-domain novelty (C8) | Yes | No | No |

**2.2 vs. 2.3 merge candidate, evaluated and rejected:** both are "positioning" subsections, but 2.2
answers "what is this paper's design-time selector *like*" (C2/C2b) while 2.3 answers "why the
inference-time/runtime literature does *not* apply to Experiment 1 at all" (a scoping argument, not a
literature family). Collapsing them would blur a distinction a reviewer specifically benefits from —
recommend keeping separate.

**Repetition between Related Work and Discussion, checked specifically:**
- §3.2 (Problem Setting) repeats the cluster-purity/majority-vote equivalence and cross-references
  §2.1 by number rather than re-arguing it — this is **required, not redundant**: `PAPER_CONTRACT.md`
  §2 row 1 mandates the equivalence be restated "wherever [ADS is] introduced."
- §6.5 (Discussion) re-cites `rice1976,smithmiles2009,barbudo2023` (same three keys as §2.2) but for a
  different, later-stage argument — that the *finding* refines rather than contradicts that lineage,
  a claim that can only be made after Results, and one `PAPER_CONTRACT.md` §2 row 8 explicitly
  requires in this near-exact wording. **Intentional, contract-mandated reuse, not accidental
  repetition.**

**Verdict: Related Work structure is clean post-E5.1. No further merge recommended; the two
apparent-repetition instances are both explicitly required by the paper contract, not drafting
drift.**

---

## Part 6 — Citation completeness

**Finding GAP-01 (the most actionable finding in this audit):** three VERIFIED-INDUSTRY ledger
sources are used substantively in manuscript prose but never formally cited.

- §2.4 (L394–396): *"Independent industry sources (accounts-payable automation vendors, not
  peer-reviewed) describe similar informal historical-consistency-audit practice already in
  production use."*
- §2.4 (L397–399): *"...or that no vendor measures historical consistency before choosing a
  mechanism — at least one industry source directly contradicts that framing..."*

Both sentences are substantiated by the `% EVIDENCE:` comment immediately below (L410: "citation_
ledger.csv rows B8-01, B8-04, B8-05, B8-06") and by `CONTRIBUTION_LOCK.md` §7 / `PAPER_CONTRACT.md`
§3 row 14, which names **B8-04 (Ken From Finance)** specifically as the source that "directly
contradicts" the no-vendor-measures-consistency framing. But **B8-04, B8-05, and B8-06 have no
`\citep{}`/`\citet{}` anywhere in the manuscript and no entry in `references.bib`** — a reader cannot
tell which vendor, or verify the claim, from the text as written. `jorgensenigel2021` (B8-01) *is*
formally cited in the same subsection, making the omission of the three industry sources more visible
by contrast, not less.

- **Required action:** REQUIRED_ACTION — add `references.bib` entries for B8-04/05/06 (all three have
  URLs and VerificationMethod notes in `citation_ledger.csv`, retrieved via WebFetch 2026-08-11 — this
  is a ledger-supported citation-formatting fix, **not** new literature research) and cite at least
  B8-04 by name where the manuscript currently says "at least one industry source." Per
  `PAPER_CONTRACT.md` §2 row 11, each must carry an explicit not-peer-reviewed label at the point of
  citation (the manuscript's existing "(accounts-payable automation vendors, not peer-reviewed)"
  parenthetical already does this in spirit for the group; it would need to travel with the specific
  `\citep{}` once added).
- This is **NOT** "NEW LITERATURE REQUIRED" — all three sources are already VERIFIED-INDUSTRY in
  `citation_ledger.csv`. This is a citation-formatting completeness gap, fixable entirely from
  already-verified sources.

**No other completeness gaps found.** The additional ledger rows named only in `% EVIDENCE:` comments
(B1-02 through B1-05, B2-10, B2-11 — background algorithm-selection surveys) are corroborating
context, not independently invoked by name in visible prose, so their absence from in-text citation is
not a gap in the same sense — the substantive claims they'd support (Algorithm Selection Problem,
meta-learning) are already covered by `rice1976`/`smithmiles2009` in the visible text.

---

## Part 7 — Bibliography integrity

- **Every citation key resolves:** ✅ 14/14 keys in `main.tex` have a matching entry in
  `references.bib` (independently cross-checked, not assumed).
- **Every bibliography entry is used:** ✅ 14/14 entries are cited at least once; no unused entries.
- **No fabricated entry:** ✅ every entry traces to a VERIFIED row in `citation_ledger.csv`,
  `ads_metric_prior_art.csv`, or `llm_advisory_prior_art.csv` — independently spot-checked, not
  trusted from the `.bib` file's own header comment.
- **Two pre-existing, self-documented TODOs, both still open, neither newly introduced by E5.1:**
  1. `dawidskene1979`: `volume`/`number`/`pages`/`doi` all marked TODO. Checked against
     `ads_metric_prior_art.csv` row G1-04 — the ledger itself only records the venue name and a note
     "(2069 citations per Consensus; no DOI independently resolved in this pass)," with no
     volume/issue/pages. **The TODO is correctly left unresolved — the ledger has nothing further to
     give it**, consistent with `PAPER_CONTRACT.md`'s "unresolved metadata remains explicitly
     documented rather than guessed" rule. Not a defect, but still a genuine outstanding gap: a
     targeted bibliographic-metadata lookup (not a literature-novelty search) could close this before
     arXiv submission.
  2. `rankgpt2023`: author field is `{Sun and Yan and Ma and others}`. Checked against
     `llm_advisory_prior_art.csv` row G2-01 — the ledger itself also only records "Sun, Yan, Ma, et
     al." **Same situation: correctly left abbreviated, not guessable from the ledger, but still open.**
- **No stale/guessed metadata found masquerading as resolved.** Both TODOs are honest, both are
  independently confirmed to still be unresolvable from currently-verified sources.

**Verdict: bibliography structurally clean (nothing fabricated, nothing orphaned, nothing silently
guessed). Two metadata TODOs remain genuinely open — flagged, not fixed, per the STOP condition.**

---

## Part 8 — Claim × Evidence × Citation matrix

| ID | Manuscript location | Claim | Claim type | Citation key | Source | Source status | Support verdict | Overclaim risk | Required action |
|---|---|---|---|---|---|---|---|---|---|
| CIT-01 | §1.2, L146–148 | ASP → meta-learning → AutoML lineage summary | Positioning | `rice1976`,`smithmiles2009`,`barbudo2023` | B1-01,B2-01,B2-02 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-02 | §2.1, L263–279 | ADS = cluster purity = majority-vote baseline | Metric-novelty (C1) | `manning2008`,`amigo2009`,`dawidskene1979` | G1-01,G1-02,G1-04 | VERIFIED (2 metadata TODOs, see Part 7) | FULLY_SUPPORTED | None | Resolve DOI/author-list TODOs (BIB-01, BIB-02) |
| CIT-03 | §2.2, L286–300 | Design-time selection is well-established; this paper's narrower delta | Positioning (C2/C2b) | `rice1976`,`smithmiles2009` | B1-01,B2-01 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-04 | §2.2, L306–317 | AutoML workflow composition vs. this paper's threshold rule | Positioning | `barbudo2023` | B2-02 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-05 | §2.2, L323–335 | Self-designed systems: opposite temporal structure | Positioning (contrast) | `idreoskraska2019` | B7-01 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-06 | §2.3, L343–352 | Reject-option/selective-classification lineage; design-time/runtime boundary | Positioning (scope) | `chow1970`,`elyaniv2010`,`hendrickx2024` | B4-01,B4-02,B4-05 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-07 | §2.3, L358–366 | Learning-to-defer framework; same design-time/runtime boundary | Positioning (scope) | `mozannarsontag2020` | B5-02 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-08 | §2.3, L372–381 | FrugalGPT cascade analog; RankGPT reranking-as-commodity | Positioning | `frugalgpt2023`,`rankgpt2023` | B3-02,G2-01 | VERIFIED (author-list TODO on rankgpt2023) | FULLY_SUPPORTED | None | Resolve author-list TODO (BIB-02) |
| CIT-09 | §2.4, L389–393 | Same cross-company generalization gap, same domain | Empirical positioning (C7/C8) | `jorgensenigel2021` | B8-01 | VERIFIED | FULLY_SUPPORTED | None | None |
| CIT-10 | §2.4, L394–402 | Industry vendors already practice informal consistency-audit + cascade patterns; contradicts a "no vendor" framing | Empirical positioning (C8) | *(none — prose only)* | B8-04,B8-05,B8-06 | VERIFIED-INDUSTRY | **MISSING_SUPPORT** | **Medium** — an attentive reviewer can ask "which vendor?" and find no answer in-text | **REQUIRED: add `\citep{}` + `references.bib` entries for B8-04/05/06 (GAP-01)** |
| CIT-11 | §3.2, L475–477 | ADS restated as cluster purity / majority-vote (required repetition) | Metric-novelty (C1) | `manning2008`,`amigo2009`,`dawidskene1979` | G1-01,G1-02,G1-04 | VERIFIED | FULLY_SUPPORTED | None | None (see CIT-02) |
| CIT-12 | §6.5, L1213–1222 | This finding refines, not contradicts, the ASP/meta-learning lineage | Positioning (post-result) | `rice1976`,`smithmiles2009`,`barbudo2023` | B1-01,B2-01,B2-02 | VERIFIED | FULLY_SUPPORTED | None | None — required, intentional reuse of CIT-01's keys (`PAPER_CONTRACT.md` §2 row 8) |
| BIB-01 | `references.bib` L55–67 | `dawidskene1979` volume/number/pages/DOI | Bibliography metadata | — | G1-04 | Ledger has no further data | Correctly-left TODO | Low (honest gap) | Optional: targeted metadata lookup before arXiv submission |
| BIB-02 | `references.bib` L96–103 | `rankgpt2023` full author list | Bibliography metadata | — | G2-01 | Ledger has no further data | Correctly-left TODO | Low (honest gap) | Optional: targeted metadata lookup before arXiv submission |
| NOV-01 | Whole document | ADS-not-novel guardrail | Novelty guardrail | — | — | — | Intact — 7/7 "novel" hits are negations | None | None |
| NOV-02 | §2.4, L397 | "No vendor measures consistency" forbidden framing | Novelty guardrail | — | — | — | Intact — only appears negated | None | Same fix as CIT-10 would also name the contradicting source explicitly |
| LOCK-01 | Whole document | Contribution Lock §2–§9 compliance (7 checks) | Contribution-lock | — | `CONTRIBUTION_LOCK.md` | Adopted, Gate 4 PASS | PASS on all 7 checks | None | None |

---

## Summary of findings (severity-ordered)

1. **[REQUIRED_ACTION, not blocking, bounded]** GAP-01 / CIT-10: three VERIFIED-INDUSTRY sources
   (B8-04 Ken From Finance, B8-05 Peakflo, B8-06 Ramp) are described in manuscript prose but never
   formally cited — no `\citep{}`, no `references.bib` entry. This is the single most
   reviewer-visible citation gap in the document: the manuscript makes a specific, falsifiable claim
   ("at least one industry source directly contradicts that framing") without naming or citing that
   source, even though the ledger already has it fully verified. Fixable entirely from already-
   verified sources — no new search needed.
2. **[OPTIONAL, pre-existing, not introduced by E5.1]** BIB-01/BIB-02: two bibliography metadata
   TODOs (`dawidskene1979` volume/pages/DOI; `rankgpt2023` full author list), both honestly
   documented as unresolved by the ledger itself, both still open. Worth a targeted metadata lookup
   before arXiv submission — not a literature-research task.
3. **No forbidden claims, no novelty-language violations, no contribution-lock drift, no
   overstated/misattributed citations, no unused/fabricated bibliography entries found.**

---

## Final answers to the nine authoritative-source cross-check questions

- Citations audited: **14** (17 in-text occurrences).
- Fully supported: **14 / 14** cited claims (100%).
- Partially supported: **0**.
- Overstated: **0**.
- Missing support (cited claim stronger than source, or source misattributed): **0**.
- Missing citation entirely (claim made, no citation at all — the GAP-01 case): **1** (covering 3
  ledger sources, B8-04/05/06).
- Bibliography issues: **2 pre-existing metadata TODOs** (BIB-01, BIB-02), both honestly documented,
  neither fabricated, neither newly introduced.
- Novelty-language findings: **clean** — ADS-not-novel guardrail intact (7/7 negated), broad
  "no prior work" framing intact (1/1 correctly negated).
- Contribution-lock verification: **PASS on all 7 specified checks.**
