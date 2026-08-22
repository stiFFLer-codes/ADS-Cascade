#!/usr/bin/env python3
r"""R10.10 -- add arXiv e-print identifiers to references.bib.

arXiv strongly encourages arXiv identifiers in reference lists so they can be
harvested by automated software (INSPIRE and others). Identifiers must contain
no extraneous font commands, spaces, tildes, braces, or line-breaks.

Three IDs added, each verified against the official arXiv abstract page:
  rankgpt2023        arXiv:2304.09542
  mozannarsontag2020 arXiv:2006.01862
  hendrickx2024      arXiv:2107.11277

Formatting matches the existing frugalgpt2023 entry (note + url).
No other field is touched. Run from manuscript/.
"""
import sys
p = 'references.bib'
s = open(p, encoding='utf-8', newline='').read()
E = []
def rep(old, new, tag):
    global s
    if s.count(old) != 1:
        E.append((tag, s.count(old))); return
    s = s.replace(old, new); print("OK  ", tag)

rep("""  doi       = {10.18653/v1/2023.emnlp-main.923},
  note      = {Full author list verified against the ACL Anthology record
             (aclanthology.org/2023.emnlp-main.923/).}
}""",
"""  doi       = {10.18653/v1/2023.emnlp-main.923},
  note      = {Preprint 2023, arXiv:2304.09542. Full author list verified
             against the ACL Anthology record
             (aclanthology.org/2023.emnlp-main.923/).},
  url       = {https://arxiv.org/abs/2304.09542}
}""", "rankgpt2023 -> arXiv:2304.09542")

rep("""  booktitle = {Proceedings of the 37th International Conference on Machine Learning (ICML), PMLR vol. 119},
  year      = {2020},
  url       = {https://proceedings.mlr.press/v119/mozannar20b.html}
}""",
"""  booktitle = {Proceedings of the 37th International Conference on Machine Learning (ICML), PMLR vol. 119},
  year      = {2020},
  note      = {Preprint 2020, arXiv:2006.01862},
  url       = {https://proceedings.mlr.press/v119/mozannar20b.html}
}""", "mozannarsontag2020 -> arXiv:2006.01862")

rep("""  doi     = {10.1007/s10994-024-06534-x},
  note    = {arXiv preprint 2021}
}""",
"""  doi     = {10.1007/s10994-024-06534-x},
  note    = {Preprint 2021, arXiv:2107.11277},
  url     = {https://arxiv.org/abs/2107.11277}
}""", "hendrickx2024 -> arXiv:2107.11277")

if E:
    print("\nFAILED:", E); sys.exit(1)
open(p, 'w', encoding='utf-8', newline='').write(s)
print("\nAll 3 identifiers added. Regenerate main.bbl and the tarball with:")
print("  cd .. && python3 scripts/r10_9_final_pass.py")
