import re, sys
s = open('main.tex', encoding='utf-8', newline='').read()
orig = s
E = []
def rep(old, new, tag):
    global s
    if s.count(old) != 1:
        E.append((tag, s.count(old))); return
    s = s.replace(old, new); print("OK  ", tag)

# ---------- 1. ABSTRACT ----------
a_old = """Classification systems are usually built by selecting a mechanism -- rules,
retrieval, a trained model -- before any measurement of whether that choice
fits the data. We ask whether historical decision consistency, measured
before deployment, can be used to select between qualitatively different
classification mechanisms. We test this with a pre-registered, 240-condition
synthetic factorial experiment"""
a_new = """Can historical decision consistency, measured before deployment, tell a
system designer which classification mechanism to build? We test this with a
pre-registered 240-condition synthetic factorial experiment"""
rep(a_old, a_new, "abstract opener")

b_old = """Realized historical consistency is
strongly correlated with each mechanism's own accuracy (Pearson $r>0.9$ in
both lexical conditions), but it does not predict which mechanism wins: a
frozen, pre-specified consistency-threshold decision rule agrees with the
empirically best-performing mechanism in 100\\% of comparisons in one
consistency band and in 0\\% of comparisons in another, because the empirical
winner is instead a constant function of the separately manipulated lexical
condition -- a variable the consistency signal is constructed to be blind to."""
b_new = """The answer splits in two.
Realized consistency predicts each mechanism's own accuracy well (Pearson
$r>0.9$ in both lexical conditions). It does not predict which mechanism
wins. A frozen, pre-specified consistency-threshold rule agrees with the
empirically best mechanism in 100\\% of comparisons in one consistency band
and 0\\% in another, because the winner is instead a constant function of the
separately manipulated lexical condition, a variable the consistency signal
is constructed not to observe."""
rep(b_old, b_new, "abstract body")

c_old = """We conclude that a design-time selector
built on historical consistency alone should not be used to predict which
mechanism will win."""
c_new = """A design-time selector built on historical
consistency alone therefore cannot predict which mechanism will win in this
setting."""
rep(c_old, c_new, "abstract conclusion")

# ---------- 2. SCOPE PARAGRAPH ----------
roadmap = """Section~2 positions this work against the algorithm-selection, meta-learning,"""
scope = """\\subsection{Scope and Non-Novelty}
\\label{sec:scope-non-novelty}

Four things this paper does not claim, stated once here rather than repeated
at each point of contact. ADS is not a new metric: its closed form is cluster
purity, and equally the raw majority-vote agreement proportion
(Section~\\ref{sec:cluster-purity}). Design-time selection from historical
evidence is not a new pattern; it is the Algorithm Selection Problem
\\citep{rice1976} and its descendants. R3 is not a proposed method: it is
reused unmodified from a production system's own rule taxonomy, and this
paper measures where it fails. The application domain is not unprecedented;
at least one non-peer-reviewed industry source \\citep{kenfromfinance2025}
describes similar practice already in use. What the paper does claim is a
bounded empirical result about where one already-used signal succeeds and
where it fails.

\\subsection{Paper Roadmap}
\\label{sec:roadmap}

Section~2 positions this work against the algorithm-selection, meta-learning,"""
rep(roadmap, scope, "scope subsection + roadmap split")

# ---------- 3. RELATED WORK DISCLAIMER DELETIONS ----------
rep("""a different name, applied to the same kind of repeated-labeling data. We
therefore make no claim that ADS is a novel metric -- this is a closed
question, not an open one, and the paper's contribution, developed in the
following subsections and in Section~5, lies entirely in what this
already-known metric is used for, not in its formula.""",
"""a different name, applied to the same kind of repeated-labeling data. The
paper's contribution lies in what this already-known metric is used for, not
in its formula.""", "2.1 disclaimer")

rep("""paper studies. We make no claim that design-time selection from historical
evidence is itself new -- this general pattern is well established. This
paper's narrower question is whether""",
"""paper studies. This general pattern is well established. This paper's
narrower question is whether""", "2.2a disclaimer")

rep("""framing found in the surrounding literature. This paper's simple,
interpretable threshold rule is not offered as a competitor to that automated
search paradigm. The delta is one of evidence type and mechanism, not
performance: this paper studies""",
"""framing found in the surrounding literature. The delta is one of evidence
type and mechanism, not performance: this paper studies""", "2.2b disclaimer")

rep("""experiment tests. We do not claim that a one-shot, pre-deployment design gate
is itself a contribution; if anything, it is the position this literature
argues against, cited here as contrast rather than as an unsolved problem
this paper addresses. This paper's experiment is about a specific signal type""",
"""experiment tests. This literature argues against the one-shot gate; it is
cited here as contrast, not as an unsolved problem this paper addresses.
This paper's experiment is about a specific signal type""", "2.2c disclaimer")

rep("""\\citet{hendrickx2024}. Nothing in this experiment is offered as a new
reject-option variant. This literature is not directly engaged by
Experiment~1 at all, because""",
"""\\citet{hendrickx2024}. This literature is not directly engaged by
Experiment~1, because""", "2.3a disclaimer")

rep("""defer to a human, informed by historical decision data. We do not claim that
this experiment's mechanism-selection rule is an instance of learning to
defer. As with reject-option methods, this literature establishes the same""",
"""defer to a human, informed by historical decision data. As with
reject-option methods, this literature establishes the same""", "2.3b disclaimer")

rep("""technique. Experiment~1's two-mechanism comparison is not itself put forward
as a cascade contribution. Neither family is directly relevant to the""",
"""technique. Neither family is directly relevant to the""", "2.3c disclaimer")

rep("""similar informal historical-consistency-audit practice already in production use. We do not
claim that the application domain itself is unprecedented, or that no vendor
measures historical consistency before choosing a mechanism -- at least one
industry source \\citep{kenfromfinance2025} (not peer-reviewed) directly contradicts that framing. The narrow delta that
survives is academic, not methodological: no peer-reviewed study""",
"""similar informal historical-consistency-audit practice already in production
use. The narrow delta that survives, stated row by row in
Table~\\ref{tab:positioning}, is academic, not methodological: no peer-reviewed study""",
"2.4 disclaimer")

# ---------- 4. CONCLUSION ENDING ----------
rep("""here as a direction, not built or tested. This paper's contribution is a
precise, evidenced boundary on what a historical-consistency signal can and
cannot tell a system designer, not a solution to mechanism selection, not a
validated method, and not a new metric or architecture.""",
"""here as a direction, not built or tested. The practical consequence is narrow
and concrete: a design-time selector reading only a consistency statistic is
most confident exactly where it is most wrong. In the realized $\\geq0.90$
band, where R3's recommendation for rules is strongest, it disagreed with the
empirical winner in all 18 tested conditions.""", "conclusion ending")

# ---------- 5. RANGE REFS ----------
rep("throughout Sections~4--5 is a third quantity",
    "throughout Sections~\\ref{sec:experimental-design} and~\\ref{sec:results} is a third quantity", "L513 range")
rep("""discusses; none of them is new information beyond what Sections~5.2--5.6
already established.""",
"""discusses; none of them is new information beyond what the preceding
subsections already established.""", "5.7 range")

if E:
    print("\nFAILED:", E); sys.exit(1)
open('main.tex','w',encoding='utf-8',newline='').write(s)
print("\nAll edits applied.")
