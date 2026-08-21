# E5.2 — Independent Citation & Claim Audit

> Independently re-derived verification pass over `manuscript/main.tex`'s citations and
> literature-facing claims. Formed without reading `research/E5_2_CITATION_CLAIM_AUDIT.md` (the
> primary session's own report) — that document is compared against only in Part 8, after this
> audit's own judgment was fixed. Read-only: no manuscript, `references.bib`, or research file was
> modified by this pass. No new literature source was searched.

---

## Part 1 — Citation inventory (independently grepped)

`grep -oE '\\cite[pt]\{[^}]+\}' manuscript/main.tex` → 14 distinct keys, matched 1:1 against
`references.bib`'s 14 `@`-entries. No orphaned bib entry, no missing key.

| Key | Ledger source | Ledger status | Verdict |
|---|---|---|---|
| `rice1976` | citation_ledger.csv B1-01 | VERIFIED | resolves cleanly |
| `smithmiles2009` | B2-01 | VERIFIED | resolves cleanly |
| `manning2008` | ads_metric_prior_art.csv G1-01 | verified (WebSearch cross-check; no explicit status column in this ledger, but verification narrative present) | resolves cleanly |
| `amigo2009` | G1-02 | verified (get_paper/OpenAlex) | resolves cleanly |
| `dawidskene1979` | G1-04 | verified (Consensus + cross-referenced descendants); DOI/volume/pages not resolved by the ledger itself | resolves, metadata incomplete |
| `barbudo2023` | B2-02 | VERIFIED | resolves cleanly |
| `idreoskraska2019` | B7-01 | VERIFIED | resolves cleanly |
| `frugalgpt2023` | B3-02 | VERIFIED | resolves cleanly |
| `rankgpt2023` | llm_advisory_prior_art.csv G2-01 | verified (FastTrack/OpenAlex + Consensus) | resolves, author list abbreviated |
| `chow1970` | B4-01 | VERIFIED | resolves cleanly |
| `elyaniv2010` | B4-02 | VERIFIED | resolves cleanly |
| `hendrickx2024` | B4-05 | VERIFIED | resolves cleanly |
| `mozannarsontag2020` | B5-02 (also G2-08) | VERIFIED | resolves cleanly |
| `jorgensenigel2021` | B8-01 | VERIFIED | resolves cleanly |

No cited key traces to an UNVERIFIED, UNVERIFIED-PARTIAL, or NOT FOUND row in any of the three
ledgers. `B2-10` (UNVERIFIED-PARTIAL) and the several UNVERIFIED/UNVERIFIED-PARTIAL B3/B6 rows are
correctly excluded from citation — they appear nowhere as `\citep{}`/`\citet{}` keys.

**Note on ledger schema:** `ads_metric_prior_art.csv` and `llm_advisory_prior_art.csv` do not carry
an explicit `Verified`/`VERIFIED-INDUSTRY`/`NOT FOUND` status column the way `citation_ledger.csv`
does — they carry a `VerificationMethod` narrative field instead. I treated a populated, specific
`VerificationMethod` (naming a lookup tool and cross-check) as verification-equivalent. This is a
reasonable reading but is itself an inference, not a literal status-string match — worth the human
author's awareness if a future pass wants a uniform status column across all three ledgers.

---

## Part 2 — Sampled claim-strength check (independent, not primed by the primary report)

Sampled 12 citation-attached sentences (all of §2's Related Work, plus the two §6.5 reuses and the
§3.2 restatement) and compared each against its ledger row's own `WhyRelevant`/description field:

- Cluster purity (`manning2008`,`amigo2009`) "identical closed-form expression as ADS" — ledger
  G1-01/G1-02 both say `EquivalenceToADS = Equivalent`. **FULLY_SUPPORTED.**
- Dawid–Skene lineage majority-vote baseline "is the same quantity under a different name" — ledger
  G1-04 says `Analogous` (not `Equivalent`) for the *model's own* output, but explicitly confirms the
  *naive majority-vote baseline within that literature* is mathematically identical to ADS. The
  manuscript's sentence is carefully scoped to "the raw majority-vote agreement proportion... used
  throughout the crowdsourcing literature," not to Dawid–Skene's own EM estimate — this scoping
  matches the ledger's own nuance exactly. **FULLY_SUPPORTED**, correctly hedged.
- `rice1976`/`smithmiles2009`/`barbudo2023` ASP → meta-learning → AutoML lineage — matches ledger
  B1-01/B2-01/B2-02 verbatim in substance. **FULLY_SUPPORTED.**
- `idreoskraska2019` "opposite temporal structure... explicitly rejecting a one-time, human-gated
  design decision" — matches B7-01 exactly ("continuous, self-adapting design... a different
  evidence type and a one-shot rather than continuously-adapting decision"). **FULLY_SUPPORTED.**
- `chow1970`/`elyaniv2010`/`hendrickx2024` reject-option lineage — matches B4-01/B4-02/B4-05.
  **FULLY_SUPPORTED.**
- `mozannarsontag2020` "trained or rule-based function decides, per item, whether to defer to a
  human, informed by historical decision data" — ledger B5-02 describes a trained end-to-end
  consistent-surrogate-loss defer function; "informed by historical decision data" is a fair gloss on
  "trained" but is the single softest paraphrase found in this sample. **FULLY_SUPPORTED**, borderline
  — not a violation, but the loosest phrasing in the sample.
- `frugalgpt2023` "closest structural match... to a multi-tier, historically-calibrated cascade" —
  matches B3-02 ("composed and tuned... using historical accuracy data"). **FULLY_SUPPORTED.**
- `rankgpt2023` "commodity information-retrieval technique" — matches G2-01 exactly
  ("thoroughly standard IR practice... commodity technique"). **FULLY_SUPPORTED.** However, the
  manuscript's own `% EVIDENCE:` comment beneath this paragraph (main.tex L383–384) cites
  `citation_ledger.csv rows B3-02, B6-02` as the source — B3-02 is FrugalGPT (correct, but already
  cited for the *other* sentence in the same paragraph) and B6-02 is Dekoninck et al.'s LLM-routing
  paper, **not** RankGPT. RankGPT's actual verification lives in `llm_advisory_prior_art.csv` row
  G2-01, which this comment never names. The citation itself is sound and independently verifiable;
  only the internal audit-trail pointer is imprecise. Minor, non-blocking.
- `jorgensenigel2021` cross-company generalization gap — matches B8-01 exactly. **FULLY_SUPPORTED.**

No OVERSTATED or MISATTRIBUTED citation found in this sample.

---

## Part 3 — Novelty guardrail

`grep -in novel manuscript/main.tex` → 6 hits, all negations: "we therefore make no claim that ADS
is a novel metric" (§2.1), "not presented as a novel contribution" (§3.2), "not a new metric...not a
new architecture" (§1.4), "much weaker than any claim of methodological novelty" (§2.4), "not a
methodological novelty claim" (Table 2 row). No positive novelty assertion for ADS, the general
design-time-selection pattern, or the combined system anywhere in the document.

`grep -in "no (prior|comparable|vendor|other)|unprecedented|first (to|paper)"` → 2 hits, both inside
the single sentence "We do not claim that the application domain itself is unprecedented, or that no
vendor measures historical consistency before choosing a mechanism — at least one industry source
directly contradicts that framing" (§2.4, L397–399). This is the forbidden pattern appearing **only**
inside its own negation, exactly as required. **PASS.**

---

## Part 4 — Missing citation check (industry-vendor sources)

Grepped `references.bib` and `main.tex` for "kenfromfinance", "peakflo", "ramp.com", "ken from
finance" — zero matches in either file.

The Related Work §2.4 paragraph makes two specific, attributable claims sourced to ledger rows
B8-04 (Ken From Finance), B8-05 (Peakflo), B8-06 (Ramp) — all three `VERIFIED-INDUSTRY` — via prose
only:

> "Independent industry sources (accounts-payable automation vendors, not peer-reviewed) describe
> similar informal historical-consistency-audit practice already in production use... at least one
> industry source directly contradicts that framing."

None of the three vendors is named, none appears as a `\citep{}`/`\citet{}` key, and none has a
`references.bib` entry — even though `jorgensenigel2021` (B8-01), the fourth source in the same
`% EVIDENCE:` comment block, *is* formally cited two sentences earlier in the same subsection. A
reader cannot identify or independently verify which vendor "directly contradicts" the no-vendor
framing from the text as written, despite the underlying evidence being fully verified and already
sitting in the ledger with URLs and WebFetch-retrieval notes. `PAPER_CONTRACT.md` §2 row 11 lists
these ledger rows among the claims the paper MAY make and requires a not-peer-reviewed label
"wherever cited" — since they are never actually cited, that specific rule is technically
vacuous, but `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §2's own Related Work row explicitly expected this
material to appear "labeled as such in-text," and `PAPER_CONTRACT.md` §11's E3 definition requires
"citations wired in for every Related Work / positioning claim." This is the one substantive,
fixable gap found in this audit — a traceability/completeness gap, not a fabrication, and not an
overclaim (the claim itself is correctly hedged as non-peer-reviewed and does not overstate what the
vendors say).

**Required fix:** add `references.bib` entries for B8-04/B8-05/B8-06 (all three already have URLs
and retrieval notes in `citation_ledger.csv` — no new search needed) and cite at least B8-04 by name
at "at least one industry source directly contradicts that framing."

No other missing-citation gap was found. Background ledger rows named only in `% EVIDENCE:` comments
(B1-02..B1-05, B2-10, B2-11, etc.) are corroborating context for claims already covered by a
formally-cited key in the visible prose (`rice1976`/`smithmiles2009`), so their absence from in-text
citation is expected, not a gap.

---

## Part 5 — Contribution-lock compliance

- **H1 status:** `grep -in "PARTIALLY.SUPPORTED"` → 7 hits, all "PARTIALLY SUPPORTED" / "partially
  supported," none upgraded to unqualified "SUPPORTED." §7.1 is titled "H1 Only Partially Supported."
  **Intact.**
- **6a/6b split:** never merged into one sentence. §5.2 ("ADS Predicts Individual Mechanism
  Accuracy") and §5.3 ("ADS Does Not Predict Mechanism Ranking") are kept as separate subsections
  throughout, with an explicit sentence in §3.4 stating "these are two different claims, with
  different (here, opposite) truth values, and this paper never merges them." Abstract and §1.4 both
  state both halves side by side without collapsing them. **Intact.**
- **C1 (ADS novelty) rejected throughout:** confirmed via Part 3 above. **Intact.**
- **Forbidden-claim grep sweep** (against `PAPER_CONTRACT.md` §3's 16-row list): searched for
  "typically ship"/"chosen up front" (item 14), "validated as effective"/"hybrid
  classification-system composition" (item 16), "55,394"/"55394" (item 15), "enterprise AI" (item 6),
  "we prove"/"demonstrates causally"/"proves that" (item 6-style causal overclaim) — **zero matches**
  for all of these in `main.tex`. Superseded numeric values (weighted ADS 0.8094, unweighted 0.9310,
  84.12%/84.1%) also produce **zero matches** — the manuscript correctly uses the canonical
  post-A5-fix synthetic figure (87.56%) at the one place a synthetic deterministic-share number
  appears (§1.1). Production figures (91.2%, 0.847, 0.964, 0.695, 76,843-equivalent) all match
  `PAPER_CONTRACT.md` §7's canonical table and each carries the confidential/cited-not-reproduced
  qualifier at every appearance checked. **No rejected claim has reappeared.**

One incidental observation, not a manuscript defect: `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §1's own
Introduction table still describes the motivating synthetic figure as "84.1%" (the pre-A5-fix, now-
superseded value) — the manuscript itself does not inherit this stale number (it correctly uses
87.56%), so this is a staleness note about a supporting document, not about `main.tex`.

---

## Part 6 — Bibliography integrity

14 `\citep{}`/`\citet{}` keys, 14 `references.bib` entries, exact 1:1 match — no orphan, no unused
entry, no missing entry.

Exactly one entry (`dawidskene1979`) carries explicit `TODO` field values (`volume`, `number`,
`pages`, `doi`) — traced to `ads_metric_prior_art.csv` row G1-04, which itself only records "(2069
citations per Consensus; no DOI independently resolved in this pass)" with no volume/pages recorded
either. The gap is genuinely unresolvable from the ledger as it stands; the in-file comment
correctly says "verify before E5, do not guess" rather than fabricating a value.

A second, softer placeholder: `rankgpt2023`'s author field is abbreviated (`Sun and Yan and Ma and
others`), matching `llm_advisory_prior_art.csv` G2-01's own abbreviation ("Sun, Yan, Ma, et al.") —
also not independently resolved by the ledger, also honestly flagged in-file ("expand before E5").

Both gaps are legitimately unresolvable from currently-verified sources under this session's
no-new-search constraint, and both are honestly marked rather than guessed — no fabricated or
silently-invented metadata found anywhere in `references.bib`. (Independent observation, not
actioned: both the Dawid & Skene 1979 DOI, 10.2307/2346806, and RankGPT's full 8-author list are
in fact well-known/easily locatable facts — but resolving them would require a lookup this session's
brief does not authorize, so I record this only as a candidate for a future metadata pass, not as a
finding against this pass.)

---

## Part 7 — Findings summary

1. **[REQUIRED FIX, CONDITIONAL-level]** Industry-vendor sources B8-04 (Ken From Finance), B8-05
   (Peakflo), B8-06 (Ramp) are described only in anonymous prose in §2.4 and are never formally
   cited (no `\citep{}`, no `references.bib` entry), despite being `VERIFIED-INDUSTRY` and despite
   substantiating a specific, falsifiable claim ("at least one industry source directly contradicts
   that framing") that a reader cannot trace without leaving the paper. Fixable entirely from
   already-verified ledger data; no new literature search required.
2. **[OPTIONAL / minor]** The `% EVIDENCE:` comment for the FrugalGPT/RankGPT paragraph (main.tex
   L383–384) points to `citation_ledger.csv` rows B3-02 and B6-02; B6-02 is a different paper
   (Dekoninck et al.) and does not verify `rankgpt2023` — the real verification source is
   `llm_advisory_prior_art.csv` row G2-01, uncited in that comment. The citation itself remains
   valid and independently verifiable; this is an internal audit-trail imprecision, not a citation
   defect.
3. **[OPTIONAL / pre-existing, not new drift]** Two bibliography metadata TODOs
   (`dawidskene1979` volume/number/pages/DOI; `rankgpt2023` full author list), both honestly
   documented as unresolved by the ledger, both legitimately out of scope for a no-new-search
   verification pass.
4. No forbidden claim, no resurrected rejected claim, no overstated or misattributed citation, no
   fabricated or orphaned bibliography entry, no novelty-guardrail violation, and no
   contribution-lock drift found anywhere else in the document.

---

## Part 8 — Comparison against the primary session's report

Read `research/E5_2_CITATION_CLAIM_AUDIT.md` only after the above was fixed. The two audits agree on
every substantive point:

- Same citation count (14/14, exact 1:1 match, no orphans).
- Same "no MISATTRIBUTED/OVERSTATED citation found" conclusion, on an overlapping but not identical
  sample (the primary report covers all 14 keys individually in its Part 1/Part 8 matrix; this audit
  sampled 12 with a slightly different lens, converging on the same verdicts for every overlapping
  key, including the same soft-spot flag pattern — this audit flagged `mozannarsontag2020`'s
  "informed by historical decision data" phrasing as the loosest paraphrase in its sample; the
  primary report did not flag this specific phrase but reached the same overall FULLY_SUPPORTED
  verdict for that citation).
- **Identical primary finding**: both audits independently identified the same GAP-01 — B8-04/05/06
  described in prose but never formally cited — as the single most actionable, load-bearing finding,
  down to citing the same manuscript line range (§2.4, L394–402) and the same required fix (add
  `references.bib` entries + `\citep{}` for at least B8-04). This is strong independent convergence:
  two separate reads of the same primary sources reached the identical conclusion about the same gap.
- Same two bibliography TODOs identified (`dawidskene1979` metadata, `rankgpt2023` author list),
  same "honestly documented, not fabricated, still open" characterization.
- Same novelty-guardrail and contribution-lock PASS conclusions.

**One disagreement in emphasis, not substance:** the primary report labels GAP-01
"REQUIRED_ACTION, not blocking" without committing to one of this task's four verdict tiers
explicitly. This audit treats the same finding as sufficient on its own to keep the overall verdict
at CONDITIONAL/ORANGE rather than PASS/GREEN, since `PAPER_CONTRACT.md`'s own E3 definition (§11)
requires citations to be "wired in for every Related Work / positioning claim" and this is the one
place in the document where that requirement is not met for a claim the paper actively relies on to
rebut a named forbidden framing (item 14 of the paper's own rejected-claims list). This is a framing
difference in how strictly to read "not blocking," not a factual disagreement about what was found.

**One additional finding in this audit not present in the primary report:** the imprecise
`% EVIDENCE:` pointer for the RankGPT citation (Part 2/Part 7 item 2 above). This does not change
either report's overall conclusion — the citation itself is sound in both audits' assessment.

---

## Verdict

**ORANGE (CONDITIONAL).**

Justification: the citation and bibliography infrastructure is sound — every cited key resolves to a
verified source, no rejected claim has resurfaced, the novelty guardrail and the 6a/6b
accuracy-vs-ranking split are both intact, and no number in the manuscript is stale or fabricated.
The one finding that keeps this from a clean PASS is concrete and specific, not an integrity
violation: three `VERIFIED-INDUSTRY` sources central to the Related Work section's domain-practice
paragraph and to rebutting one of the paper's own explicitly-named forbidden claims ("no vendor
measures historical consistency") are used substantively in prose without ever being formally cited,
leaving a reader unable to verify which vendor is meant. This is fixable entirely from
already-verified ledger data (no new literature search needed) and should be resolved — along with,
optionally, the two pre-existing bibliography metadata TODOs and the one imprecise `% EVIDENCE:`
pointer — before this citation pass is considered closed.
