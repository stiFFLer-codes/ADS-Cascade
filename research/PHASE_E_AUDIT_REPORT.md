# Audit Report — Phase E Kickoff (Format/Structure/Boundary Planning Pass)

> Independent audit of the four new Phase E planning documents. This pass is a
> FORMAT/STRUCTURE/BOUNDARY review, not a code or experimental-evidence review — no manuscript
> prose, no code, and no experimental artifacts were touched this session. This is a **separate**
> report from `research/AUDIT_REPORT.md` (the frozen Gate 4 / Contribution Lock audit, referenced by
> `CONTRIBUTION_LOCK.md`'s own "Auditor verdict" section) — that file was NOT overwritten and its
> Gate 4 content remains authoritative and unchanged for that gate. This report covers Phase E0 only.

---

## 1. Repository state

- Branch: `main`. HEAD: `5cf04e6` ("Phase D: lock research contribution").
- Working tree: four new untracked files, nothing else modified, nothing staged:
  `research/MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `research/MANUSCRIPT_FORMAT_RESEARCH.md`,
  `research/PHASE_E_PLAN.md`, `research/PUBLIC_RELEASE_BOUNDARY.md`.
- Diffed: read all four new files in full; cross-checked against `CONTRIBUTION_LOCK.md`,
  `RESEARCH_GPS.md`, `EVIDENCE_BASELINE.md`, `TECHNICAL_REPORT.md`, `STATE.md`,
  `research/literature/citation_ledger.csv`, `scripts/experiments/exp1/*`, and live official arXiv
  documentation (fetched this pass, not from training memory).
- No git commit, push, or staging performed by this audit.
- **Correction note:** this audit's first execution pass, run as a subagent, mistakenly wrote its
  output over `research/AUDIT_REPORT.md` (the frozen Gate 4 audit artifact `CONTRIBUTION_LOCK.md`
  references by name). That was caught and reverted (`git checkout -- research/AUDIT_REPORT.md`)
  before being presented to the human; this document is the same audit content, correctly filed
  under its own name instead.

## 2. Current research GPS

`RESEARCH_GPS.md`'s "CURRENT LOCATION"/"CURRENT GATE" sections still read "Phase D.1 — COMPLETE" /
"Contribution lock" gate, with Gate 4's checklist items shown unchecked (⬜). This is **stale**:
`CONTRIBUTION_LOCK.md` (committed at the current HEAD) records Gate 4 as "Adopted" with an
auditor-verified PASS, and its own commit message states "Phase E (manuscript drafting) is now
unblocked." This session has already produced four Phase E documents on top of that. `STATE.md`
likewise contains no mention of Phase E. Neither file was edited by this audit (not mine to rewrite
per my instructions) — flagged for the human to update. North-star distance: on track — Phase E0
(format/structure/boundary) is the correct next step per the locked contribution, not a detour.

## 3. Changed files

- **Docs (planning only):** `MANUSCRIPT_FORMAT_RESEARCH.md`, `PHASE_E_PLAN.md`,
  `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`, `PUBLIC_RELEASE_BOUNDARY.md` — all four newly created.
- **Code:** none changed.
- **Experimental artifacts:** none changed.
- **Manuscript:** none — confirmed no `manuscript/` directory, no `.tex` file, no new figure file
  exists anywhere in the tree (`find` swept for `*.tex` and a `manuscript` directory; both empty).
- **Other:** none.

## 4. Research integrity

No new quantitative claims were introduced by these four documents — they map, plan, and bound;
they do not assert new results. Checked the rejected-claims list (`CONTRIBUTION_LOCK.md` §7)
against all four files by direct grep for the forbidden phrases (`novel metric`, `validates R3`,
`universally`, `enterprise AI broadly`, `no vendor`/`no comparable vendor`, `consistency alone is
sufficient`, `higher ADS means...`, etc.). Every match found occurs strictly inside an explicit
"claims that must NOT appear" list or table (`PHASE_E_PLAN.md` §3.2 item 5,
`MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §2) — never asserted positively as the document's own claim.
No rejected claim has crept back in.

Independently reconfirmed the two outstanding `TECHNICAL_REPORT.md` issues these documents cite as
still-open (rather than trusting the documents' own restatement):
- §5, lines 289-291: vendor-practice sentence ("typically ships a single learned classifier...
  chosen up front rather than derived from a measured determinism distribution") is still present
  verbatim — confirmed by direct read.
- §3.2 line 219-220 and §3.3: synthetic figures are still the pre-A5-fix superseded values
  (0.809/0.931 weighted/unweighted ADS, 84.1% deterministic-share), not the canonical post-fix
  0.9031/0.9597/87.56% recorded in `EVIDENCE_BASELINE.md` §2-3 as the only citable values.

Both claims in `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md` §3-4 about `TECHNICAL_REPORT.md`'s staleness are
therefore verified accurate, not merely restated.

## 5. Scientific consistency

`PHASE_E_PLAN.md`'s manuscript structure (§3.3, the 9-section hierarchy) and its per-section
claim/evidence table (§3.4-3.6) trace cleanly back to `CONTRIBUTION_LOCK.md` §6/§11: Results is
split into 5.1 (headline), 5.2 (6a — ADS predicts accuracy), 5.3 (6b — ADS does not predict
ranking), 5.4 (mechanistic explanation) — the accuracy/ranking distinction that
`CONTRIBUTION_LOCK.md` §4 insists must never be collapsed is preserved as a structural boundary
between subsections, not just a sentence-level caveat. Discussion §6.1 is pinned to reuse
`CONTRIBUTION_LOCK.md`'s synthesis sentence verbatim, and the production case study is confined to
§6.3 (Discussion, explicitly "contextual, not evidentiary") and a brief mention in §1
(Introduction, as motivation). Figure F7 ("project-history diagram") is explicitly rejected in
Task 7 for being exactly the internship/project-history framing the brief forbids — this is the
correct call and shows the plan actively guarding against the failure mode, not just avoiding it
by omission.

## 6. Evidence/claim traceability

Spot-verified `MANUSCRIPT_CLAIM_EVIDENCE_MAP.md`'s cited literature-ledger rows directly against
`research/literature/citation_ledger.csv` rather than trusting the map's own status labels:
B1-01, B2-01, B2-02, B4-03, B4-04, B4-07, B7-01, B8-04, B8-05, B8-06 were all read directly from
the CSV and confirmed `VERIFIED` or `VERIFIED-INDUSTRY` (the industry-source rows B8-04/05/06 are
correctly downgraded to `VERIFIED-INDUSTRY` in the ledger and correctly flagged in the map as
"not peer-reviewed — must be labeled as such in-text"). No claim in the map overstates its
ledger-recorded confidence.

## 7. Code review

Not applicable in the strict sense — no code was written or modified this pass. However, Task 6 of
`PHASE_E_PLAN.md` makes a reproducibility claim about existing code (`scripts/experiments/exp1/*`
runs "end-to-end offline, no keys, no cost"), so this was checked by inspection per the brief's
item 6:
- `run_final.py` imports only `csv/itertools/json/statistics/sys/time/pathlib` (stdlib) plus the
  repo's own `consistency.py`/`mechanisms.py`/`stats.py`/`p2lib` modules. `p2lib/retrieval.py`
  imports `rapidfuzz` (a pip package, no network/keys required) — no `requests`/`urllib`/`socket`/
  `boto3` import anywhere in the exp1 call graph. The claim of "no keys, no cost" holds structurally.
- Frozen-config assertions in `run_final.py` (δ=0.02, cutoff=75, thresholds 0.90/0.70, 20 seeds)
  match the values `EXPERIMENT_1_FINAL_RESULTS.md` and `CONTRIBUTION_LOCK.md` §9 report as frozen.
  240 = 6 targets × 2 lexical conditions × 20 seeds, matching the documented factorial design.
- `PHASE_E_PLAN.md` Task 8's planned (not-yet-created) `generate_figures.py` would add a
  `matplotlib` dependency; this is not new scope creep — `ROADMAP.md` line 179 already names "one
  matplotlib script generating all figures" as a pre-existing plan item, and no such file was
  actually created this pass (confirmed by `find`).

## 8. Experimental integrity

Not applicable — no experimental artifact under `data/outputs/experiments/` was touched, read-write
checked, or re-derived differently this pass. (Numbers cited from frozen Experiment 1 evidence in
the four new documents were spot-checked only for correct restatement, covered under Research
Integrity/Traceability above, not for re-derivation — that was already done by the prior audit pass
recorded in `CONTRIBUTION_LOCK.md`'s own auditor verdict.)

## 9. Scope/GPS alignment

**PASS.** All four documents stay inside the Phase E0 brief: format research, template decision,
manuscript structure, claim/evidence map, release boundary, reproducibility strategy, figure/table
plan, workflow, milestones. Verified directly (not merely trusting the documents' own scope
statements): no `manuscript/` directory, no `.tex` file, no figure file, and no manuscript prose
exists anywhere in the tree. `RESEARCH_GPS.md`'s DO NOT CHASE list is still fundamentally correct
for this pass's content (no new experiment, no vendor/model experimentation, no re-tuning of frozen
parameters occurred), but the document itself is stale on *location* (see §2) — a live
inconsistency worth the human's attention, not a violation caused by this pass.

## 10. Git hygiene

`git status --porcelain` shows exactly the four expected new files, untracked, nothing staged,
nothing else modified (after reverting the AUDIT_REPORT.md overwrite noted in §1). Independently
grepped the full tracked tree (not trusting `PUBLIC_RELEASE_BOUNDARY.md`'s own sweep) for AWS
credential patterns, private-key headers, `GROQ_API_KEY` literals, signed-URL patterns, and real
Romanian CUI/company-name patterns. All hits were false positives on inspection:
- `GROQ_API_KEY` hits are an environment-variable *name* referenced in setup instructions
  (`scripts/phase2/p2lib/ai/adapter.py`, `scripts/phase2/p2_06_llm_tail.py`), never a literal key
  value.
- The `s3://` hit in `scripts/01_5_xml_normalization.py` is an f-string template
  (`s3_uri = f"s3://{bucket}/{key}"`), not a hardcoded bucket/credential.
- `CUI`/company-name hits in `architecture/11_SEQUENCE_PETROMAX.md` are explicitly labeled
  fictionalized in the document's own header ("Vendor/company names, CUIs... are fictionalized for
  public documentation"); the fake CUI shown (`RO90012345`) is not a real identifier.
- `CUI` hits in `data/outputs/invoice_lines_all_companies.csv` and related CSVs resolve to
  `SYNTH COMPANY 0NN SRL` with CUIs in the fake `99000NN` range — confirmed by direct read of the
  CSV header and first rows.
No secrets, no real client data, no credentials found anywhere in the tracked tree. This
independently confirms `PUBLIC_RELEASE_BOUNDARY.md`'s "clean" verdict rather than just accepting
it.

**arXiv sourcing independently re-verified** (per the task's explicit request) against live
official pages, not training memory:
- `info.arxiv.org/help/endorsement.html` + `blog.arxiv.org/2026/01/21/...`: confirmed the
  2026-01-21 policy change eliminating "institutional email alone" as sufficient for automatic
  endorsement, and the two-path structure (automatic = institutional email + prior co-authorship
  in the domain; manual = personal endorsement from an established author) exactly as
  `MANUSCRIPT_FORMAT_RESEARCH.md` §1.14 states.
- 50MB submission cap: no official page currently states a size figure directly on the pages
  fetched (`info.arxiv.org/help/submit/index.html`, `sizes.html`), consistent with the document's
  own honest hedge ("no official page found stating a more recent change... reconfirm at actual
  submission time"); independent web search corroborates 50MB has been in effect since July 2020
  and remains current. The document's hedged framing is accurate, not overclaimed.
- "No universal template required": confirmed — `info.arxiv.org/help/policies/format_requirements.html`
  states general formatting standards (title/authorship, references, margins, font size) with no
  mandated template or `.cls` file.

## 11. Findings

1. **[OPTIONAL FUTURE WORK]** `research/RESEARCH_GPS.md`'s "CURRENT LOCATION"/"CURRENT GATE"
   sections are stale — they still describe Gate 4 as open/in-progress with unchecked boxes, even
   though `CONTRIBUTION_LOCK.md` (same HEAD) records Gate 4 as adopted/PASS and this session has
   already begun Phase E. `STATE.md` similarly has no Phase E mention. Not a defect introduced by
   the four new documents (none of which depend on `RESEARCH_GPS.md` being current — they cite
   `CONTRIBUTION_LOCK.md` directly), but a real drift risk for a future session that trusts
   `RESEARCH_GPS.md` as the "living pointer" without cross-checking. File: `research/RESEARCH_GPS.md`,
   lines 12-68.
2. **[OPTIONAL FUTURE WORK]** No new finding beyond what the four documents themselves already
   flag: `TECHNICAL_REPORT.md` §5 (lines 289-291, vendor-practice sentence) and §3.2/§3.3 (lines
   219-220, superseded synthetic figures) remain uncorrected. This audit independently reconfirms
   both are still present (see §4 above) — restating here only so it is visible in this report's
   own findings list, not because it is new. File: `TECHNICAL_REPORT.md`, lines 219-220, 289-291.
3. **[PROCESS, RESOLVED]** This audit's own subagent execution initially overwrote
   `research/AUDIT_REPORT.md` (the frozen Gate 4 artifact) instead of writing to a separate file.
   Caught and reverted before delivery (§1). Flagging so the pattern is known: any future audit
   invocation on this repository should be told explicitly to write its report to a *new*,
   phase-specific filename, never to the bare `research/AUDIT_REPORT.md` name, once that name is
   serving as a specific gate's frozen, cross-referenced artifact rather than a rolling log.

No REQUIRED NOW findings were identified. All six of the task's explicit verification points
(arXiv sourcing, template-lock, structure-vs-contribution, release-boundary conservatism,
no-rejected-claims-returned, reproducibility-accuracy) were independently checked and confirmed
accurate, and no scope creep beyond the Phase E0 brief was found.

## 12. Required fixes

None. (Empty — no REQUIRED NOW findings.)

## 13. Verdict

## 🟡 PASS_WITH_NOTES

All four Phase E0 documents independently verify as accurate, properly scoped, and free of
resurrected rejected claims. arXiv-sourcing claims (endorsement policy change, 50MB cap, no
universal template) were confirmed against live official arXiv/blog.arxiv.org pages, not merely
trusted. The plain-`article`-class template recommendation genuinely avoids venue lock-in. The
proposed manuscript structure is evidence-first and correctly subordinates the production case
study to a motivating/contextual role throughout, matching `CONTRIBUTION_LOCK.md` §6/§11.
`PUBLIC_RELEASE_BOUNDARY.md`'s "repo is clean" claim was independently re-derived (not just
restated) and holds. Reproducibility-tier claims about `scripts/experiments/exp1/` structurally
check out (stdlib + rapidfuzz only, no network, matches documented frozen parameters). No
manuscript prose, LaTeX file, or figure was created — the pass stayed inside its E0 boundary. The
only issue found is process hygiene, not integrity: `RESEARCH_GPS.md`/`STATE.md` are stale on
current phase/gate status, which the human should update but which does not itself compromise any
claim in the four audited documents. Safe to proceed to Phase E1.
