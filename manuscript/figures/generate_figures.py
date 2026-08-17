"""Generate F1-F4 for the ADS-Cascade manuscript from frozen Experiment 1 evidence.

Reads only committed, frozen artifacts under data/outputs/experiments/exp1/ --
no new experiments, no re-computation of any statistic beyond what those
artifacts already report. Uses the stdlib csv module (not pandas) and
matplotlib, consistent with this repository's stdlib-first convention.

NOTE (Phase E5.4): matplotlib is not installed in this repository's own
environment (verified via `python -c "import matplotlib"`, ModuleNotFoundError)
-- requirements.txt intentionally leaves it commented out (see that file) since
it is needed only for this figure-generation step, not for reproducing
Experiment 1's results. This script was executed in an isolated,
scratchpad-only virtualenv with matplotlib installed (mirroring the
verification pattern used for rapidfuzz in E5.3,
research/E5_3_CORRECTION_AUDIT.md Sec.3) to render the committed
manuscript/figures/f1_design_flow.pdf .. f4_ranking_constancy.pdf, which
main.tex now includes via \includegraphics.

Usage:
    pip install matplotlib
    python manuscript/figures/generate_figures.py
"""

import csv
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RESULTS_CSV = os.path.join(
    REPO_ROOT, "data", "outputs", "experiments", "exp1", "final", "final_condition_results.csv"
)
OUT_DIR = os.path.dirname(__file__)

R3_LOW = 0.70
R3_HIGH = 0.90


def load_rows():
    with open(RESULTS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    for r in rows:
        r["realized_det_pct"] = float(r["realized_det_pct"])
        r["rules_whole_set_accuracy"] = float(r["rules_whole_set_accuracy"])
        r["retrieval_whole_set_accuracy"] = float(r["retrieval_whole_set_accuracy"])
        r["lexical_variation"] = r["lexical_variation"] in ("True", "true", "1")
    return rows


def ads_band(x):
    if x < R3_LOW:
        return "<0.70"
    if x < R3_HIGH:
        return "0.70-0.90"
    return ">=0.90"


def make_f1(plt):
    """F1 -- experimental design / pre-registration flow. A static schematic,
    not data-driven from the CSV (no numbers to transcribe), drawn directly."""
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.axis("off")
    boxes = [
        (0.03, "Generator\n(6 nominal targets\n x 20 seeds)"),
        (0.28, "Lexical condition\nCLEAN / VARIED"),
        (0.53, "Two isolated\nmechanisms\n(rules, retrieval)"),
        (0.78, "Pre-registered\nfalsification table\n(Sec.4.8)"),
    ]
    for x, label in boxes:
        ax.add_patch(plt.Rectangle((x, 0.35), 0.19, 0.3, fill=False))
        ax.text(x + 0.095, 0.5, label, ha="center", va="center", fontsize=8)
    for x0 in (0.03, 0.28, 0.53):
        ax.annotate("", xy=(x0 + 0.24, 0.5), xytext=(x0 + 0.22, 0.5),
                    arrowprops=dict(arrowstyle="->"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "f1_design_flow.pdf"))
    plt.close(fig)


def make_f2(plt, rows):
    """F2 -- ADS vs mechanism accuracy, both lexical conditions."""
    fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True)
    for ax, varied in zip(axes, (False, True)):
        sub = [r for r in rows if r["lexical_variation"] == varied]
        x = [r["realized_det_pct"] for r in sub]
        ax.scatter(x, [r["rules_whole_set_accuracy"] for r in sub], s=10, label="rules", marker="o")
        ax.scatter(x, [r["retrieval_whole_set_accuracy"] for r in sub], s=10, label="retrieval", marker="^")
        ax.set_title("VARIED" if varied else "CLEAN")
        ax.set_xlabel("realized ADS")
    axes[0].set_ylabel("whole-set accuracy")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "f2_ads_vs_accuracy.pdf"))
    plt.close(fig)


def make_f3(plt, rows):
    """F3 -- R3 agreement by realized-ADS region, VARIED only (CLEAN has no
    defined comparisons -- see main.tex Sec.5.1/5.3).

    The <0.70 band has zero defined R3-vs-empirical comparisons: R3 selects
    llm_required there (excluded from the primary comparison), never
    rules/retrieval, so r3_agrees_with_empirical is blank for all 70 rows.
    That is rendered as an explicit N/A marker, not a 0%-height bar -- a bare
    0% bar would be visually indistinguishable from the >=0.90 band's
    genuine, defined, exceptionless 0/18 disagreement, collapsing
    "structurally not evaluated" and "evaluated and failed" into the same
    mark (research/PAPER_CONTRACT.md Sec.6/Sec.7 numerical-rule concern)."""
    bands = ["<0.70", "0.70-0.90", ">=0.90"]
    varied = [r for r in rows if r["lexical_variation"]]
    counts = {b: {"agree": 0, "n": 0} for b in bands}
    for r in varied:
        b = ads_band(r["realized_det_pct"])
        flag = r.get("r3_agrees_with_empirical")
        if flag in ("True", "False"):
            counts[b]["n"] += 1
            if flag == "True":
                counts[b]["agree"] += 1

    fig, ax = plt.subplots(figsize=(5, 4))
    for i, b in enumerate(bands):
        n, agree = counts[b]["n"], counts[b]["agree"]
        if n:
            rate = 100.0 * agree / n
            ax.bar(i, rate, color="tab:blue")
            ax.text(i, rate + 2, f"{agree}/{n}", ha="center", va="bottom", fontsize=9)
        else:
            ax.bar(i, 100, facecolor="none", edgecolor="gray", hatch="//", linewidth=0.8)
            ax.text(i, 50, "N/A\n(R3 excludes\nthis band)", ha="center", va="center",
                    fontsize=8, color="gray")
    ax.set_xticks(range(len(bands)))
    ax.set_xticklabels(bands)
    ax.set_ylabel("R3 agreement rate (%)")
    ax.set_xlabel("realized-ADS band (VARIED)")
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "f3_r3_agreement_by_band.pdf"))
    plt.close(fig)


def make_f4(plt, rows):
    """F4 -- mechanism-ranking constancy: rules-retrieval accuracy difference
    vs realized ADS, both lexical conditions, zero line marked."""
    fig, ax = plt.subplots(figsize=(6, 4))
    for varied, marker, label in ((False, "o", "CLEAN"), (True, "^", "VARIED")):
        sub = [r for r in rows if r["lexical_variation"] == varied]
        x = [r["realized_det_pct"] for r in sub]
        y = [r["rules_whole_set_accuracy"] - r["retrieval_whole_set_accuracy"] for r in sub]
        ax.scatter(x, y, s=10, marker=marker, label=label)
    ax.axhline(0.0, linestyle="--")
    ax.set_xlabel("realized ADS")
    ax.set_ylabel("rules - retrieval accuracy")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "f4_ranking_constancy.pdf"))
    plt.close(fig)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = load_rows()
    make_f1(plt)
    make_f2(plt, rows)
    make_f3(plt, rows)
    make_f4(plt, rows)
    print("Wrote f1_design_flow.pdf, f2_ads_vs_accuracy.pdf, "
          "f3_r3_agreement_by_band.pdf, f4_ranking_constancy.pdf to", OUT_DIR)


if __name__ == "__main__":
    main()
