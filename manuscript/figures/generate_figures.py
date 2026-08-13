"""Generate F1-F4 for the ADS-Cascade manuscript from frozen Experiment 1 evidence.

Reads only committed, frozen artifacts under data/outputs/experiments/exp1/ --
no new experiments, no re-computation of any statistic beyond what those
artifacts already report. Uses the stdlib csv module (not pandas) and
matplotlib, consistent with this repository's stdlib-first convention.

NOTE (Phase E3): this script was written but could not be executed in the
current environment -- matplotlib is not installed here (verified via
`python -c "import matplotlib"`, ModuleNotFoundError). This mirrors the
project's existing, previously-reported substitution pattern for the missing
pdflatex/bibtex toolchain (research/MANUSCRIPT_SKELETON_AUDIT.md): the gap is
reported explicitly rather than faked. Run this script in an environment with
matplotlib installed to produce manuscript/figures/f1.pdf .. f4.pdf; main.tex
currently references these paths in captioned figure placeholders (per the E3
definition of done, a captioned placeholder without a rendered image is a
valid slot -- research/PAPER_CONTRACT.md Sec.11).

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
        (0.78, "Pre-registered\nfalsification table\n(Sec.4.13)"),
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
    defined comparisons -- see main.tex Sec.5.1/5.3)."""
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
    rates = [100.0 * counts[b]["agree"] / counts[b]["n"] if counts[b]["n"] else 0.0 for b in bands]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(bands, rates)
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
