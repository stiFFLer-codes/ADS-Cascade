#!/usr/bin/env python3
r"""R10.9 -- final arXiv preparation.

  1. Strip the entire comment layer from main.tex (326 comment-only lines).
  2. Replace it with a short public header.
  3. Remove \nocite{*} (inert today, a trapdoor the moment an uncited entry
     is added).
  4. Preserve the two \section* trap warnings as LaTeX-visible notes so the
     warning does not vanish with the comments.
  5. Write .gitattributes so autocrlf can never smudge .tex again.
  6. Build arxiv_submission.tar.gz and verify it compiles from a clean
     extract with zero errors and zero undefined references.

Run from the repository root:  python3 scripts/r10_9_final_pass.py
"""
import os, re, sys, shutil, subprocess, tarfile, hashlib

ROOT = os.getcwd()
MAN  = os.path.join(ROOT, 'manuscript')
TEX  = os.path.join(MAN, 'main.tex')
if not os.path.isfile(TEX):
    sys.exit("ERROR: run from the repository root (manuscript/main.tex not found)")

src = open(TEX, encoding='utf-8', newline='').read()
lines = src.split('\n')
n_before = len(lines)
n_comments = sum(1 for l in lines if l.lstrip().startswith('%'))

# --- 1. preserve the two \section* trap warnings as real LaTeX comments -----
# They are re-emitted below; everything else in the comment layer goes.

# --- 2. strip every comment-only line -------------------------------------
kept = [l for l in lines if not l.lstrip().startswith('%')]

# collapse runs of 3+ blank lines left behind into a single blank line
out, blanks = [], 0
for l in kept:
    if l.strip() == '':
        blanks += 1
        if blanks <= 1: out.append(l)
    else:
        blanks = 0; out.append(l)
s = '\n'.join(out)

# --- 3. public header ------------------------------------------------------
HEADER = (
 "% Historical Consistency Predicts Mechanism Accuracy, Not Mechanism Ranking:\n"
 "% Evidence from a Controlled Synthetic Study\n"
 "%\n"
 "% Compiles with pdfLaTeX + BibTeX. Requires: amsmath, amssymb, graphicx,\n"
 "% booktabs, natbib. Figures are in figures/ as PDF.\n"
 "%\n"
 "% Code and data: github.com/stiFFLer-codes/ADS-Cascade\n"
 "%\n"
 "% Note: the two \\section* units near the end carry no \\label, because a\n"
 "% \\label after \\section* captures the last stepped counter and would\n"
 "% resolve to the wrong number. Adding one requires \\phantomsection\n"
 "% (hyperref), which this document does not load.\n"
)
s = HEADER + s.lstrip('\n')

# --- 4. remove \nocite{*} --------------------------------------------------
before_nocite = s.count('\\nocite{*}')
s = re.sub(r'[ \t]*\\nocite\{\*\}[ \t]*\n', '', s)
if s.count('\\nocite{*}') != 0:
    sys.exit("ERROR: \\nocite{*} removal failed")

open(TEX, 'w', encoding='utf-8', newline='').write(s)
n_after = len(s.split('\n'))
print(f"[1] comment layer: removed {n_comments} comment-only lines")
print(f"[2] \\nocite{{*}}   : removed {before_nocite} occurrence(s)")
print(f"[3] line count   : {n_before} -> {n_after}")

# --- 5. .gitattributes -----------------------------------------------------
ga = os.path.join(ROOT, '.gitattributes')
want = "* text=auto eol=lf\n*.tex text eol=lf\n*.bib text eol=lf\n*.py text eol=lf\n*.pdf binary\n"
existing = open(ga, encoding='utf-8').read() if os.path.isfile(ga) else ''
if existing != want:
    open(ga, 'w', encoding='utf-8', newline='').write(want)
    print("[4] .gitattributes written (eol=lf enforced)")
else:
    print("[4] .gitattributes already correct")

# --- 6. integrity checks ---------------------------------------------------
raw = open(TEX, 'rb').read()
cr  = raw.count(b'\r'); na = sum(1 for b in raw if b > 127)
print(f"[5] bytes        : CR={cr}  non-ASCII={na}")
if cr or na: sys.exit("ERROR: CR bytes or non-ASCII bytes present")

labels = set(re.findall(r'\\label\{([^}]*)\}', s))
refs   = set(re.findall(r'\\(?:ref|eqref)\{([^}]*)\}', s))
dangling = refs - labels
print(f"[6] labels={len(labels)} refs={len(refs)} dangling={sorted(dangling)}")
if dangling: sys.exit("ERROR: dangling references")

cited = set()
for m in re.findall(r'\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}', s):
    cited.update(k.strip() for k in m.split(','))
bibkeys = set(re.findall(r'^@\w+\{([^,]+),',
                         open(os.path.join(MAN, 'references.bib'), encoding='utf-8').read(), re.M))
print(f"[7] cited={len(cited)} bib={len(bibkeys)} "
      f"missing_from_bib={sorted(cited-bibkeys)} uncited={sorted(bibkeys-cited)}")
if cited - bibkeys: sys.exit("ERROR: citation with no bib entry")

if s.count('{') != s.count('}'): sys.exit("ERROR: unbalanced braces")
for env in ('table','figure','equation','tabular','abstract','document'):
    if s.count('\\begin{%s}' % env) != s.count('\\end{%s}' % env):
        sys.exit("ERROR: unbalanced environment: " + env)
print("[8] braces and environments balanced")

# --- 7. build the arXiv tarball -------------------------------------------
STAGE = os.path.join(ROOT, 'arxiv_build')
shutil.rmtree(STAGE, ignore_errors=True); os.makedirs(STAGE)
shutil.copy(TEX, STAGE)
shutil.copy(os.path.join(MAN, 'references.bib'), STAGE)
figs = os.path.join(MAN, 'figures'); os.makedirs(os.path.join(STAGE, 'figures'))
used = set(re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}', s))
copied = []
for f in sorted(os.listdir(figs)):
    if f.lower().endswith('.pdf'):
        shutil.copy(os.path.join(figs, f), os.path.join(STAGE, 'figures')); copied.append(f)
print(f"[9] staged: main.tex, references.bib, {len(copied)} figures {copied}")
missing = [u for u in used if not any(os.path.basename(u).split('.')[0] in c for c in copied)]
if missing: sys.exit("ERROR: figure referenced but not staged: %s" % missing)

# --- 8. compile from the clean stage --------------------------------------
have_tex = shutil.which('pdflatex') and shutil.which('bibtex')
if have_tex:
    env = dict(os.environ, TEXINPUTS='.:')
    for cmd in (['pdflatex','-interaction=nonstopmode','main'],
                ['bibtex','main'],
                ['pdflatex','-interaction=nonstopmode','main'],
                ['pdflatex','-interaction=nonstopmode','main']):
        subprocess.run(cmd, cwd=STAGE, env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    log = open(os.path.join(STAGE,'main.log'), encoding='utf-8', errors='replace').read()
    errs = len(re.findall(r'^!', log, re.M))
    und  = len(re.findall(r'undefined|multiply.defined', log, re.I))
    pdf  = os.path.join(STAGE,'main.pdf')
    print(f"[10] clean-extract compile: errors={errs} undefined={und} "
          f"pdf={'yes' if os.path.isfile(pdf) else 'NO'}")
    if errs or und or not os.path.isfile(pdf):
        sys.exit("ERROR: clean-extract compile failed -- do NOT submit")
else:
    print("[10] pdflatex/bibtex not installed -- SKIPPED. "
          "The tarball is UNVERIFIED; compile it elsewhere before submitting.")

# --- 9. tar it -------------------------------------------------------------
TAR = os.path.join(ROOT, 'arxiv_submission.tar.gz')
with tarfile.open(TAR, 'w:gz') as t:
    t.add(os.path.join(STAGE,'main.tex'), arcname='main.tex')
    t.add(os.path.join(STAGE,'references.bib'), arcname='references.bib')
    bbl = os.path.join(STAGE,'main.bbl')
    if os.path.isfile(bbl): t.add(bbl, arcname='main.bbl')
    for f in copied:
        t.add(os.path.join(STAGE,'figures',f), arcname='figures/'+f)
size = os.path.getsize(TAR)
sha = hashlib.sha256(open(TAR,'rb').read()).hexdigest()
with tarfile.open(TAR) as t: names = sorted(t.getnames())
print(f"[11] {os.path.basename(TAR)}  {size/1024:.0f} KB  sha256={sha[:16]}...")
print(f"[12] contents: {names}")
print("\nR10.9 complete. Tarball is ready for arXiv upload.")
