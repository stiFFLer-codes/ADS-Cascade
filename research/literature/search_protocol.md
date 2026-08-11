# Search Protocol — Phase B Literature Verification

> Documents how the adversarial prior-art sweep in `literature_matrix.csv` and
> `citation_ledger.csv` was actually conducted, for reproducibility. Written after the fact from
> four parallel research agents' self-reported search logs, consolidated and lightly deduplicated
> by the coordinating session. Date of search: **2026-08-11**.

## 1. Scope and method

The sweep was split into four parallel research passes, each covering two of the eight named
research families (B1–B8, see `../PHASE_A_CLOSURE.md` context and the mission brief this phase
began from). Each pass was run independently by a separate research agent with no visibility into
the other three passes, to avoid anchoring all four on the same initial hits. Each pass was
required to: (1) verify real bibliographic metadata (title/authors/year/venue/DOI) against a
primary source — publisher page, DOI resolver, or a literature-database tool's structured
`get_paper` record — rather than trust a search-engine snippet alone; (2) answer the mission's
11 diagnostic questions per retained paper; (3) actively search for evidence that would *weaken*
ADS-Cascade's claimed distinctions, not just evidence that supports them; (4) report total papers
screened vs. retained, for a reproducible funnel count.

## 2. Databases / search tools used

- **Consensus** (`mcp__claude_ai_Consensus__search`) — semantic search over the peer-reviewed
  literature index, returns abstracts, citation counts, and a Consensus-hosted URL per paper.
- **FastTrack Literature Open** (`search_papers`, `get_paper`) — search over an OpenAlex-backed
  ~250M-paper index; `get_paper` was used specifically to pull verified DOI/venue/abstract records
  for candidate citations before they were retained.
- **Scholar Gateway** (`semanticSearch`) — full-text passage-level semantic search, used where
  abstract-level search under-performed (notably for B8, where lexical search on generic
  AI/ML/accounting terms surfaced heavy off-topic noise — drug discovery, blockchain, edge
  computing, etc. — and passage-level search had much higher precision).
- **WebSearch / WebFetch** — used to (a) independently verify DOI/venue/year against a publisher
  page or DOI resolver when a tool result was ambiguous, (b) retrieve industry/vendor content with
  no DOI (B8's accounts-payable-automation vendor blogs), and (c) resolve author-list or venue
  discrepancies in garbled tool records (e.g. Peloton's author list, Franc et al.'s third author).

## 3. Exact search queries run

Reproduced verbatim from each agent's self-reported log; approximate result counts are as reported
by the tool, not independently re-counted.

### B1 (Algorithm Selection Problem) + B2 (AutoML / meta-learning)

| Tool | Query |
|---|---|
| FastTrack search_papers | "The Algorithm Selection Problem Rice" |
| FastTrack search_papers | "meta-learning algorithm selection survey Smith-Miles" |
| FastTrack search_papers | "AutoML systematic review workflow composition Barbudo" |
| Consensus | "algorithm selection problem per-instance algorithm portfolio" |
| WebSearch | Rice 1976 Advances in Computers vol 15 |
| WebSearch | Barbudo Ventura Romero 2023 Knowledge and Information Systems |
| FastTrack search_papers | "Auto-WEKA combined algorithm selection and hyperparameter optimization CASH" |
| FastTrack search_papers | "dataset characterization meta-features model selection landmarking" |
| FastTrack get_paper | DOI 10.1007/s10115-023-01935-1 (Barbudo) |
| FastTrack get_paper | DOI 10.1145/1456650.1456656 (Smith-Miles) |
| FastTrack get_paper | DOI 10.1613/jair.2490 (SATzilla) |
| FastTrack search_papers | "empirical hardness models predicting algorithm runtime Leyton-Brown" |
| FastTrack search_papers | "human-in-the-loop AutoML interactive machine learning pipeline selection" |
| Scholar Gateway semanticSearch | "Does the algorithm selection problem framework... historical label consistency..." |
| FastTrack search_papers | "Kerschke Hoos Neumann Trautmann Automated Algorithm Selection Survey..." |
| WebSearch | Thornton Hutter Hoos Leyton-Brown Auto-WEKA KDD 2013 DOI |
| FastTrack get_paper | DOI 10.1016/j.knosys.2021.108101 (Rivolli) |
| WebSearch | Kerschke et al. Evolutionary Computation 2019 DOI |
| WebSearch | Feurer et al. Auto-sklearn NeurIPS 2015 |

### B3 (Adaptive computation / Adaptive-RAG) + B7 (Workload-aware / design-time systems)

| Tool | Query |
|---|---|
| Consensus | "Adaptive-RAG learning to adapt retrieval-augmented language models through question complexity" |
| Consensus | "FrugalGPT reducing cost large language models cascade" |
| Consensus | "self-designed learned database systems workload-aware" |
| Consensus | "adaptive computation time recurrent neural networks early exit" |
| Consensus | "database cracking adaptive indexing self-organizing" |
| Consensus | "learned index structures case for learned index Kraska" |
| Consensus | "OtterTune automatic database management system tuning machine learning" |
| Consensus | "design continuum data systems instance-optimized systems Kraska" |
| Consensus | "LLM routing model selection query difficulty router large language models" |
| Consensus | "algorithm selection problem meta-learning dataset characteristics choose classifier before deployment" |
| Consensus | "learning to defer human AI collaboration selective prediction confidence threshold" |
| FastTrack search_papers | "From Auto-tuning One Size Fits All to Self-designed and Learned Data-intensive Systems Idreos" |
| FastTrack search_papers | "Adaptive-RAG…Jeong" |
| FastTrack search_papers | "FrugalGPT…Chen" |
| FastTrack search_papers | "Database Cracking Idreos Kersten Manegold CIDR 2007" |
| FastTrack search_papers | "Towards instance-optimized data systems Kraska VLDB 2021" |
| FastTrack get_paper | DOI verification x3 (Kraska Learned Index, Van Aken OtterTune) |
| WebSearch | 6 targeted DOI/venue verification queries (FrugalGPT venue, Database Cracking CIDR, instance-optimized VLDB DOI, Peloton CIDR authors, Graves ACT, RouteLLM, Khan meta-learning IEEE Access) |

### B4 (Selective prediction / reject option) + B5 (Human-in-the-loop / learning to defer)

Approximately 140 papers screened via 7 FastTrack `search_papers` query lanes (~25–100 results
each, skimmed for relevance) covering: reject-option classification, selective classification,
Chow's rule / risk-coverage theory, learning-to-defer foundational and follow-on work, human-in-
the-loop ML surveys, and 10 targeted WebSearch verification queries against specific bibliographic
leads (Hendrickx, Franc, Madras, Mozannar & Sontag, and the unresolved "Vernon 2022" lead).

### B6 (Heterogeneous pipeline composition) + B8 (Enterprise / invoice classification)

| Tool | Query |
|---|---|
| FastTrack search_papers | "model cascade coverage accuracy tradeoff machine learning" |
| FastTrack search_papers | "compound AI systems pipeline composition" |
| FastTrack search_papers | "automated general ledger account classification machine learning" |
| FastTrack search_papers | "invoice line item classification deep learning accounting" |
| FastTrack search_papers | "chart of accounts classification NLP text classification bookkeeping" |
| FastTrack search_papers | "receipt OCR document AI accounting automation extraction survey" |
| Consensus | "LLM cascade cost accuracy tradeoff routing" |
| Consensus | "expense categorization machine learning automated bookkeeping" |
| Consensus | "rule-based versus machine learning system selection criteria dataset characteristics" |
| Consensus | "mixture of experts routing gating network" |
| Consensus | "neuro-symbolic hybrid systems combining rules and neural networks survey" |
| Consensus | "algorithm selection problem meta-learning which classifier to use for a dataset" |
| Consensus | "retrieval augmented generation architecture design choices survey" |
| Scholar Gateway semanticSearch | "How do systems decide, before deployment, whether to use rule-based methods versus machine learning models versus large language models for a classification task, based on measured historical label consistency or agreement in the training data?" |
| Scholar Gateway semanticSearch | "Automated general ledger account coding and invoice line item classification for accounting using machine learning, and SAF-T fiscal e-invoicing document classification in Romania or the EU" |
| WebSearch | "SAF-T D406 Romania fiscal document classification machine learning automated GL account coding" |
| WebSearch | "invoice GL coding software vendor 'confidence score' auto-post threshold human review accounts payable AI" |
| WebFetch | Ken From Finance, Peakflo, and Ramp AP-automation vendor blogs (2 follow-up fetches after WebSearch identified the URLs) |

## 4. Screening funnel

| Family group | Approx. screened | Retained |
|---|---:|---:|
| B1 + B2 | ~120–150 | 14 (5 + 9, plus 2 later reclassified as B2 by other agents: Ali & Smith 2006, Khan 2020) |
| B3 + B7 | ~160–180 | 14 (7 + 7) |
| B4 + B5 | ~140 | 17 (10 + 7) |
| B6 + B8 | ~220 | 15 (9 + 6) |
| **Total** | **~640–690** | **56 unique** (after deduplication — see §6) |

## 5. Inclusion / exclusion criteria

**Included:** peer-reviewed papers, major-conference/journal proceedings, foundational papers with
a resolvable DOI or stable publisher/preprint page, systematic reviews and surveys, and — for B8
specifically, where academic coverage of the exact application niche (invoice/GL-account
classification) proved thin — high-quality industry/vendor sources (accounts-payable-automation
company blogs) *explicitly labeled as such* and never treated as peer-reviewed evidence.

**Excluded:** results whose bibliographic metadata could not be resolved to a real, findable paper
after multiple query variants (the "Vernon 2022" seed lead — see `citation_ledger.csv` row
`UNVERIFIED-01`); one corrupted/likely-injected FastTrack Literature Open record (nominally titled
"GPT-4 Technical Report," DOI `10.4230/lipics.cosit.2024.11`, but returning an abstract about a
fictitious "MFOUR Vibe Framework" / "Vibe Integrity Score" unrelated to GPT-4 or its real DOI) —
flagged by the B6/B8 agent, not cited, and not acted on as an instruction despite containing
instruction-like text; and weak/tangential hits below each agent's own relevance bar, which were
screened but not retained (see funnel counts above — retained is roughly 8–12% of screened).

## 6. Duplicate handling

Three papers were independently surfaced by more than one agent under different family
assignments, because their content genuinely spans families: **Khan, Zhang, Rehman & Ali (2020)**
and **Ali & Smith (2006)** were found by both the B3/B7 agent and the B6/B8 agent (both correctly
identified them as meta-learning/algorithm-selection work); **Moslem et al. (2026)**'s LLM-routing
survey was found by both the B3/B7 agent and the B6/B8 agent. Each was retained exactly once in the
final matrix, filed under its primary family (B2 for the meta-learning papers, B3 for the routing
survey), with the cross-family relevance noted in its `KeyDifference`/`PotentialChallengeToContribution`
fields rather than duplicated as a second row.

## 7. Relevance assessment

A paper was retained only if it engaged at least one of ADS-Cascade's two claimed mechanism parts
(design-time architecture selection from historical evidence; runtime confidence-tiered cascade
with human deferral) closely enough to require an explicit `OverlapType`/`OverlapStrength`/
`KeyDifference` judgment — not merely because it used adjacent vocabulary. Each retained paper was
scored against the same 11 diagnostic questions (see `literature_matrix.csv` columns) to keep the
judgment auditable rather than impressionistic, and against the mission's explicit conceptual
distinctions (runtime vs. design-time; model selection vs. system composition; query-level routing
vs. dataset-level architecture selection; learned selection vs. evidence-driven threshold selection;
homogeneous ensembles vs. heterogeneous mechanisms; confidence-based routing vs. historical-label-
behavior analysis; single-task optimization vs. system architecture design).

## 8. Terminology expansions actually used

Beyond the mission brief's seed term list, agents independently expanded into: "empirical hardness
models," "CASH problem," "instance-optimized systems," "self-driving database systems," "answer
consistency" (LLM self-agreement), "L2D" (learning to defer, as used by its own sub-literature),
"split computing," "compound AI systems," and "cascade routing" — all logged per-family above.

## 9. Known limitations of this sweep

- Four independent agents means partially independent judgment calls on `OverlapStrength` — no
  cross-agent calibration pass was run to normalize scoring across families before this document
  was written. Treat `OverlapStrength` as indicative, not a calibrated numeric scale.
- Screened-vs-retained counts are agent-self-reported approximations, not machine-counted.
- Two arXiv-only papers (B3-04, B3-07) and two arXiv-only industry-adjacent papers (B6-02, B6-03,
  B6-04) were not independently verified beyond a single tool's snippet — flagged `UNVERIFIED` or
  `UNVERIFIED-PARTIAL` in `citation_ledger.csv` and should be spot-checked before manuscript citation.
- No formal database (ACM DL, IEEE Xplore, Web of Science) was searched directly by a human;
  all searches went through the three literature-search tools plus WebSearch. This is a
  reproducibility caveat, not a validity one — every retained citation's DOI/URL was independently
  cross-checked against a publisher page or resolver, per §1.
- Areas flagged by agents as adjacent but explicitly out of scope for this pass, requiring a
  follow-up sweep before Phase C can be considered complete: (1) the label-noise / inter-annotator-
  agreement / data-quality literature (Northcutt-style "confident learning"), which may be a closer
  prior-art match to the ADS *metric itself* than anything in B1/B2; (2) the DeCCaF/OpenL2D
  fraud-detection learning-to-defer line of work (Alves et al.), which the B3/B7 agent flagged as
  looking closer to ADS-Cascade's human-escalation design than the general L2D literature reviewed
  under B5, but which was not independently verified or scored in this pass.
