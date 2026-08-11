# Experiment 1 Redesign Review — H1 (Historical Consistency → Mechanism-Class Selection)

> Review-only document. Produced under the Phase D pre-implementation review mandate. Does not
> modify `research/experimental_hypotheses.md`, `research/experimental_design.md`,
> `TECHNICAL_REPORT.md`, `README.md`, or `METHODOLOGY.md`, and nothing here has been implemented,
> piloted, or run. Where this document's decisions diverge from the two files above, this document
> is the design authority for Experiment 1 going forward; those files should be reconciled to it in
> a later, explicitly-approved editing pass — not silently treated as already updated.

---

## 1. Executive decision

The prior design (`experimental_design.md` Experiment 1) was directionally sound but had four
defects serious enough to invalidate a straightforward implementation:

1. It used the generator's *control* parameter (`DETERMINISTIC_SHARE`) as if it were the
   *scientific* independent variable, rather than the post-hoc measured quantity it actually
   thresholds against (`det_pct`, computed downstream by `03_5_dataset_intelligence.py`).
2. It called the fuzzy-lexical retrieval mechanism "embedding-primary" without qualification, and
   the synthetic product strings it would be tested on contain no lexical variation at all — so the
   retrieval leg had nothing to meaningfully retrieve *across*.
3. It planned to feed the LLM mechanism a classification task (`"SYNTH FUEL 00073"` → account)
   without checking whether the synthetic generator's product string actually carries any signal
   predictive of the true label. It does not — see §10. Testing the LLM on this task risks
   contaminating the primary comparison with noise unrelated to historical consistency.
4. Several leakage, calibration, and metric-definition questions were left implicit rather than
   pre-specified, which is exactly the gap that lets an experiment's own construction bias it toward
   confirming H1.

This document resolves all four, tightens H1 to a claim the design can actually support, and
produces a concrete, falsifiable, pre-registerable specification. **Recommendation: conditional GO
for harness implementation and a pilot, not for the frozen 20-seed run** — five decisions in §24
still need the author's sign-off before freezing.

---

## 2. Revised H1

> **H1 (revised).** Under controlled synthetic conditions, higher **realized historical decision
> consistency** (measured after data generation, not the generator's target parameter) will be
> associated with predictable changes in the relative performance of classification mechanisms,
> such that the mechanism selected by a pre-specified, frozen consistency-based decision rule will
> agree with the empirically best-performing mechanism **more often than chance**.

This is deliberately weaker than the original phrasing ("rules-first dominates at 0.90–0.99...").
It claims *better-than-chance agreement*, not *monotonic dominance in every band* — monotonic
dominance, if observed, is a stronger finding the analysis can still report, but it is not baked
into the hypothesis itself, so a non-monotonic but still above-chance result is not automatically a
falsification (see §19).

---

## 3. Independent variable

**Primary IV: `realized_det_pct`** — the share of products, computed on the **train split only**
(see §13) of a given generated condition, with per-product `determinism_score > 0.95`, using the
*current, A5-corrected* aggregation logic in `03_5_dataset_intelligence.py` Module C.1 (sum counts
by `account_id` across all rows before selecting the dominant account — the pre-fix row-max bug is
not to be reintroduced).

This is the exact quantity `04_architecture_decision.py::decide_model_complexity()` thresholds at
0.90/0.70 to emit R3's RULES_FIRST / EMBEDDING_PRIMARY / LLM_REQUIRED decision. Using anything else
as the IV would make "does the rule agree with the empirical winner" incoherent — the rule was
built for this specific quantity, not for weighted ADS, unweighted/mean ADS, or cross-company
consistency, all of which are different, real, differently-defined numbers already found conflated
in Phase A (`RESEARCH_AUDIT.md` finding A3). `00_generate_synthetic.py`'s `DETERMINISTIC_SHARE` is
demoted to a **generation control parameter** — it is recorded per condition but never appears on
an axis of any primary result.

**Recorded but non-primary, per condition (diagnostic covariates, reported to prevent the exact
A3-style conflation from recurring here):**
- `target_deterministic_share` (the generator knob)
- `realized_det_pct_full` — the same statistic computed over train+test combined, reported once as
  a sanity cross-check against the leakage-safe `realized_det_pct` (train-only); a large gap between
  the two would itself be worth a footnote, but only the train-only value drives any decision or
  analysis.
- `weighted_ads`, `unweighted_ads` (train-only, same corrected pipeline)
- `cross_company_consistency` (train-only)

---

## 4. Controlled variables

Fixed identically across all six target bands and both lexical conditions, changed only between
the *pilot* and *frozen calibration* runs (never mid-sweep):

| Variable | Value | Why fixed |
|---|---|---|
| Company count | 60 | Existing generator scale; changing it would confound sample-size effects with the IV |
| Product vocabulary size | 1,200 | Same reason |
| Cross-company alignment (`CROSS_COMPANY_ALIGN`) | 0.695 | Existing, evidence-derived production value; sweeping it alongside `DETERMINISTIC_SHARE` would be a second independent variable and violate the "avoid a large factorial" instruction |
| Invoice-volume model (lognormal params) | unchanged from `00_generate_synthetic.py` | Controls transaction volume |
| Product-weight (frequency) distribution | unchanged lognormal | Controls per-product occurrence count |
| VAT stability / purchase-sale split | unchanged (0.945 / 0.739) | Not the object of study |
| Account pool (chart of accounts) | unchanged `PURCHASE_ACCOUNTS`/`SALE_ACCOUNTS` | Fixed universe of classes |
| Train/test split procedure | existing `split_of()`, unchanged 80/20 hash split | Reused, not re-derived |
| Lexical-variation algorithm (§8) | fixed algorithm; only the ON/OFF switch varies | One controlled factor, not several |

**Variables that necessarily co-vary with the IV, measured and reported, not artificially held
constant** (per the instruction not to silently force these fixed, since doing so could itself be
scientifically incoherent):
- **Class (account) frequency concentration.** Determinism is a within-product concentration
  property; as `DETERMINISTIC_SHARE` rises, the account-frequency distribution *may* become more
  peaked as a second-order effect. Report a Herfindahl–Hirschman index (HHI) over test-split account
  frequencies per condition as a diagnostic, not a control.
- **Realized ADS vs. target divergence at the extremes.** Because `CROSS_COMPANY_ALIGN` stays fixed
  at 0.695 while `DETERMINISTIC_SHARE` sweeps toward 0.99, the ~12% of products that are
  multi-company will structurally cap how high `realized_det_pct` can go, independent of the
  generation knob — flagged in the prior review (§4ii there) and carried forward here as a
  pre-registered, expected, reportable ceiling effect, not a bug to silently work around.
- **Test-split size (N).** Held-out row count per condition is a downstream consequence of the
  (fixed) invoice-volume model, not directly set; it will vary condition-to-condition by ordinary
  sampling variance. Report N per condition; bootstrap CIs computed per condition naturally reflect
  this.

---

## 5. Nuisance variables

Variables that must be *randomized over*, not fixed, so their effect averages out across seeds
rather than aliasing with the IV:

- Which specific accounts land in each product's disagreement pool (`random.sample(pool, ...)`).
- Which companies share a given multi-company product, and the exact per-company agree/disagree
  draws.
- Exact invoice count and line count per company/invoice (lognormal draws).
- The per-line lexical-transform draws (§8), when the lexical condition is ON.

**RNG-independence requirement (a genuine implementation bug in the current generator, must be
fixed before any multi-seed sweep is possible):** `00_generate_synthetic.py` currently calls
`random.seed(42)` once at **module import time** and every downstream function mutates the single
global `random` module state. A sweep across 20+ seeds needs each seed to produce an
**independent, reproducible stream**, not 20 draws chained off one mutating global. The generator
must be refactored so `gen_dataset(seed, ...)` constructs its own `random.Random(seed)` instance and
threads it explicitly through every function that currently calls the bare `random.*` module
functions — otherwise seed 2's output depends on how much of the RNG stream seed 1 consumed, which
breaks both reproducibility (any refactor elsewhere silently shifts every later seed's output) and
the statistical independence the bootstrap analysis assumes.

---

## 6. Experimental conditions

Two controlled factors, not a large factorial:

- **Factor 1 — target consistency band** (6 levels): ≈0.60, 0.70, 0.80, 0.90, 0.95, 0.99
  (generation-time `DETERMINISTIC_SHARE` values; analysis uses `realized_det_pct`, §3).
- **Factor 2 — lexical condition** (2 levels): CLEAN (existing generator, unchanged) vs. VARIED
  (§8's transform, fixed algorithm and frozen rate).

6 × 2 × ≥20 seeds = **≥240 generated dataset conditions**, each evaluated with 2 isolated mechanisms
(rules-only, retrieval-only — LLM excluded from the primary comparison, §10). No third factor is
added (no synonym-substitution axis, no separate OCR-noise axis, no separate class-imbalance
sweep) — this is the deliberate ceiling on scope the task instructions set.

---

## 7. Realized-ADS strategy

1. Generate at the target `DETERMINISTIC_SHARE`.
2. Compute `realized_det_pct` from the **train split only** (§13) using the corrected Module C.1
   logic.
3. Use `realized_det_pct` — never the target — as the x-axis for every primary plot, table, and
   statistic.
4. **Tolerance, not regeneration.** A condition is labeled "on-target" if
   `|realized_det_pct − target| ≤ 0.05`; conditions outside that band are **kept, not discarded or
   regenerated** — this is itself informative (e.g., if the 0.99 target band never realizes above
   ~0.93 because of the `CROSS_COMPANY_ALIGN` ceiling in §4, that is a reportable finding about the
   generator's realizable range, and the analysis must still use the true realized value). No seed
   is ever re-drawn because its realized value was inconvenient.
5. If, after generation, the realized values across the 6 target bands do not actually span a
   useful range of `realized_det_pct` (e.g., bands 0.90/0.95/0.99 all realize within 0.02 of each
   other because of the ceiling effect), that is reported as a limitation of the generator's dynamic
   range, not patched by re-tuning thresholds after the fact.

---

## 8. Lexical-variation design

**Two conditions only: CLEAN (existing generator, byte-identical to today's output) and VARIED
(one fixed transformation algorithm, toggled on).** No synonym-substitution axis is included — the
category token (§10) is already established to carry no ground-truth signal, so semantic paraphrase
is out of scope for this factor; a synonym axis would add a second noise dimension without a clear
question it answers.

**Algorithm (applied per invoice line at generation time, VARIED condition only):**

```
for each generated invoice line with product index p, logical_key k, line_number n:
    local_seed = stable_hash(global_seed, k, n)     # same crc32-based convention as split_of()
    rng = random.Random(local_seed)                  # independent, reproducible per line
    if rng.random() < P_TRANSFORM:
        n_transforms = rng.choice([1, 2])
        chosen = rng.sample(TRANSFORM_TYPES, k=n_transforms)
        apply each chosen transform (independently, in list order) to the surface string
    else:
        surface string unchanged
```

`TRANSFORM_TYPES` (5, matching the brief's examples):
1. **Case variation** — each whitespace-delimited token independently upper/lower-cased.
2. **Punctuation variation** — insert a hyphen or period at one randomly chosen token boundary.
3. **Token reorder** — swap the fixed `"SYNTH"` prefix and the category token (the only two
   semantic tokens preceding the numeric id — a single well-defined, reversible swap).
4. **Abbreviation** — truncate the category token to its first 3 characters + `.`.
5. **Whitespace variation** — replace one inter-token space with a double space or a tab.

**Semantic identity is preserved by construction, not by convention:** the transform is applied
only to the display/lookup string (`product_description`/`normalized_product`); the ground-truth
key used for KB-building and accuracy scoring remains the existing stable `product_code`
(zero-padded product index, already a separate column in the row schema) — untouched by the
transform. A mechanism can be surface-confused, but "correct" is never ambiguous, because grading
never looks at the surface string.

**Reproducibility** is guaranteed by the deterministic per-line sub-seed derivation above — no
extra state needs to be stored; re-running the same `(global_seed, logical_key, line_number)` always
reproduces the same transform decision.

**`P_TRANSFORM` is not asserted as a first-principles constant** — the brief explicitly warns
against inventing an arbitrary corruption rate. Instead it is an empirically-tuned, pre-registered
**pilot output**: the pilot (§18) evaluates `P_TRANSFORM ∈ {0.3, 0.5, 0.7}` against the acceptance
criterion "a non-trivial share (target: 15–40%) of held-out test lines have a normalized-product
string not byte-identical to any train-split occurrence of the same true product," and freezes
whichever candidate lands closest to the middle of that target band. The rate is fixed for the
entire frozen run once chosen — never re-tuned after seeing mechanism accuracy results.

**Known side effect, expected and desired, not a bug:** because the transform is applied
independently per line, a single product can appear under multiple surface forms even within the
*train* split (different companies, different draws). This further fragments the rules-only
mechanism's exact-key hit rate under VARIED — that is the intended stress condition, and its
magnitude is exactly what the retrieval-vs-rules comparison is measuring.

---

## 9. Retrieval mechanism decision

**Option A — local embedding model.** Genuine semantic retrieval; would let "embedding-primary"
be a literally accurate name. Costs: a new, heavy dependency (a sentence-embedding library plus a
downloaded model checkpoint, hundreds of MB), a reproducibility risk this repo does not currently
carry anywhere (model-hub availability, version pinning, hash-verifying weights, potential future
deprecation of the exact checkpoint used), a live-download-or-vendor-weights decision that conflicts
with the repo's offline/no-client-data convention if vendored, and materially higher compute cost
across 240 conditions. Most importantly: a general-purpose sentence embedding model is not trained
on Romanian accounting product strings, and the controlled lexical-variation transform in §8
(case/punctuation/reorder/whitespace/abbreviation) is exactly the class of surface noise that
character/token-level fuzzy matching (rapidfuzz's `WRatio`, which already blends token-sort and
token-set scoring) is designed to be robust to as well — so it is not obvious an embedding model
would show a *qualitatively different* pattern on *this specific* noise design, only a possibly
better one on the same axis, at much higher implementation and reproducibility cost.

**Option B — keep rapidfuzz, rename the mechanism.** Zero new dependencies, fully deterministic
(no model download, no hardware-dependent numerics), matches the repo's existing stdlib-first,
offline-first convention, and — critically — is scope-honest: it stops calling a lexical-similarity
mechanism "embedding-primary" without evidence it behaves like one, which is exactly the kind of
staleness Phase A's audit (finding A6) already penalized elsewhere in this repository for a
different mechanism.

**Recommendation: Option B.** Rename the mechanism **"retrieval-primary / similarity-based
retrieval"** everywhere in the experiment's code, output columns, and write-up. Reasoning,
prioritized as instructed: reproducibility and deterministic execution (Option B wins outright —
no model/hardware nondeterminism), no paid API dependency (both options satisfy this, moot), stable
model version (Option B has no model to version), minimal infrastructure (Option B wins — no new
dependency), fair comparison (roughly a wash — see the middle-paragraph argument above; a real
embedding model's advantage on *this specific* controlled noise is not clearly established, so it
would not obviously make the comparison fairer, only add cost and a new failure surface). A local
embedding model remains a legitimate **future upgrade**, explicitly out of scope for H1, and would
be its own approved research question if the paper later wants a genuine embedding-vs-lexical claim
(orthogonal to whether historical consistency predicts mechanism-class choice at all).

**Implementation changes needed if this recommendation is accepted (not built yet):** rename
`fuzzy_company`/`fuzzy_global` call sites in the isolated-mechanism harness's user-facing labels and
CSV `mechanism` column from `"embedding_primary"` to `"retrieval_primary"`; no change to
`p2lib/retrieval.py` itself.

---

## 10. LLM inclusion/exclusion decision

**Central finding: the synthetic product string carries no signal predictive of the true label, by
construction.** In `00_generate_synthetic.py::gen_products()`:

```python
pool = PURCHASE_ACCOUNTS if direction == "PURCHASE" else SALE_ACCOUNTS
...
accounts = random.sample(pool, k=min(n_accts, len(pool)))
cat = random.choice(CATEGORIES)
name = f"SYNTH {cat} {i:05d}"
```

`cat` (the only semantically-readable token in the product string, e.g. `"FUEL"`) is drawn from
`CATEGORIES` **independently** of `accounts` (the account pool actually sampled for that product).
There is no code path anywhere that makes `"FUEL"` more likely to end up mapped to the real
fuel-expense account (`6022`) than to any other account in the purchase pool. A human or LLM reading
`"SYNTH FUEL 00073"` and reasoning "fuel → account 6022" would be reasoning from a regularity the
generator does not implement — any apparent semantic fit is coincidental, not a property of the
data-generating process.

**Answering the seven questions:**
1. *Can the current synthetic task fairly test an LLM?* No — see above. The label is generated
   independently of the only human-readable content in the input.
2. *Does the LLM have enough semantic information to reason?* It has real-world semantic priors
   (Romanian account descriptions like `"CHELT. PRIVIND COMBUSTIBILUL"` are genuine), but the
   product string's category token is not actually wired to those priors by the generator, so
   applying them would, if anything, introduce a **systematic bias uncorrelated with the
   independent variable** — the worst kind of confound, because it could produce an apparent
   accuracy pattern that has nothing to do with historical consistency at all.
3. *Zero-shot, few-shot, or retrieval-augmented?* As specified for a clean isolated-mechanism test
   (§9 of the original design), it would be zero-shot, fed the full static chart of accounts — no
   candidates, no history. This also does not match the production system's actual LLM role
   (reranking retrieved candidates, never blank-slate classification per ADR-007/§2.4 of the
   manuscript), so a zero-shot result here would not even transfer back to describing the shipped
   system's real behavior.
4. *Live-API stochasticity/cost?* Real, but secondary to (1)–(3) — moot if the task itself isn't
   valid.
5. *Can caching make it reproducible?* Yes, mechanically (existing `adapter.py` convention), but
   reproducible measurement of an invalid test is not evidence.
6. *Would a local/free model help?* No — the problem is the task construction, not the model choice
   or its cost.
7. *Should LLM be excluded from the primary H1 comparison?* **Yes.**

**Recommendation: exclude the LLM mechanism from the primary H1 statistical comparison.**

**What H1 then tests:** whether realized historical consistency predicts the crossover between
**rules-first exact-precedent lookup** and **retrieval-primary similarity-based lookup** — i.e.,
whether consistency predicts when precedent-based methods (either exact or fuzzy) suffice versus
degrade. This is not a narrowing invented to dodge a hard problem: per `RESEARCH_AUDIT.md` finding
A4 and `r3_threshold_analysis.md`, the `LLM_REQUIRED` band (`det_pct < 0.70`) has **never once been
empirically triggered** by either the production or synthetic run in this repository's history —
excluding it from Experiment 1 removes an already-untested region, not a validated one. Nothing
that has ever actually been observed is being discarded.

**Where the LLM remains relevant to the broader architecture (explicitly out of scope for H1, not
denied):** the production system's actual, evidenced LLM role is candidate-reranking on the
already-retrieved review tail for genuinely novel items (Phase 2's `p2_06_llm_tail.py` /
`llm_tail_proposals.csv`), a different question than "can the LLM classify from a bare product
string." Testing *that* claim validly would require synthetic product strings with genuine,
generator-wired semantic content (i.e., making the category token actually predictive of the
account, probabilistically) — a real, defensible extension, but a **new, separate, explicitly
approved research question**, not an ad hoc addition to H1 to keep three mechanisms in the primary
comparison for its own sake.

---

## 11. Mechanism interfaces

Primary comparison — **two** isolated mechanisms, built by adding a `mode` parameter over the
*existing* KB/retrieval primitives (no parallel codebase, per the repo's own ponytail-style
convention already invoked for Experiment 2 in `experimental_design.md`):

- **`rules_only`** — exact `(cui, product_surface_string)` company lookup, then exact global
  lookup; any hit is accepted as the mechanism's answer (no ADS/evidence gating — that policy logic
  belongs to the shipped cascade's tiering, not to this mechanism-capability test); no hit = abstain.
  **No confidence threshold to calibrate** — binary exact-match/no-match.
- **`retrieval_only`** — rapidfuzz fuzzy match (`fuzzy_company` then `fuzzy_global`) used as the
  **primary** classifier, not a fallback gated behind a rules-miss; accept if score ≥ a single
  calibrated cutoff (§12); below cutoff = abstain.

**LLM interface — not built for the primary comparison** (§10). If a future, separately-approved
experiment revisits the LLM condition, `adapter.propose_account()` already supports a from-scratch
call (pass the full static chart instead of retrieved candidates) with **zero adapter code changes**
— noted for that future work, not implemented now.

The central comparison this produces is exactly "which mechanism performs best at this realized
consistency level," never "does the shipped cascade perform well" (that is H2, explicitly out of
scope, per §9 of the original task).

---

## 12. Calibration protocol

**Only `retrieval_only` has a tunable threshold** (rapidfuzz score cutoff); `rules_only` has none.

- **Calibration data:** a single, separate generation run — its own seed (fixed, documented,
  distinct from every seed used in the 6-band × 2-lexical × 20-seed frozen sweep), `DETERMINISTIC_SHARE = 0.80`
  (the midpoint of the target range, deliberately not one of the six official bands, and both
  lexical conditions generated once each), same company/product scale as the main conditions. This
  avoids calibrating on the exact data the final comparison will run on, while still calibrating
  under representative synthetic conditions.
- **Candidate threshold range:** rapidfuzz `WRatio` score cutoff ∈ `{70, 75, 80, 85, 90}` (the
  existing shipped constants — `T2_SIM=85`, `GLOBAL_FUZZY_CUTOFF=88` — sit inside this range, so the
  calibration is checking, not ignoring, prior production experience).
- **Optimization criterion:** maximize whole-set accuracy (§14) on the calibration set's held-out
  slice, subject to a minimum coverage floor of 30% (a cutoff that "wins" by abstaining on
  everything is rejected regardless of its accuracy-among-covered-items).
- **Selected threshold:** determined by running the calibration once, before the frozen sweep, and
  recorded verbatim (not re-run or re-selected afterward) in the frozen-config artifact (§20).
- **Calibration instability handling:** if the accuracy-vs-cutoff curve has no single clear maximum
  (multiple cutoffs within 1 percentage point of the best), select the **highest** (most
  conservative / precision-favoring) near-tied cutoff — consistent with this repository's own
  existing precedent of choosing safety over aggressiveness when a calibration run found the
  original design unsafe (`EVIDENCE_BASELINE.md`'s `FUZZY_AUTO_APPLY=False` history). The full
  candidate curve is written to the calibration artifact regardless of outcome, so the choice is
  auditable.
- Calibration happens **once**, before any of the 6×2×20 frozen conditions are generated, and the
  resulting cutoff is frozen into the config used for all of them — never re-tuned per band, per
  lexical condition, or after seeing results.

---

## 13. Train/test protocol

Three logically distinct data roles per generated condition, made explicit to close the leakage gap
the original design left implicit:

1. **Consistency-measurement data (train split only).** `realized_det_pct` (§3) — the "design-time"
   signal the mechanism-selection rule acts on — is computed **exclusively from the train split**,
   mirroring the real deployment temporal logic: a design-time decision can only see history, never
   the future held-out data it will be judged against. Computing it over the full dataset (as the
   original design left ambiguous) would leak test-set label structure into the very signal being
   evaluated as a predictor — a direct instance of the leakage the task explicitly warns against.
2. **Mechanism-construction data (train split only).** The KB (`kb.build_from_rows(keep=lambda r:
   split_of(r) == "train")`) — reused unchanged from the existing Phase 2 convention.
3. **Calibration data (a separate, single dedicated generation run — see §12).** Never overlaps with
   any of the 6×2×20 frozen conditions' train or test data.
4. **Final evaluation data (test split only).** Every accuracy/coverage/cost number reported for a
   condition is computed exclusively on that condition's `test` rows (`split_of() == "test"`),
   classified by a mechanism built only from that same condition's `train` rows. No test row is ever
   used to compute `realized_det_pct`, calibrate a threshold, or build a KB.

`split_of()` itself is unchanged (deterministic `crc32(logical_key|line_number) % 5`) — reused
exactly as-is, since it does not depend on account labels and therefore cannot itself leak.

---

## 14. Primary metric — Mechanism-Selection Agreement

**Step 1 — per-mechanism performance criterion (defined once, before any run):**
**whole-set accuracy** — a prediction counts as correct only if the mechanism both answered *and*
was right; an abstention (no KB hit / below cutoff) counts as **incorrect**, evaluated over the
full test split for that condition. This is a single, pre-specified number that already composes
accuracy and coverage in one principled, standard (reject-option-literature) way, avoiding an
ad hoc weighted composite invented after seeing results.

**Step 2 — empirical winner.** Per condition (seed × band × lexical condition), the mechanism with
the strictly higher whole-set accuracy is the winner. **Tie handling:** if the two mechanisms'
paired-bootstrap 95% CIs on the whole-set-accuracy difference overlap zero, the condition is scored
as a **TIE**, reported as its own category — never broken toward either mechanism by convention, and
excluded from the strict agreement/disagreement count but reported as a distinct row (a tie-heavy
result is itself informative about how sharply consistency discriminates mechanisms).

**Step 3 — rule-selected mechanism.** Apply the **existing, unmodified** R3 constants
(`THRESHOLD_DETERMINISTIC_RULES=0.90`, `THRESHOLD_DETERMINISTIC_EMBED=0.70`) to that condition's
`realized_det_pct` (train-only): `≥0.90 → rules`, `[0.70, 0.90) → retrieval`, `<0.70 → LLM_REQUIRED`.
**LLM_REQUIRED cases are scored as `N/A — rule selects an excluded mechanism`**, not silently
dropped and not force-matched to either remaining mechanism. Given the six target bands include
0.60 and 0.70, some realized values will legitimately fall under 0.70 — this is expected and
pre-registered, not a design failure.

**Step 4 — aggregation.** Agreement rate = (# conditions where rule-selected == empirical winner) /
(# conditions with a **defined** comparison, i.e. excluding TIE and N/A rows, reported separately).
Primary reporting is **micro** (every seed × band × lexical trial is one Bernoulli observation);
band-level and lexical-condition-level agreement rates are reported as secondary breakdowns (this
doubles as part of the crossover analysis, §16).

**Chance baseline:** with the LLM leg excluded from the primary comparison, the rule discriminates
between **two** mechanisms wherever a comparison is defined — chance is **0.5**, not 1/3. (Framing
it as 1/3 — as if three mechanisms were always in play — would understate how hard the rule actually
has to work to look good, which is exactly the kind of thing that makes an experiment un-falsifiable
by accident.) Test statistic: one-sided exact binomial test of the observed agreement rate against
p = 0.5, plus a Wilson or bootstrap CI on the agreement rate itself.

---

## 15. Secondary metrics

- **Accuracy and coverage per mechanism per condition** — needed to see *why* an agreement/
  disagreement happened (a mechanism could "win" on whole-set accuracy while covering very little,
  which whole-set accuracy already penalizes, but the raw components remain diagnostically useful).
- **Cost proxy** — `rules_only`/`retrieval_only` lookup count as a unit cost (both effectively O(1)
  amortized / O(vocabulary) per query); wall-clock reported as a **diagnostic only**, since it is
  machine-dependent and not comparable across environments.
- **Per-condition variance across seeds** — needed to size the CIs in §14/§16 honestly and to
  support the "CIs too wide → inconclusive" falsification bucket (§19).
- **Bootstrap CIs** (percentile method, ≥2,000 resamples, stdlib `random`-based — no new dependency,
  matching this repo's existing stdlib-only convention) — needed because no closed-form CI is
  appropriate for whole-set accuracy under mechanism-specific abstention.
- **Mechanism-selection agreement** — the primary metric, also broken out by band and by lexical
  condition as a secondary table (directly supports §16).
- **Crossover point(s)** — see §16.

No metric is added beyond this list "because it's available" — macro/micro averaging is reported
only where it changes an interpretation (band-level breakdown), not computed for its own sake.

---

## 16. Crossover analysis

Per lexical condition (CLEAN and VARIED analyzed **separately**, never pooled, since H1's revised
form explicitly allows the relationship to hold in only one of the two):

1. Pool all seed-level `(realized_det_pct, whole_set_accuracy_rules − whole_set_accuracy_retrieval)`
   points across all six bands.
2. Sort by `realized_det_pct`. Walk the sorted sequence and record every `realized_det_pct` interval
   where the sign of the accuracy difference flips, estimating the crossing point by linear
   interpolation between the two bracketing points.
3. Report **every** crossing found, with a bootstrap CI on each (resample seeds with replacement,
   recompute crossings, take the percentile interval) — including the case of **zero** crossings
   (one mechanism dominates everywhere realized) or **more than one** (non-monotonic).
4. Compare the reported crossing point(s) against the frozen rule's actual constants (0.90, 0.70) —
   proximity is evidence for H1's threshold values specifically; a real but *displaced* crossing
   point is evidence for the qualitative relationship without validating the specific numbers, and
   must be reported as such, not rounded up to "H1 confirmed."

No monotonicity is assumed or enforced anywhere in this procedure — a non-monotonic result (e.g., a
sign flip, a flip back) is a valid, reportable outcome and is explicitly one of the falsification
triggers in §19.

---

## 17. Pilot protocol

**Purpose (only):** verify the generator's parameterized interface and RNG-independence fix behave
correctly; verify `realized_det_pct` is measurable and matches hand-computation on a tiny synthetic
case; verify the VARIED lexical condition actually changes measured retrieval accuracy relative to
CLEAN (a manipulation check — if it doesn't, `P_TRANSFORM` or the transform set needs revisiting
before freezing); verify `rules_only` and `retrieval_only` produce different predictions on at least
some held-out lines (confirms isolation actually decouples the mechanisms); verify the output CSV
schema carries every required field (§20); verify runtime is feasible to extrapolate to the full
sweep.

**Size:** 1–3 seeds, at minimum the two extreme target bands (0.60, 0.99) plus the band nearest the
frozen rule's exact threshold (0.90), × both lexical conditions. Small enough to debug quickly by
design.

**Acceptance criteria (all must hold before freezing):**
- Generator runs end-to-end at every pilot target/seed/lexical combination without error.
- `realized_det_pct` (train-only, corrected aggregation) is computed and logged for every pilot
  condition, and matches a hand-computed value on a constructed 3-product toy case.
- `P_TRANSFORM` candidate sweep (`{0.3, 0.5, 0.7}`, §8) produces a clear winner against the 15–40%
  target-share acceptance band; if none of the three candidates lands in range, the candidate set is
  widened and the pilot re-run before freezing (this is pilot iteration, explicitly permitted;
  re-running the *frozen* sweep after seeing its results is not).
- `retrieval_only` measurably outperforms `rules_only` on at least one VARIED-condition pilot slice
  where it does not on the matched CLEAN-condition slice (confirms the noise condition is doing
  real work, not zero work).
- `rules_only` and `retrieval_only` diverge in their predictions on ≥5% of held-out pilot lines
  (confirms mechanism isolation, not accidental convergence).
- Estimated full-sweep runtime (extrapolated from pilot timing × 240 conditions) is reported and
  judged feasible before proceeding.

**Pilot outputs are written to a clearly separate, non-cited scratch location, never copied into the
frozen-run's output tree, and never referenced as evidence in any later write-up.**

After pilot review and explicit author sign-off: **freeze** the configuration (generator params,
`P_TRANSFORM`, retrieval cutoff, RNG-seed manifest) and only then execute the ≥20-seed final run.

---

## 18. Falsification criteria

| Verdict | Criterion |
|---|---|
| **H1 SUPPORTED** | Agreement rate significantly above chance (one-sided exact binomial, p=0.5, α=0.05) in **both** lexical conditions; at least one crossover point's CI overlaps the existing 0.90 and/or 0.70 constants; direction of the relationship (higher realized ADS favors rules, lower favors retrieval) matches prediction. |
| **H1 PARTIALLY SUPPORTED** | Agreement significantly above chance overall, but only in **one** lexical condition; OR a real crossover exists but its CI is significantly displaced from 0.90/0.70; OR the relationship holds with a systematic minority of disagreeing bands rather than uniformly. |
| **H1 NOT SUPPORTED / FALSIFIED** | Agreement rate not distinguishable from 0.5 chance; OR the accuracy-difference curve is non-monotonic with multiple sign flips not attributable to CI-width noise; OR the direction of the relationship is reversed from prediction; OR agreement is significantly **below** chance (the rule systematically anti-selects). |
| **INCONCLUSIVE (underpowered)** | Bootstrap/binomial CIs at the pre-registered ≥20-seed count are too wide to distinguish any of the above at α=0.05. Treated conservatively as **insufficient to claim H1 SUPPORTED** — the prescribed remedy is a larger, still-pre-registered seed count in a follow-up run, never a relaxed α or a re-interpretation of the existing data. |

None of these criteria are contingent on which outcome is "wanted" — the SUPPORTED row requires the
same statistical bar (α=0.05, two-condition replication) regardless of which direction the result
points.

---

## 19. Reproducibility requirements

Every artifact below must be committed under `research/experiments/exp1/` (or an equivalent single,
clearly-named directory), offline-reproducible, no client data — consistent with this repository's
existing convention:

- **Frozen configuration** (generator params, `P_TRANSFORM`, retrieval cutoff, R3 constants used
  unchanged) — a single file, timestamped, committed **before** the frozen sweep's output exists.
- **Seed manifest** — the exact, deterministically-generated list of seeds per band/lexical
  condition (e.g., a documented rule such as `range(BASE, BASE+20)` per condition, never hand-picked
  after seeing any result).
- **Raw per-condition results** — one row per (seed, band, lexical condition, mechanism, test line)
  prediction record, for full auditability, plus a condition-level summary CSV.
- **Aggregated results** — the agreement table, crossover table, per-mechanism accuracy/coverage/
  cost tables with CIs.
- **Statistical summary** — the binomial test result, CIs, and the final verdict table (§18).
- **Plots** — accuracy vs. realized ADS per mechanism per lexical condition; agreement-rate bar
  chart with CI; crossover-point estimate with CI.
- **Experiment metadata** — Python version, `rapidfuzz` version, OS, execution date/time.
- **Execution instructions** — exact commands to regenerate every artifact above from scratch.
- **Final H1 verdict**, stated in the exact language of §18's table.
- **Calibration artifact** — the full candidate-cutoff accuracy curve from §12, not just the chosen
  value.
- **Pilot report**, clearly labeled non-evidentiary, kept separate from the frozen artifacts above.

---

## 20. Phase D stopping criteria (hard stop)

Phase D / Experiment 1 (H1 only) is complete when, and only when, **all** of the following exist,
committed:

- RNG-independence fix and parameterized generator, with a regression test proving today's default
  (seed 42, `DETERMINISTIC_SHARE=0.95`, no lexical variation) output is byte-identical to the
  current committed output.
- Pilot completed, reviewed, and explicitly signed off by the author against §17's acceptance
  criteria.
- Frozen configuration committed, predating the frozen run's output.
- ≥20 seeds × 6 bands × 2 lexical conditions completed for `rules_only` and `retrieval_only`.
- Calibration completed once, on its own dedicated data, before the frozen run, never revisited.
- §14's primary metric, §15's secondary metrics, and §16's crossover analysis all computed and
  committed.
- A single, explicit H1 verdict issued per §18's table.
- Every artifact in §19 committed to the public repository.
- Limitations documented, including the ones surfaced in this review (§9's retrieval-fidelity scope,
  §10's LLM exclusion rationale, §4's `CROSS_COMPANY_ALIGN` ceiling effect, §8's pilot-tuned
  `P_TRANSFORM`).

**After that: STOP.** Do not automatically proceed to H2 or H3. Do not begin manuscript rewriting.
Do not add the LLM mechanism, a local embedding model, a synonym-substitution axis, or any other new
model/dataset/condition without it being explicitly proposed and approved as a distinct, new
research question. Do not re-tune any threshold, transform rate, or generator parameter after the
frozen run's results are known.

---

## 21. Implementation gap list

Everything below is **not yet built**; nothing here has been implemented this session.

| Item | Category | Notes |
|---|---|---|
| Per-call `random.Random(seed)` refactor of `00_generate_synthetic.py` | Bug fix, blocking | Module-level `random.seed(42)` must be removed before any multi-seed sweep is valid |
| `DETERMINISTIC_SHARE` / seed as function parameters | Parameterization | Mechanical |
| Lexical-variation transform (§8) | New | Needs the stable per-line sub-seed helper (reuse `split_of()`'s crc32 convention) |
| Train-only `realized_det_pct` computation, callable as a library function (not just a full pipeline script) | New | Port of `03_5_dataset_intelligence.py` Module C.1, restricted to a row subset |
| `rules_only` / `retrieval_only` isolated-mechanism harness | New | Thin `mode` parameter over existing `kb.py`/`retrieval.py` primitives; **no LLM interface built** per §10 |
| Retrieval mechanism relabeling (`embedding_primary` → `retrieval_primary`) | Rename only | No logic change |
| Calibration runner (§12) | New | Separate dedicated generation + candidate-cutoff sweep |
| Bootstrap CI / crossover-point stats module | New | stdlib `random`-based, no numpy/scipy — matches existing stdlib-only convention |
| Sweep-runner script | New | Loops conditions, writes per-condition CSVs |
| Pilot self-check tests | New | ponytail-style `test_*.py`, no framework |

Explicitly **not** needed, contrary to the original design's assumption: any LLM adapter changes
(§10), any embedding-model dependency (§9).

---

## 22. Threats to validity

- **Retrieval-fidelity scope (carried from §9).** Findings about "retrieval-primary" describe
  rapidfuzz lexical similarity under a specific, pilot-tuned synthetic noise model — they are not a
  claim about semantic embedding models, and the write-up must say so explicitly, not imply
  generalization.
- **`CROSS_COMPANY_ALIGN` ceiling (§4, §7).** Realized ADS at the high target bands may not reach
  the nominal target; reported honestly, but it does narrow the effective range the crossover
  analysis can probe near 0.95–0.99.
- **`P_TRANSFORM` is empirically tuned to a pilot acceptance band, not derived from real OCR/typo
  error-rate data.** An external-validity limitation to state plainly: the lexical-noise level is
  chosen to make the retrieval mechanism testable, not measured from any real document-error corpus.
- **`realized_det_pct` is a single dataset-level scalar per condition**, matching R3's own
  dataset-level framing (a deliberate scope match, not an oversight) — it does not capture
  per-product heterogeneity the way the shipped cascade's per-item tiers do. That is intentional:
  Experiment 1 tests R3's dataset-level rule, not the cascade's per-item tiers, and the two must not
  be conflated in the write-up.
- **Single synthetic-generator "world."** As with every existing result in this repository, findings
  describe this generator's structure; they are not evidence about real invoice data, and the
  existing repository-wide limitation language applies unchanged here.
- **Excluded-LLM scope narrowing.** A SUPPORTED verdict under this design would support "consistency
  predicts the rules-vs-retrieval crossover," not the full three-way claim in the original H1
  phrasing — the write-up must state this narrowing explicitly wherever the result is cited.

---

## 23. Decisions requiring human approval before implementation

1. **`P_TRANSFORM` final value** — pilot-tuned from `{0.3, 0.5, 0.7}` per §8/§17; needs author
   sign-off on the pilot's chosen rate before it is frozen into the real sweep.
2. **Calibration protocol** — a separate dedicated calibration generation run (this document's
   recommendation, §12) vs. carving a calibration slice out of each condition's own train split;
   the former is recommended for cleanliness, needs confirmation.
3. **LLM full exclusion vs. a clearly-labeled, non-primary exploratory appendix condition** — this
   document recommends full exclusion from the *primary* comparison (§10); if the author wants a
   cheap, explicitly-non-evidentiary exploratory LLM run anyway (e.g., purely to document *how* it
   fails on this task, as a limitations-section data point), that is a small addition but must be
   pre-labeled as exploratory, never folded into §14's primary statistic.
4. **Seed-manifest generation rule** — a simple deterministic range vs. a hash-derived list; either
   is fine, needs a documented choice before freezing.
5. **Output directory** — `research/experiments/exp1/` (this document's assumption) vs. `data/
   outputs/experiments/`, for consistency with whichever convention the author prefers going
   forward for Phase D artifacts generally.

---

## GO / NO-GO for implementation

**Conditional GO** — for building the harness described in §21 and running the pilot described in
§17. **NO-GO for the frozen ≥20-seed run** until: (a) the pilot has run and met every acceptance
criterion in §17, and (b) the five decisions in §23 have explicit author sign-off, particularly the
frozen `P_TRANSFORM` value (§23.1), since it is the one pilot-dependent number the entire retrieval
leg's validity rests on. No code has been written, no pilot has been run, and no existing file other
than this new document has been modified in producing this review.
