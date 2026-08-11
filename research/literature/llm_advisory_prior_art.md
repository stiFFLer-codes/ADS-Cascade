# Gap-Verification Report — LLM Advisory / Never-Auto-Applied Prior Art

> Targeted follow-up pass (2026-08-11), scoped to close the second highest-priority gap flagged at
> the end of the main Phase B sweep: ADS-Cascade's Tier-3 constraint — "the LLM re-ranks
> already-retrieved candidates only, never classifies from a blank product string, and its output
> is never auto-applied, always routed to human review" — was not the subject of a targeted
> adversarial search in the original pass. Full per-source detail in `llm_advisory_prior_art.csv`.
> This document does not defend the constraint's novelty; it reports what was found.

## ADS-Cascade's exact constraint (restated for reference)

Four sub-constraints, claimed together as one Tier-3 mechanism:
1. LLM is given only a candidate list a rules/fuzzy-matching layer already retrieved.
2. LLM is never given a blank/unconstrained classification prompt.
3. LLM output is never auto-applied — 100% of Tier-3 outputs route to human review.
4. This sits as the lowest-confidence tier of a broader deterministic confidence cascade.

## Search coverage

Consensus, FastTrack Literature Open (`search_papers` + `get_paper`), Scholar Gateway
`semanticSearch`. ~260 records screened; 16 sources retained (`llm_advisory_prior_art.csv`).
Representative queries: "Is ChatGPT Good at Search Investigating Large Language Models as
Re-Ranking Agents," "AI advisory system human final decision content moderation flag review,"
"GDPR Article 22 automated decision-making human in the loop meaningful human involvement,"
"learning to defer prediction human expert," plus direct DOI verification on every retained source.

## What was found, broken down by sub-constraint

### Sub-constraint 1–2 (candidates-only, never blank-slate): extremely well-established

**LLM-as-reranker is commodity technique in information retrieval since 2023.** Sun et al.
(2023, EMNLP, "RankGPT," DOI `10.18653/v1/2023.emnlp-main.923`, 590 citations) established the
now-standard pattern: an LLM is given a query plus a fixed candidate list a first-stage retriever
already produced, and only reorders that list — never generating or selecting candidates outside
the supplied set. This spawned a large, directly-descended sub-literature independently confirmed
in this search: Ma et al. 2023 (LRL, zero-shot listwise reranking), Qin et al. 2024 (pairwise
ranking prompting, ACL Findings), Ma et al. 2024 (RankLLaMA, SIGIR), plus RankZephyr, RankVicuna,
FIRST, ListT5, PE-Rank, and REARANK identified as adjacent variants. Anyone reviewing ADS-Cascade's
Tier-3 mechanism against the IR literature would correctly say this half of the constraint is
exactly how LLM reranking is normally done by 2023 — not a novel restriction.

**Important asymmetry:** none of these IR-reranking papers pair the constraint with a human-review
requirement — their reranked output is auto-applied directly as the system's final answer. The
"candidates-only" half and the "human-gated" half of ADS-Cascade's constraint are precedented
*separately*, not *together*, anywhere in this stream.

### Sub-constraint 3–4 (never auto-applied, always human-routed): well-established as a general principle, diffusely sourced

This is not attributable to one paper — it is the organizing idea of several independent, mature
literatures:

- **Automation-bias / human-factors research**, two decades old: Cummings (2004) already names and
  studies exactly "the automation only makes recommendations and the operator has the final say" in
  aviation/military contexts (393 citations).
- **Clinical decision support**: Khera, Butte et al. (2023, JAMA, 160 citations) document
  "AI-advises, clinician-decides" as standard, heavily-studied practice in one of the most
  safety-conscious deployed-AI domains.
- **Learning to defer (L2D)**: Mozannar & Sontag (2020) and its large descendant literature
  (Keswani et al. 2021, Strong et al. 2025's LLM-specific "guided deferral" system, Lykouris & Weng
  2024's content-moderation pipeline) formalize confidence-gated human handoff as a named academic
  field.
- **Explicit authority taxonomies**: Hu et al. 2025 ("AI Supports Human Decisions" mode, co-authored
  by a lead L2D author) and Singh & Szajnfarber 2025 (formal "human approver"/"human selector"
  architecture taxonomy, published specifically because the field lacked settled terminology for
  these configurations) both name general versions of "AI proposes, human always decides."
- **Content moderation**: Lai et al. 2022 ("conditional delegation") studies exactly which output
  regions an AI may act on alone versus must route to a human as a first-class design variable.
- **Regulatory/legal**: GDPR Article 22's statutory "right to obtain human intervention" has
  generated its own academic literature (Wagner 2019's "quasi-automation" critique of token human
  sign-off; Malgieri 2019's survey of EU member-state implementations) — confirming a regulatory
  driver exists, though this is legal/policy scholarship, not a systems paper describing an
  LLM-reranker pattern.

### The full four-part combination: not found assembled anywhere

No single retrieved paper combines all four sub-constraints simultaneously. The closest
single-paper matches each capture roughly two of the four:

- **Strong, Men & Noble (2025)** — LLM + classification + confidence-triggered human deferral —
  but its LLM classifies directly rather than reranking a rules-layer shortlist (misses
  sub-constraint 1–2), and is architecturally simpler than ADS-Cascade (no upstream
  retrieval/candidate-generation layer).
- **Lykouris & Weng (2024)** — content-moderation AI-human pipeline with confidence-gated routing,
  structurally close to the cascade shape — but its AI is a direct risk classifier (not an LLM
  reranking candidates), and it explicitly permits high-confidence auto-decisions without human
  review, the opposite of ADS-Cascade's 100%-of-Tier-3-to-human invariant.
- **Singh & Szajnfarber (2025)** — names the "human selector from a filtered list" authority
  pattern generally, but not LLM- or reranking-specific.

## Verdict

**C (partially established).**

- The **reranking-only** half of the constraint (sub-constraints 1–2) is closer to **A** — a named,
  extremely well-documented pattern (RankGPT and its many descendants) that a reviewer would
  recognize immediately and expect cited.
- The **never-auto-applied / always-human-routed** half (sub-constraints 3–4) is closer to **B** —
  widespread, decades-old field common sense spanning automation-bias research, clinical decision
  support, learning-to-defer, and regulatory scholarship, but not attributable to any single citable
  source; too diffuse to call "established prior art" in the singular.
- The **specific joint assembly** of all four sub-constraints into one cascade tier — LLM
  simultaneously restricted to reranking a pre-fetched shortlist, barred from blank-slate
  classification, structurally incapable of auto-applying (not merely conditionally, and without a
  high-confidence auto-execute branch), and positioned as the terminal tier of a broader
  deterministic cascade — was not found described together anywhere in this search.

**This does not support a claim that the mechanism itself is new** — every individual piece has
clear precedent, and the reranking piece specifically has no defensible novelty claim available at
all. What may survive, narrowly, is the specific combination as configured in this cascade
position — a materially weaker and more precisely-scoped claim than "LLM-advisory-only is
distinctive."

## Recommendation for the manuscript

`TECHNICAL_REPORT.md` §2.4 should explicitly cite RankGPT (Sun et al. 2023) as the direct
methodological ancestor of the Tier-3 reranking mechanism, and should cite the learning-to-defer
lineage (Mozannar & Sontag 2020) and/or the automation-bias/CDSS literature (Cummings 2004; Khera
et al. 2023) for the "always routes to human" design principle, rather than presenting either as
an unclaimed design choice. If a novelty point is retained here at all in Phase C, it should be
scoped narrowly to the specific four-part combination, not to any individual constraint.
