# E5.2 Correction Pass — Independent Audit

> Independent, read-only verification of the E5.2 correction pass described in
> `research/E5_2_CORRECTION_AUDIT.md`. All findings below were derived from primary sources
> (`git diff`, `citation_ledger.csv`, `llm_advisory_prior_art.csv`, `PAPER_CONTRACT.md`) before
> that report was read. Nothing in this repository was modified, staged, or committed while
> producing this audit.

---

## 1. Repository state

- Branch: `main`. HEAD: `bf3b07f` ("Phase E5.1 GPS closeout: E5.1 complete, E5.2 audit complete,
  E5.3 next"). Working tree: two tracked files modified (`manuscript/main.tex`,
  `manuscript/references.bib`), plus eight untracked audit-report `.md` files under `research/`
  (none of which are part of the correction diff itself). Nothing staged.
- Diffed: `git diff -- manuscript/main.tex manuscript/references.bib` in full (reproduced and
  read in this session, not summarized from the builder's report).

## 2. Bibliography field accuracy (Task item 1) — VERIFIED, no discrepancy

Read `citation_ledger.csv` rows B8-04/05/06 (lines 55–57) directly and compared field-by-field
against the three new `references.bib` entries:

| Field | Ledger (B8-04/05/06) | `references.bib` | Match |
|---|---|---|---|
| Titles | "Invoice GL Coding Automation: Workflow & Controls" / "How to Automate GL Coding for Non-PO Invoices" / "What Are the Best Practices for Using AI Agents in AP?" | Identical (minus the ledger's parenthetical source-type suffix, which is metadata, not title text) | Yes |
| Authors | Ken From Finance / Peakflo / Ramp | Identical | Yes |
| Year | "undated (~2025)" / "undated (~2025)" / "2025-11-03" | `2025` for all three, with `note` fields recording the ledger's exact date precision (Ramp's note explicitly states "published 2025-11-03") | Yes — BibTeX requires a single `year` field; the imprecision is disclosed in `note`, not hidden |
| URL | Verbatim URLs given | Byte-identical | Yes |
| DOI | None (all three) | No `doi` field on any of the three | Yes |
| Verified status | `VERIFIED-INDUSTRY` (all three) | Each entry's `note` states "Industry source, not peer-reviewed... Ledger row: ... B8-0X" | Yes |

No field was invented, upgraded, or altered from what the ledger states. This matches the
builder's own §3 table exactly.

## 3. Citation placement correctness (Task item 2) — VERIFIED for the "contradicts" sentence; one open precision note for the joint citation

Read each row's `WhyRelevant` field directly:

- **B8-04 (Ken From Finance)**: "Independently recommends almost the SAME two-part shape as
  ADS-Cascade (historical-consistency check before deployment + confidence-tiered runtime
  cascade)..." — this is the only one of the three that actually describes a **pre-deployment
  historical-consistency check**.
- **B8-05 (Peakflo)**: "...no pre-deployment historical-determinism measurement driving an
  architecture choice..." — explicitly disclaims the historical-consistency-audit behavior.
  Confirms only the confidence-tiered auto-approve/review half.
- **B8-06 (Ramp)**: "...'baseline' here is operational (time, exception counts), not a
  label-consistency metric." — explicitly disclaims a label-consistency historical audit; confirms
  only a generic pre-deployment baseline-measurement practice.

**Point 2 of the task (the "contradicts" sentence)**: citing `kenfromfinance2025` alone at "at
least one industry source \citep{kenfromfinance2025} (not peer-reviewed) directly contradicts that
framing" is the correct, ledger-faithful choice — it is the only one of the three whose own
`WhyRelevant` field supports the specific claim being made (a vendor measuring historical
consistency before choosing a mechanism). Confirmed independently, matches the builder's §4 claim.

**Point 1 (the joint citation)**: "Independent industry sources... \citep{kenfromfinance2025,
peakflo2025,ramp2025} describe similar informal historical-consistency-audit practice already in
production use." Only B8-04 (and arguably, loosely, B8-06's operational baseline) actually
supports a "historical-consistency-audit" characterization; B8-05's ledger entry explicitly states
it has *no* pre-deployment historical-determinism measurement — it only confirms the
confidence-tiered-cascade half of the practice, not the historical-audit half. Attaching a formal
`\citep{}` to B8-05 at a sentence specifically about "historical-consistency-audit practice" is a
mild precision overreach relative to what that source's own ledger entry says it supports. This is
not a fabrication (the sentence's wording was not changed by this pass — it already existed
uncited and unmodified before E5.2; the correction pass's job was only to attach citations to
existing prose, not to re-litigate that prose's precision) and it does not resurrect any
`PAPER_CONTRACT.md` §3 forbidden claim. It is a legitimate but non-blocking finding: the joint
citation is defensible as "these three sources jointly establish a category of informal
pre-deployment/confidence-gated practice in this vendor space" (a looser reading "historical
consistency" can support), but a more surgical citation would be `\citep{kenfromfinance2025,
ramp2025}` for the historical-baseline half and a separate mention of B8-05 for the confidence-tier
half. Flagged as OPTIONAL FUTURE WORK, not a blocker, since it doesn't misstate any field and
doesn't cross a `PAPER_CONTRACT.md` §3 line.

## 4. Peer-review qualification (Task item 3) — VERIFIED, satisfied at both points and in the bib

`PAPER_CONTRACT.md` §2 row 11 (read directly, line 42): "Industry-source rows (B8-04/05/06) must
be labeled as not peer-reviewed wherever cited." Checked both in-text citation points in the
current `main.tex`:

- First citation (`kenfromfinance2025,peakflo2025,ramp2025`) sits directly after the sentence's
  pre-existing "(accounts-payable automation vendors, not peer-reviewed)" parenthetical — label is
  present at this citation point.
- Second citation (`kenfromfinance2025` alone) received its own explicit "(not peer-reviewed)"
  qualifier inline, immediately after the `\citep{}` — label is present at this citation point too.
- Each `references.bib` entry's `note` field independently states "Industry source, not
  peer-reviewed" as well.

Requirement satisfied at both manuscript citation points, confirmed by direct reading of the
current file, not by trusting the builder's assertion.

## 5. RankGPT provenance fix (Task item 4) — VERIFIED correct and comment-only

- `llm_advisory_prior_art.csv` row G2-01 (read directly, line 2) is "Is ChatGPT Good at Search?
  Investigating Large Language Models as Re-Ranking Agents" (Sun, Yan, Ma, et al., EMNLP 2023,
  DOI `10.18653/v1/2023.emnlp-main.923`) — this is in fact RankGPT, the paper the manuscript's
  `\citep{rankgpt2023}` (line 374) is about (LLM re-ranking a pre-fetched candidate list).
- `citation_ledger.csv` row B6-02 (read directly, line 48) is "A Unified Approach to Routing and
  Cascading for LLMs" (Dekoninck, Baader, Vechev, 2024, arXiv) — a genuinely different paper, about
  unifying LLM routing/cascading across model sizes, not re-ranking. Confirmed unrelated to
  RankGPT.
- The old `% EVIDENCE:` comment cited `B3-02, B6-02` (FrugalGPT + the wrong Dekoninck paper) for a
  sentence that discusses both FrugalGPT and RankGPT — B6-02 was indeed a misattribution for the
  RankGPT half.
- `references.bib`'s `rankgpt2023` entry (lines 96–103) was already correctly populated with Sun et
  al.'s title/venue/DOI before this pass, and its own file-header `note` already pointed at
  `llm_advisory_prior_art.csv, G2-01` — confirming the defect was confined to the one internal
  `% EVIDENCE:` audit-trail comment in `main.tex`, never the actual bib entry or the visible
  `\citep{rankgpt2023}` in reader-facing text. Confirmed by direct read, not by trusting the
  builder's report.

## 6. Scope boundary (Task item 5) — VERIFIED, nothing else changed

- Full `git diff -- manuscript/main.tex manuscript/references.bib` (reproduced above) touches
  exactly two prose sentences in §2.4, one internal comment in §2.3, and one appended block at the
  end of `references.bib`. No line outside those regions is present in the diff.
- `git diff --stat -- research/PAPER_CONTRACT.md research/CONTRIBUTION_LOCK.md
  research/contribution_lock.csv data/outputs/experiments/` returned empty — byte-identical to
  HEAD, confirmed directly (not merely asserted).
- H1 status, the 6a/6b split, and every Results/Discussion number are outside the diffed line
  ranges (381–410 of `main.tex` only) — confirmed by inspecting the diff's line numbers directly;
  Results (§5) and Discussion (§6) contain zero changed lines in this pass.

## 7. Bibliography integrity (Task item 6) — VERIFIED, exact 1:1 match

Independently grepped (not reused from the builder's count):
- `main.tex` `\cite*{}` keys (deduplicated): `amigo2009, barbudo2023, chow1970, dawidskene1979,
  elyaniv2010, frugalgpt2023, hendrickx2024, idreoskraska2019, jorgensenigel2021,
  kenfromfinance2025, manning2008, mozannarsontag2020, peakflo2025, ramp2025, rankgpt2023, rice1976,
  smithmiles2009` — 17 keys, plus one `*` wildcard from `\nocite{*}` (line 1461, a legitimate
  LaTeX directive to force all bib entries into the compiled bibliography, not an orphaned
  citation).
- `references.bib` `@`-entry keys: same 17 keys, exact match, no extras, no gaps.

No orphaned citation, no unresolved `\cite{}`, no unused bib entry.

## 8. Novelty guardrail (Task item 7) — VERIFIED, all occurrences remain negations

Grepped `main.tex` for `novel` (case-insensitive) and `no vendor`:
- All 7 "novel" occurrences are negations or explicitly-weaker-than-novelty framings: "no claim
  that ADS is a novel metric" (line 276), "not a novel contribution of this paper" (line 481), "Not
  presented as a novel..." (line 495), "not a methodological novelty claim" (line 436), "much
  weaker than any claim of methodological novelty" (line 409) — no positive, unqualified novelty
  claim present.
- The single "no vendor" occurrence (line 400) sits inside "We do not claim... that no vendor
  measures historical consistency before choosing a mechanism -- at least one industry source...
  directly contradicts that framing" — still a negation, and now the contradicting source is
  actually named and cited, which if anything makes the hedge stronger/more honest, not a
  reintroduction of `CONTRIBUTION_LOCK.md` §7 / `contribution_lock.csv` row C1's rejected framing.

No rejected claim resurfaced.

## 9. Tests (Task item 8, optional)

Ran `python -m pytest scripts/experiments/exp1/ -q` myself: **30 passed**, confirming the
builder's claim and confirming no code-side regression (expected, since no code file is in this
diff).

## 10. Public-safety scan (Task item 9)

Grepped both modified files for secrets/credentials/tokens/private-key markers and for local
Windows paths/usernames: no matches. The only URLs present are the three public vendor-blog URLs
already vetted in the literature ledger (kenfromfinance.com, peakflo.co, ramp.com) plus
pre-existing DOI links — no `C:\Users\...` paths, no `/Users/...` paths, no API keys, no
`BEGIN ... PRIVATE KEY` blocks.

## 11. Comparison against the builder's own report

Read `research/E5_2_CORRECTION_AUDIT.md` only after completing the above. Its §2–§10 match this
independent audit's findings on every checkable point (ledger field accuracy, citation placement
rationale for the "contradicts" sentence, RankGPT provenance, scope boundary, bibliography
integrity, test result). One point of independent judgment not present in the builder's report:
this audit additionally flags the joint `\citep{kenfromfinance2025,peakflo2025,ramp2025}` citation
at the "historical-consistency-audit practice" sentence as a mild precision overreach for the
`peakflo2025` component specifically (§3 above) — the builder's report asserts this grouping is
correct because "the section's own pre-existing `% EVIDENCE:` comment already grouped all three
sources under" that sentence, which is true as provenance but does not by itself establish that
B8-05's content actually supports the specific "historical-consistency-audit" characterization.
This disagreement is noted as OPTIONAL FUTURE WORK, not as a basis for a lower verdict, per the
reasoning in §3.

## 12. Findings summary

- **OPTIONAL FUTURE WORK**: The joint citation `\citep{kenfromfinance2025,peakflo2025,ramp2025}`
  at the "historical-consistency-audit practice" sentence (`manuscript/main.tex` line 398) is
  slightly broader than what `peakflo2025`'s own ledger `WhyRelevant` field (citation_ledger.csv
  row B8-05) individually supports (B8-05 explicitly disclaims pre-deployment
  historical-determinism measurement). Consider narrowing to `\citep{kenfromfinance2025,ramp2025}`
  for the historical-audit clause and citing `peakflo2025` separately for the confidence-tiered
  cascade half, in a future pass — not required before checkpoint.

No REQUIRED NOW findings were identified in this correction pass.

## 13. Verdict

**PASS**

Justification: every field in the three new `references.bib` entries traces exactly to
`citation_ledger.csv` rows B8-04/05/06 with no invention or alteration. The "contradicts that
framing" citation is precisely and correctly scoped to the one source (`kenfromfinance2025`) whose
own ledger entry supports it. The `PAPER_CONTRACT.md` §2 row 11 not-peer-reviewed qualification is
satisfied at both citation points, independently verified by reading the current manuscript text.
The RankGPT fix is confirmed correct and genuinely comment-only — no reader-facing citation was
ever wrong. The diff is scope-clean: nothing outside the two targeted sentences and one internal
comment changed, and `PAPER_CONTRACT.md`, `CONTRIBUTION_LOCK.md`, `contribution_lock.csv`, and the
frozen Experiment 1 artifacts are byte-identical to HEAD. Bibliography keys match 1:1 with no
orphans. No rejected claim (novelty, "no vendor measures...") resurfaced. Tests pass (30/30). No
secrets, credentials, or local-path leakage in either modified file. The one substantive
disagreement with the builder's own report — the joint three-source citation being marginally
broader than B8-05 alone supports — is a precision nit, not a factual error, misstatement of
ledger content, or a `PAPER_CONTRACT.md`/`CONTRIBUTION_LOCK.md` violation, and does not rise to
CONDITIONAL. This correction pass is safe to commit as-is.
