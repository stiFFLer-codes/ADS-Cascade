# Manuscript Update Queue

> Output of the Final Phase-A Evidence Closure Audit (2026-08-11). `TECHNICAL_REPORT.md` was **not
> edited** in this pass — this document is the punch list for the manuscript-rewrite phase (Phase
> E). Every item traces to a row in `research/final_numbers_audit.csv`. Items are split into
> **NUMERIC UPDATE** (a value changes, the claim's shape doesn't) and **INTERPRETATION UPDATE** (the
> prose's *meaning* needs to change, not just a digit) — some items are both.

---

## NUMERIC UPDATES

### N1. §3.2 table — synthetic ADS figures (F27, F28, F39)

| | Current manuscript value | Canonical value | Source |
|---|---|---|---|
| Weighted ADS (synthetic) | 0.809 | **0.903** | `research/EVIDENCE_BASELINE.md` §2 |
| Unweighted ADS (synthetic) | 0.931 | **0.960** | Same |
| Products >0.95 deterministic (synthetic) | 84.1% | **87.6%** | Same |

**Why it changed:** A5 bug fix in `scripts/03_5_dataset_intelligence.py` (dominant-account
selection now correctly sums by account before comparing). See
`research/a5_correction_analysis.md`.

**Also touches:** §3.3's restated "84.1%" (F39, same underlying number, different sentence) and the
R3 table row (see N2, same root cause).

**Interpretation rewrite needed?** No — see Note under N2/I1 below; the *qualitative* story (R3
flips, weighted<unweighted) is unchanged, only the digits.

### N2. §3.2 table — R3 synthetic row percentage (F34)

Current: `EMBEDDING_PRIMARY (84.1% < 90%)` → Canonical: `EMBEDDING_PRIMARY (87.6% < 90%)`.
Decision label itself (EMBEDDING_PRIMARY) is unchanged and correct — only the cited percentage is
stale. Margin from the 90% boundary narrows from 5.9 points to 2.4 points; §3.3's "close decision"
framing is if anything *strengthened* by the corrected number, not weakened.

### N3. §2.4 — T2 cascade threshold value (F19)

Current: "a weaker company rule (0.80–0.95 ADS)" → Actual code value: **0.90–0.95 ADS**
(`T2_ADS_LOW = 0.90` in `scripts/phase2/p2lib/confidence.py`). This is not simply a typo to fix —
see **I2** below; the whole T2 sentence needs a structural rewrite, not just a digit swap.

---

## INTERPRETATION UPDATES

### I1. §2.2 / §3.2 / §3.3 — the ADS-divergence magnitude, synthetic branch (F27, F28, F39)

This is the case flagged explicitly by this task's brief: A5 changed not just a number but
arguably the *strength* of the divergence claim as measured on synthetic data.

- **Before:** synthetic weighted/unweighted gap = 0.9310 − 0.8094 = **0.1216**.
- **After:** synthetic weighted/unweighted gap = 0.9597 − 0.9031 = **0.0566** — roughly half.

`04_architecture_decision.py`'s own `>0.1` "ADS Divergence Warning" no longer fires on the
corrected synthetic run (it did on the pre-fix run). **What this does *not* change:** the
*production* divergence claim in §2.2 (0.964 vs. 0.847, gap 0.117) is untouched — production data
was never re-run in this repository (see F10's caveat). §2.2's headline claim is about production,
not synthetic, so its own wording does not need to change. What *does* need rewriting is §3.2's
framing of the synthetic column as corroborating evidence for the *magnitude* of the divergence —
post-fix, the synthetic run corroborates the *direction* (weighted < unweighted) much more weakly
than it did pre-fix. If §3.2's surrounding prose currently implies the synthetic gap supports the
production gap's size, that implication should be softened or removed. **Recommendation:** when
rewriting §3.2, state plainly that the synthetic gap (0.057) is smaller than the production gap
(0.117) and both are directionally consistent, rather than letting a reader assume they're
comparable in magnitude.

### I2. §2.4 — the T2 tier no longer auto-applies fuzzy matches at all (F19, F20)

This is the single most consequential finding of this closure pass, and it is a **structural**
claim, not a digit.

**Current manuscript text (§2.4 table, T2 row):**
> "Fuzzy/embedding match (similarity ≥ 0.85) or a weaker company rule (0.80–0.95 ADS) corroborated
> by VAT | Auto-apply, flagged for a sampled spot-check"

**What the shipped code (`scripts/phase2/p2lib/confidence.py` + `cascade.py`) actually does:**
- The company-rule mid-tier ADS floor is **0.90**, not 0.80 (`T2_ADS_LOW = 0.90`).
- `FUZZY_AUTO_APPLY = False` is a hardcoded constant. The fuzzy-similarity auto-apply branch in
  `cascade.py` (`if C.FUZZY_AUTO_APPLY: ...`) is **dead code** — it can never execute. Every fuzzy
  match, regardless of similarity score, currently falls through to `FUZZY_REVIEW` at **Tier 3**,
  never Tier 2.

**Why this happened (traceable, not mysterious):** code comments in `confidence.py` explain the
Stage-A held-out eval measured the original 0.80-ADS-floor rules at ~45% accuracy and fuzzy
auto-apply (even with top-3 agreement) at ~49% — both judged unsafe — so the implementation was
tightened *after* `architecture/08_CONFIDENCE_CASCADE.md` (which specifies the same 0.80/fuzzy-auto
design the manuscript describes) was written. `STATE.md`'s own Phase 2 notes already record this
recalibration ("fuzzy is demoted to review (never auto-applied)") — it was simply never
back-ported into `TECHNICAL_REPORT.md` §2.4 or `architecture/08_CONFIDENCE_CASCADE.md`.

**What needs to change in the manuscript:** the T2 row needs to state that T2 is now reached
*only* via the company-rule mid-tier path (0.90–0.95 ADS, ≥5 evidence) or the global-pattern
mid-tier path (0.85–0.98 global ADS, ≥5 companies) — **not** via fuzzy/embedding similarity, which
now always routes to human review (T3) regardless of score. This also means the T3 row's "Similarity
< 0.85" framing is imprecise — as implemented, *all* fuzzy matches land at T3, not just those below
0.85 similarity.

**Not a code bug** — the code is internally consistent and intentional (it's a deliberate safety
tightening, well-commented). This is purely a documentation-lag finding. **Not fixed here** — per
this task's explicit "do not modify methodology or code" constraint. Flagged for the author to
decide: update the manuscript+architecture-doc to match the safer shipped behavior, or reconsider
re-enabling `FUZZY_AUTO_APPLY` if the underlying accuracy has since improved. Either way, the
current manuscript text is stale and should not be published as-is.

### I3. §2.3 — R3's incomplete threshold description (F13; carried forward from finding A4)

Not new to this pass — already documented in `research/r3_threshold_analysis.md` and Recommendation
E4 of `research/RESEARCH_AUDIT.md`. Restated here so it appears on the same consolidated punch
list: §2.3 states only the ≥90% RULES_FIRST cutoff and omits the code's second band
(EMBEDDING_PRIMARY, 0.70–0.90) and third band (LLM_REQUIRED, <0.70, never empirically triggered).
Recommend the manuscript name all three bands explicitly, since Band 2 is not hypothetical — it's
exactly where the synthetic run lands.

### I4. §3.2 table — Purchase/sale split compares different units (F31)

Current table row cites production 73.9%/26.1% against synthetic 73.5%/26.5% in the same row. The
production figure is computed at the **invoice** level (`phase1_final_report.md` §1 Executive
Summary: 79,616/28,127 invoices); the synthetic figure is computed at the **line** level
(`dataset_statistics.csv`: 5,533/1,990 lines). The true line-level production split, stated
elsewhere in the same source document, is **73.7%/26.3%** — closer to, but still not identical to,
the synthetic figure. Values are close enough (~0.2 percentage points) that this is a low-severity,
cosmetic-precision issue, not a materially wrong claim — but the table implicitly presents both
columns as the same measurement, which they are not. **Recommendation:** either swap the production
cell to the line-level figure (73.7%/26.3%) for a true apples-to-apples comparison, or add a
footnote noting the production figure is invoice-level.

### I5. §4 — unsupported/self-contradictory multi-seed claim (F42, F43)

**Current text:** "Cross-company consistency has a real, measured ceiling (0.695 in production;
0.76–0.80 across synthetic seeds)."

No script, output file, or record of any kind exists anywhere in this repository's current state
or git history that produces a *range* of cross-company-consistency values across multiple seeds.
Only one synthetic run has ever been executed here (`random.seed(42)`), producing exactly **0.7632**
— a single point, not a range. This directly contradicts the **same section's own later bullet**:
"Single-seed synthetic run... was not swept to produce confidence intervals." This is an internal
self-contradiction within §4, not merely an unverifiable aside.

**Recommendation:** either (a) actually run the generator across a small sweep of seeds and report
the true range (this would satisfy Phase D's "minimal reproducible validation" goal too, and is
explicitly in scope for that phase, not this one), or (b) if no such sweep was ever run, replace
"0.76–0.80 across synthetic seeds" with the single reproducible value, 0.763, and remove the
implied range entirely. **Do not publish the current sentence as-is** — it is not supported by
anything in this repository.

### I6. §6 Conclusion — unsupported "under 10% of production volume" claim (F45)

**Current text:** "the LLM's job shrinks to re-ranking retrieved candidates for a measured minority
tail (under 10% of production volume)."

No artifact in this repository states an LLM-share-of-*volume* (occurrence-weighted) figure. The
closest real number is 100% − 91.2% = 8.8% **non-deterministic products** — a product-*count*
statistic, not a volume statistic. Given §2.2's own explicit point that weighted and unweighted
figures diverge substantially in this dataset (0.847 vs. 0.964, a gap of 0.117 — i.e., the
high-volume products are disproportionately the *harder* ones), asserting a volume-weighted "under
10%" figure without a distinct weighted computation is exactly the conflation §2.2 warns readers
against. This is not proven numerically wrong (no artifact exists to check it against either way) —
it is **unsupported**, and its plausibility is actually undercut by the paper's own argument
elsewhere.

**Recommendation:** either compute and cite an actual occurrence-weighted LLM-touch-rate from
production data (author-only, confidential), or soften the claim to what's actually measured —
"under 10% of the product catalog" (product-count framing, which IS supported) rather than
"production volume" (which implies occurrence-weighting and is not supported).

---

## Items considered and explicitly NOT queued

- **F10/F11 production ADS figures** (0.847/0.964/91.2%) — flagged "likely understated, unverified"
  in `EVIDENCE_BASELINE.md`, not "wrong." No queue item until the author re-runs production data
  through the corrected code; premature to change manuscript numbers based on an unverified
  hypothesis.
- **F23 (63,048 test-line arithmetic)** — flagged UNRESOLVED (minor) in
  `research/final_numbers_audit.csv`; not queued as a manuscript change because the number itself
  is not contradicted by anything in this repo, only insufficiently documented. Not urgent.
- **F30 (kb_summary.json's 96.4% orphan metric)** — not cited anywhere in `TECHNICAL_REPORT.md`, so
  there is nothing to update in the manuscript. Addressed instead as an `EVIDENCE_BASELINE.md`
  completeness gap (see `research/PHASE_A_CLOSURE.md`).
