"""Confidence thresholds + tier definitions (architecture/08, ADR-016).

Named constants, not magic numbers. These are PILOT starting points derived from Phase 1
distributions — calibration is a pilot exit criterion (OPEN-Q12), not a fixed truth.
"""
# Tier 1 — company deterministic
T1_ADS = 0.95
T1_MIN_EVIDENCE = 3
# Tier 1c — global unanimous (strict: cross-company consistency is only 0.695)
T1_GLOBAL_ADS = 0.98
GLOBAL_MIN_COMPANIES = 5
# Tier 2 — mid-confidence (auto-apply + spot-check).
# Calibrated from the Stage A held-out eval: ads>=0.80 on low evidence measured ~45%,
# and fuzzy auto-apply measured ~49% — both unsafe. So mid-tier now needs stronger
# agreement AND real evidence, and fuzzy is demoted to review (never auto-applied).
T2_ADS_LOW = 0.90
T2_MIN_EVIDENCE = 5
T2_GLOBAL_ADS_LOW = 0.85
T2_SIM = 85          # rapidfuzz WRatio scale is 0..100 (== similarity 0.85)
FUZZY_AUTO_APPLY = False   # fuzzy/embedding matches go to review until human-confirmed (ADR: alias promotion)
# Tier 3/4 floor
T3_FLOOR = 0.50
# Cold-start fuzzy bridge: only a near-identical form counts (repairs OCR formatting, not
# a semantic guess). Review only.
GLOBAL_FUZZY_CUTOFF = 88

AUTO_APPLY_TIERS = (1, 2)   # applied without a human
REVIEW_TIERS = (3, 4)       # routed to a person
