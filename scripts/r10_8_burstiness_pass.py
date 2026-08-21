# R10.8 -- sentence-length variation. Splits long clause-stacks into shorter
# sentences. No claim, number, or statistic is added, removed, or altered.
import sys
s = open('main.tex', encoding='utf-8', newline='').read()
E = []
def rep(old, new, tag):
    global s
    if s.count(old) != 1:
        E.append((tag, s.count(old))); return
    s = s.replace(old, new); print("OK  ", tag)

R = [
# 57w -> 20w + 37w
("retrieval-based fuzzy matching)? Answering it requires four preconditions to\nhold in the target setting: a history of repeated decisions on the same or\nsimilar items, observable ground-truth labels for those decisions, a",
 "retrieval-based fuzzy matching)? Four preconditions must hold in the target\nsetting. There must be a history of repeated decisions on the same or\nsimilar items, observable ground-truth labels for those decisions, a", "174"),
# 57w -> 22w + 33w
("third mechanism, a large language model, is deliberately excluded from the\nprimary comparison for a documented, principled reason detailed in\nSection~\\ref{sec:domain-mechanism-scope}: not because it was inconvenient to\ninclude, but because the\nsynthetic generator's product string carries no signal predictive of the",
 "third mechanism, a large language model, is deliberately excluded from the\nprimary comparison. The reason is documented in\nSection~\\ref{sec:domain-mechanism-scope}, and it is not convenience. The\nsynthetic generator's product string carries no signal predictive of the", "210"),
# 58w -> 12w + 25w
("are two different claims, with two different (here, opposite) answers, and\nthis paper never merges them into a single statement about whether\n\"historical consistency works.\"",
 "are two different claims with two different answers. Here the answers are\nopposite. This paper never merges them into a single statement about whether\n\"historical consistency works.\"", "229"),
# 57w -> 25w + 30w
("use. The narrow delta that survives, stated row by row in\nTable~\\ref{tab:positioning}, is academic, not methodological: no peer-reviewed study of this\nspecific document-classification niche was found in the literature search\nthis paper's evidence base draws on, which is a modest, honest niche-novelty\nobservation, much weaker than any claim of methodological novelty, and not",
 "use. The narrow delta that survives, stated row by row in\nTable~\\ref{tab:positioning}, is academic rather than methodological. No\npeer-reviewed study of this specific document-classification niche was found\nin the literature search this paper's evidence base draws on. That is a\nmodest niche-novelty observation, much weaker than any claim of\nmethodological novelty, and not", "433"),
# 65w -> 33w + 26w
("$\\{70,75,80,85,90\\}$ were evaluated against a product-identity hit-rate\ncriterion (whether the top fuzzy match resolves to the same underlying\nproduct as the query, rather than whether the resulting account label is\ncorrect), subject to a minimum coverage floor of 30\\%; a cutoff of 75 was selected and\nfrozen for the entire run, never re-tuned per band, per lexical condition, or",
 "$\\{70,75,80,85,90\\}$ were evaluated against a product-identity hit-rate\ncriterion, subject to a minimum coverage floor of 30\\%. That criterion asks\nwhether the top fuzzy match resolves to the same underlying product as the\nquery, not whether the resulting account label is correct. A cutoff of 75 was\nselected and frozen for the entire run, never re-tuned per band, per lexical\ncondition, or", "718"),
# 62w -> 27w + 30w
("mechanism-blind ADS calibration swept a dense 17-point target grid with ten\nseeds per target (using no import of, and no reference to, either\nmechanism's code) to characterize the generator's realizable realized-ADS\nrange and to choose the six final targets by a mechanism-blind greedy\nfurthest-point selection over that curve, so that no target band was chosen",
 "mechanism-blind ADS calibration swept a dense 17-point target grid with ten\nseeds per target, using no import of and no reference to either mechanism's\ncode. It characterized the generator's realizable realized-ADS range and\nchose the six final targets by a greedy furthest-point selection over that\ncurve, so that no target band was chosen", "820"),
# 56w -> 30w + 24w
("structure rather than the flat aggregate. Binned by each row's own realized\nADS against R3's own thresholds (the primary framing, matching the locked\nwording this paper draws on), R3 agrees with the empirical winner\nin 100\\% (32 of 32) of conditions in the realized 0.70--0.90 band, and in 0\\%\n(0 of 18) of conditions in the realized $\\geq0.90$ band (Figure~\\ref{fig:r3-agreement}). A secondary, also",
 "structure rather than the flat aggregate. The primary framing bins by each\nrow's own realized ADS against R3's own thresholds, matching the locked\nwording this paper draws on. Under it, R3 agrees with the empirical winner\nin 100\\% (32 of 32) of conditions in the realized 0.70--0.90 band, and in 0\\%\n(0 of 18) of conditions in the realized $\\geq0.90$ band (Figure~\\ref{fig:r3-agreement}). A secondary, also", "1002"),
# 56w -> 26w + 32w
("The production observation described in Section~1.1 is consistent with\nSection~5.2's positive finding (a real deployment did show a measured\nconsistency statistic correlating with something real about its own data),\nbut it was never itself a controlled test of Section~5.3's ranking finding,\nbecause production never ran a lexical-noise sweep of the kind this",
 "The production observation described in Section~1.1 is consistent with\nSection~5.2's positive finding. A real deployment did show a measured\nconsistency statistic correlating with something real about its own data. It\nwas never itself a controlled test of Section~5.3's ranking finding, though,\nbecause production never ran a lexical-noise sweep of the kind this", "1177"),
# 58w -> 30w + 28w
("construction. We state this account explicitly as inferred from exhaustive\nbut post-hoc inspection of the frozen data and the generator's code, not as\nthe result of a second, independently designed confirmatory experiment: the\npattern holds without exception across all 240 rows, but a fresh, prospective\ntest of this exact causal claim on new data would strengthen it further",
 "construction. We state this account explicitly as inferred from exhaustive\nbut post-hoc inspection of the frozen data and the generator's code. It is\nnot the result of a second, independently designed confirmatory experiment.\nThe pattern holds without exception across all 240 rows, but a fresh,\nprospective test of this exact causal claim on new data would strengthen it\nfurther", "1231"),
# 68w -> 26w + 40w
("so the qualitative shape of 6b is partly built into the construction; what is\nnot given by that construction is the magnitude and direction actually\nobserved: the empirical winner is constant across all 120 conditions of\neach lexical condition (retrieval under VARIED, tie under CLEAN), and the",
 "so the qualitative shape of 6b is partly built into the construction. What\nthat construction does not give is the magnitude and direction actually\nobserved. The empirical winner is constant across all 120 conditions of\neach lexical condition (retrieval under VARIED, tie under CLEAN), and the", "1251"),
# 55w -> 18w + 37w
("H1 (revised), stated and pre-registered before any data from the frozen run\nexisted: under controlled synthetic conditions, higher realized historical\ndecision consistency will be associated with predictable changes in relative\nmechanism performance, such that a pre-specified, frozen consistency-based",
 "H1 (revised) was stated and pre-registered before any data from the frozen\nrun existed. Under controlled synthetic conditions, higher realized\nhistorical decision consistency will be associated with predictable changes\nin relative mechanism performance, such that a pre-specified, frozen\nconsistency-based", "600"),
]
for o,n,t in R: rep(o,n,t)
if E:
    print("\nFAILED:", E); sys.exit(1)
open('main.tex','w',encoding='utf-8',newline='').write(s)
print("\nAll", len(R), "edits applied.")
