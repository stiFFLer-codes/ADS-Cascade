# Gap-Verification Report — ADS Metric Mathematical Prior Art

> Targeted follow-up pass (2026-08-11), scoped to close the highest-priority gap flagged at the end
> of the main Phase B sweep: the label-noise / inter-annotator-agreement / data-quality literature
> was never searched in the original pass. This document reports what that search found. Full
> per-source detail in `ads_metric_prior_art.csv`. Per the mission brief for this pass: **this
> document does not defend ADS's novelty** — it reports the closest prior art plainly, including
> where the answer is unfavorable to a novelty claim.

## ADS's exact mathematical definition (restated for reference)

For a product/item $p$ with historical occurrence counts $c_1, \dots, c_k$ across accounts
$a_1, \dots, a_k$:

$$\text{ADS}(p) = \frac{\max_i c_i}{\sum_i c_i}$$

Aggregated two ways: **unweighted** (mean of $\text{ADS}(p)$ over distinct products — catalog-level)
and **weighted** (mean weighted by occurrence count — line-level).

## Search coverage

Consensus, FastTrack Literature Open (`search_papers` + `get_paper`), Scholar Gateway
`semanticSearch`, and WebSearch for bibliographic verification. ~250+ raw results screened; 9
sources retained as directly load-bearing for the comparison (`ads_metric_prior_art.csv`). Full
query log preserved in the underlying agent transcript; representative queries: "cluster purity
metric clustering evaluation majority class proportion," "Dawid Skene repeated labeling
crowdsourcing majority vote baseline truth inference," "percent agreement majority vote proportion
inter-annotator agreement raw agreement," plus direct `get_paper` DOI verification on every
retained source.

## What was found

### Exact match #1 — Cluster purity

Cluster purity (Manning, Raghavan & Schütze 2008, *Introduction to Information Retrieval*, Ch.
16.3; formalized rigorously in Amigó, Gonzalo, Artiles & Verdejo 2009, *Information Retrieval*,
DOI `10.1007/s10791-008-9066-8`; independently confirmed in the CLUTO-toolkit lineage, Zhao &
Karypis 2003) is defined, per cluster, as:

$$\text{purity}(\omega_k) = \frac{\max_j |\omega_k \cap c_j|}{|\omega_k|}$$

— the fraction of a cluster's members belonging to its single most common ground-truth class.
**This is the identical closed-form expression as ADS**, under the substitution: "cluster" ↔
"an item's historical booking multiset," "ground-truth class" ↔ "GL account." ADS's weighted
(line-level) aggregate is the same size-weighted average used for corpus-level purity. This is not
a loose analogy — it is the same formula applied to a relabeled unit of analysis.

### Exact match #2 (informal, uncited) — Raw majority-vote-agreement proportion

Independently, in the crowdsourcing / label-aggregation literature descending from Dawid & Skene
(1979, *JRSS-C*), the raw proportion of repeated labels agreeing with an item's majority (modal)
label is the standard naive baseline every truth-inference method (Dawid-Skene EM, spectral
methods, deep-learning-from-crowds) is benchmarked against — confirmed independently by Uma et al.
2021 (JAIR survey), Davani, Díaz & Prabhakaran 2021 (arXiv), and the Fleiss (1971) inter-rater-
reliability lineage. This quantity is mathematically identical to ADS and matches ADS's unit of
analysis even more closely than cluster purity (per-item, repeated historical judgments, not a
one-shot clustering comparison) — but critically, **it circulates without a dedicated, independently
citable name or paper**. It is referred to descriptively ("majority vote," "percent agreement with
the majority label") rather than treated as a named metric the way Cohen's/Fleiss's kappa are.

### Structural near-misses, ruled distinct

- **Fleiss's kappa itself** (Fleiss 1971) computes a *pairwise*-agreement fraction per item
  ($P_i = \sum_j \binom{n_{ij}}{2} / \binom{n}{2}$), not max/sum — mathematically different from
  ADS, converging toward it only under specific distributional conditions.
- **Confident Learning** (Northcutt, Jiang & Chuang 2021, JAIR) — uses a *model's* predicted-
  probability confusion structure against given labels, not repeated historical labels. Different
  input, different mechanism; convergent goal only.
- **Maximum Softmax Probability / MSP** (Hendrycks & Gimpel 2017) — `max(softmax output)`, the
  same *operator* (take the max of a distribution) applied to a *model's* live predictive
  distribution rather than an empirical historical frequency distribution. Worth citing as a
  precise contrast: same operator, categorically different input.
- **Learning from Disagreement** (Uma et al. 2021, JAIR survey) — represents the opposite design
  philosophy: this literature argues *against* collapsing multi-annotator label distributions to a
  point estimate, whereas ADS deliberately does exactly that.

## Verdict

**B (a known metric under a different name), with a substantial secondary D (novel only in its
system-design application).**

ADS's mathematical core is not new. It is cluster purity, reapplied to per-item historical booking
history instead of clustering output — the same closed-form expression, independently and
rigorously documented since at least 2003–2009 in the clustering-evaluation literature — and it is
simultaneously the same quantity as the uncited raw majority-vote-agreement baseline used
throughout the Dawid-Skene-descended crowdsourcing/truth-inference literature since 1979. Both
lines of evidence point to the same conclusion from independent directions, which is strong
adversarial confirmation, not a single coincidental match.

What is **not** found anywhere in this search — across clustering evaluation, inter-annotator-
agreement/crowdsourcing, confident learning, and OOD-confidence literature — is this quantity
being computed from real transactional history and used **as a signal for automatically selecting
which classification architecture to deploy, once, before serving traffic**. Its documented uses
are strictly: (a) post-hoc clustering-quality evaluation, (b) a naive baseline/diagnostic in
truth-inference research, or (c) — for the MSP/confident-learning family specifically — model-
confidence or label-error detection. None of the retrieved literature treats it as an architecture-
selection or design-time routing signal.

## Recommendation for the manuscript

Position ADS explicitly as "cluster purity, computed per catalog item over historical label
assignments" (cite Manning, Raghavan & Schütze 2008 and/or Amigó et al. 2009), and note it is
mathematically identical to the informally-named raw majority-vote-agreement baseline used
throughout the Dawid-Skene descendant literature (cite Dawid & Skene 1979). **The paper's novelty
claim for this component should rest entirely on the architecture-selection/cascade-routing
application of the metric, not on the metric's mathematical construction.** Claiming the metric
itself as new would not survive a literature-aware review.
