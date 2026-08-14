# E5.2 — Correction Pass Audit

> Bounded correction pass for E5.2's one required finding. No new literature search performed. No
> scientific claim, number, frozen evidence, or contract/lock document touched. Not yet committed —
> this is the pre-commit evidence trail for that decision.

---

## 1. Original E5.2 finding

`research/E5_2_CITATION_CLAIM_AUDIT.md` (primary pass) and `research/E5_2_INDEPENDENT_CITATION_AUDIT.md`
(independent `research-code-auditor` pass, verdict 🟠 ORANGE/CONDITIONAL) both converged on the same
finding: manuscript §2.4 ("Domain-Specific Practice") describes three VERIFIED-INDUSTRY sources
(B8-04 Ken From Finance, B8-05 Peakflo, B8-06 Ramp) in prose — including making the specific,
falsifiable claim "at least one industry source directly contradicts that framing" (rebutting the
`CONTRIBUTION_LOCK.md` §7 forbidden claim "no vendor measures historical consistency") — without a
formal `\citep{}` or a `references.bib` entry for any of the three. `jorgensenigel2021` (B8-01), cited
two sentences earlier in the same subsection, made the omission visible by contrast.

## 2. Exact bounded changes made

- **`manuscript/references.bib`**: added three `@misc` entries — `kenfromfinance2025`,
  `peakflo2025`, `ramp2025` — after `jorgensenigel2021`, with a one-line comment noting they were
  added at E5.2's correction pass from ledger data only, no new search.
- **`manuscript/main.tex`** §2.4 (two sentences, +2 citation insertions, +1 four-word inline
  qualifier, no sentence rewritten):
  - "Independent industry sources (accounts-payable automation vendors, not peer-reviewed)
    `\citep{kenfromfinance2025,peakflo2025,ramp2025}` describe similar informal
    historical-consistency-audit practice already in production use."
  - "...at least one industry source `\citep{kenfromfinance2025}` (not peer-reviewed) directly
    contradicts that framing..."
- **`manuscript/main.tex`** §2.3, RankGPT `% EVIDENCE:` comment (internal, non-reader-visible):
  replaced the incorrect pointer `citation_ledger.csv rows B3-02, B6-02` (B6-02 is Dekoninck et al.'s
  unified routing/cascading paper — a different source, not cited in that sentence) with the correct
  pointer: `citation_ledger.csv row B3-02` (FrugalGPT, correct) + `llm_advisory_prior_art.csv row
  G2-01` (RankGPT, correct), with a note explaining the correction.

**Total diff**: `manuscript/main.tex` 11 lines changed (7 insertions, 4 deletions — all within the two
`% EVIDENCE:`/prose regions above); `manuscript/references.bib` 34 lines added (3 new entries + 1
section comment), 0 deleted. No other file touched.

## 3. Source-to-bibliography mapping

| Ledger row | Bib key | Title (verbatim from ledger) | Author (verbatim) | Year (ledger) | URL (verbatim) | DOI |
|---|---|---|---|---|---|---|
| B8-04 | `kenfromfinance2025` | Invoice GL Coding Automation: Workflow & Controls | Ken From Finance | undated (~2025) → recorded as 2025 + note | `https://www.kenfromfinance.com/blog/invoice-gl-coding-automation` | none (industry source) |
| B8-05 | `peakflo2025` | How to Automate GL Coding for Non-PO Invoices | Peakflo | undated (~2025) → recorded as 2025 + note | `https://peakflo.co/blog/gl-coding-automation-non-po-invoices` | none |
| B8-06 | `ramp2025` | What Are the Best Practices for Using AI Agents in AP? | Ramp | 2025-11-03 → recorded as 2025 + exact-date note | `https://ramp.com/blog/agentic-ai/best-practices-for-ap-agents` | none |

Every field traces directly to `research/literature/citation_ledger.csv` rows 55–57, verified
character-for-character by direct read before writing the `.bib` entries. No field was invented,
guessed, or sourced outside that ledger.

## 4. Source-to-citation mapping (why each citation lands where it does)

- **All three (`kenfromfinance2025,peakflo2025,ramp2025`)** at the general "similar informal
  historical-consistency-audit practice already in production use" sentence — this is the sentence
  the section's own pre-existing `% EVIDENCE:` comment already grouped all three sources under.
- **`kenfromfinance2025` alone** at "at least one industry source... directly contradicts that
  framing" — checked individually against each source's `WhyRelevant` ledger field: only B8-04
  explicitly "recommends... a historical-consistency check before deployment," the specific claim
  that contradicts the forbidden "no vendor measures consistency" framing. B8-05's own ledger entry
  states explicitly "no pre-deployment historical-determinism measurement"; B8-06's states its
  baseline is "operational..., not a label-consistency metric." Citing only B8-04 here — not all
  three — is the more precise, ledger-faithful choice, not a broader claim than the evidence supports.

## 5. Industry-source qualification verification

`PAPER_CONTRACT.md` §2 row 11 (read directly before editing): *"Industry-source rows (B8-04/05/06)
must be labeled as not peer-reviewed wherever cited."* Both citation points carry this label: the
first inherits the sentence's existing "(accounts-payable automation vendors, not peer-reviewed)"
parenthetical, now sitting immediately before the three new `\citep{}` keys; the second sentence
received its own explicit "(not peer-reviewed)" insertion next to `\citep{kenfromfinance2025}`, since
that citation is a standalone, individually-attributable claim a reader could otherwise mistake for
peer-reviewed. Each new `references.bib` entry's `note` field also states "Industry source, not
peer-reviewed" independently, so the qualification is present at three independent points (bib entry,
first in-text citation, second in-text citation) — exceeds, not merely meets, the "wherever cited" bar.

## 6. RankGPT provenance correction

Confirmed via direct read of `research/literature/llm_advisory_prior_art.csv` row G2-01 that RankGPT's
actual verified source is that file, not `citation_ledger.csv` row B6-02 (which is a different paper —
Dekoninck, Baader & Vechev's unified LLM routing/cascading work). The manuscript's visible `\citep{}`
for RankGPT (line 374) was always correctly wired to the `rankgpt2023` `references.bib` entry, which
itself has always correctly cited `llm_advisory_prior_art.csv` row G2-01 in its own file header
comment — **the defect was confined to one internal, non-reader-visible `% EVIDENCE:` audit-trail
comment** in `main.tex`, not the citation itself. Corrected as described in §2 above; no reader-facing
text changed.

## 7. Bibliography integrity

- **Citation keys ↔ bib entries**: 17 distinct `\cite[pt]{}` keys in `main.tex` (re-grepped fresh
  post-edit) match exactly the 17 `@`-entries in `references.bib` (also re-grepped fresh) — 1:1, no
  gaps, no orphans in either direction.
- **No entry unused, no entry fabricated**: every one of the 17 entries traces to a VERIFIED /
  VERIFIED-INDUSTRY row in `citation_ledger.csv` or the two literature gap-verification CSVs.
- **No existing citation disturbed**: the diff (§2 above) touches only the three added `\citep{}`
  insertions and the one internal comment; the other 14 pre-existing citation instances are
  byte-identical in the diff (confirmed — no other line in the diff hunk touches them).

## 8. Claim-safety verification

Grepped the post-edit `manuscript/main.tex` for the checklist terms:
- `B8-04/05/06 topic (GL coding, AP automation)` — appears only inside the two edited sentences,
  unchanged in substance, now cited.
- `RankGPT` — one occurrence (line 374), citation unchanged; the correction was to a comment only.
- `EMBEDDING_PRIMARY` — one occurrence (line 104, Introduction), untouched, unchanged from the
  E4.1-fixed wording.
- `novel` — 7 occurrences, all still negations ("make no claim... is a novel metric," "not presented
  as a novel contribution," etc.) — no positive novelty claim reappeared.
- `no vendor` — 1 occurrence (line 400), same sentence as before, still correctly negated ("We do not
  claim... that no vendor measures historical consistency... at least one industry source... directly
  contradicts that framing") — now with the contradicting source actually named and cited.
- **H1**: still stated `PARTIALLY\_SUPPORTED` at both prior locations (Limitations §7.1 heading and
  body) — byte-identical, outside the diff.
- **Formulation #2 / 6a / 6b**: byte-identical, outside the diff — Results (§5, untouched since E5.1)
  and Discussion (§6, untouched since E5.1) carry zero lines in this pass's diff.
- **Protected numbers**: none of 32/32, 0/18, 30/30, 2/20, 32/50=64.0%, the Wilson CI, either p-value,
  either Pearson-r range, δ=0.02, cutoff=75, or P_TRANSFORM=0.3 appear anywhere in this diff — the
  edited region (§2.3–2.4, Related Work) contains no experimental statistics.

## 9. Protected/frozen-file verification

`git diff --quiet` (exit 0 = unchanged) confirmed for: `research/PAPER_CONTRACT.md`,
`research/CONTRIBUTION_LOCK.md`, `research/contribution_lock.csv`, and everything under
`data/outputs/experiments/exp1/final/`. `git status --porcelain` confirms only `manuscript/main.tex`
and `manuscript/references.bib` are modified; no other file entered the working tree as
modified/staged (six pre-existing/this-session untracked audit-report files remain untracked, listed
in §12 below, none touched).

## 10. Tests

`python -m pytest scripts/experiments/exp1/ -q` → **30 passed**, unchanged from every prior checkpoint
this phase (expected — no code was touched).

## 11. Auditor verdict

🟢 **PASS** (`research/E5_2_CORRECTION_INDEPENDENT_AUDIT.md`). Independently re-verified every
bibliography field against the ledger, confirmed the `kenfromfinance2025`-alone placement at the
"directly contradicts" sentence is the more precise choice (by individually checking each source's
`WhyRelevant` field), confirmed the peer-review qualification is satisfied at both citation points,
confirmed the RankGPT fix is genuinely comment-only and the visible citation was never wrong,
confirmed the scope boundary holds (zero diff on `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`,
`contribution_lock.csv`, frozen evidence), re-derived the 17-key citation/bibliography match
independently, reconfirmed the novelty guardrail, re-ran the test suite (30/30), and found no
secrets/paths in either modified file. One non-blocking precision note: the joint three-source
citation at the general "historical-consistency-audit practice" sentence is slightly broader than
`peakflo2025`'s own ledger entry individually supports (B8-05 explicitly disclaims historical-
determinism measurement) — flagged as optional future refinement, not a defect requiring a fix before
commit.

## 12. Exact proposed staging list (not yet staged)

```
manuscript/main.tex
manuscript/references.bib
research/E5_2_CORRECTION_AUDIT.md
```

Untracked, not part of this proposed staging list (pre-existing or this session's earlier audit
trail, unrelated to this specific correction):
```
research/E4_CHECKPOINT_FINAL_STAGING_AUDIT.md
research/E4_CHECKPOINT_MANIFEST_VERIFICATION.md
research/E5_1_E5_2_GPS_CLOSEOUT_AUDIT.md
research/E5_1_GPS_FINAL_PRECOMMIT_AUDIT.md
research/E5_2_CITATION_CLAIM_AUDIT.md
research/E5_2_INDEPENDENT_CITATION_AUDIT.md
research/E5_GPS_HOUSEKEEPING_AUDIT.md
```
