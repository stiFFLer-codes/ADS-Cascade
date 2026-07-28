"""Provider-neutral LLM adapter. Groq now (demo), Claude Haiku in production — same two
functions, same call sites. Reads the API key from the environment (never a file/arg), and
caches every response to disk so re-runs cost nothing and are deterministic.

Enable:  set GROQ_API_KEY in the environment (see docs/PHASE2_PLAN.md). Absent -> available()
is False and callers skip the LLM tier cleanly.
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[4]   # p2lib/ai/adapter.py -> .../Analysis
CACHE = REPO / "data" / "outputs" / "phase2" / "llm_cache"


def _load_dotenv():
    """Minimal .env loader (no python-dotenv dependency). Env vars already set win."""
    envf = REPO / ".env"
    if not envf.exists():
        return
    for line in envf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_dotenv()

# --- provider config (the one place to change for Haiku) ---
ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
KEY_ENV = "GROQ_API_KEY"

# Groq free-tier limits for llama-3.3-70b-versatile (per user's dashboard): 30 RPM, 12K TPM.
# Proactive spacing keeps us under RPM; the 429 retry below is the backstop for TPM bursts.
RPM_LIMIT = 30
TPM_LIMIT = 12_000
MIN_INTERVAL = float(os.environ.get("GROQ_MIN_INTERVAL", "2.2"))  # ~27 RPM
_last_call = [0.0]


def available() -> bool:
    return bool(os.environ.get(KEY_ENV))


def _chat(messages, temperature=0.0, max_tokens=400):
    key = os.environ.get(KEY_ENV)
    if not key:
        raise RuntimeError(f"{KEY_ENV} not set — LLM tier disabled")
    CACHE.mkdir(parents=True, exist_ok=True)
    ck = hashlib.sha256(json.dumps([MODEL, messages, temperature], sort_keys=True).encode()).hexdigest()[:16]
    cf = CACHE / f"{ck}.json"
    if cf.exists():
        return cf.read_text(encoding="utf-8")
    body = {"model": MODEL, "messages": messages, "temperature": temperature, "max_tokens": max_tokens}
    for attempt in range(5):
        gap = time.monotonic() - _last_call[0]          # proactive throttle (stay under 30 RPM)
        if gap < MIN_INTERVAL:
            time.sleep(MIN_INTERVAL - gap)
        r = requests.post(ENDPOINT, headers={"Authorization": f"Bearer {key}"}, json=body, timeout=30)
        _last_call[0] = time.monotonic()
        if r.status_code == 429 or r.status_code >= 500:  # free-tier rate limit / transient
            wait = float(r.headers.get("retry-after", 2 ** attempt))
            time.sleep(min(wait, 15))
            continue
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        cf.write_text(content, encoding="utf-8")
        return content
    raise RuntimeError("Groq rate limit not clearing after retries — wait a minute and re-run (cached calls won't repeat)")


def _json(content):
    """Lenient: pull the first {...} block so a chatty model still parses."""
    m = re.search(r"\{.*\}", content, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    return {"_raw": content.strip()}


def normalize_product(raw_text, context=""):
    """Novel/messy product line -> {generic_name, category}. Tier 3/4 only."""
    return _json(_chat([
        {"role": "system", "content":
            "You are a Romanian accounting assistant. For a receipt product line, give a concise "
            "generic product name and a spending category. Reply ONLY as JSON: "
            '{"generic_name": "...", "category": "..."}. Romanian is fine.'},
        {"role": "user", "content": f"Product line: {raw_text}\nContext: {context}"},
    ]))


def propose_account(product, candidate_accounts, context=""):
    """Propose ONE account_id from the provided chart (never invent). Output goes to review."""
    chart = "\n".join(f"- {a}: {d}" for a, d in candidate_accounts)
    return _json(_chat([
        {"role": "system", "content":
            "You are a Romanian accountant. Choose the single best AccountID for the product, "
            "strictly from the provided chart of accounts — never invent one. Reply ONLY as JSON: "
            '{"account_id": "...", "rationale": "..."}.'},
        {"role": "user", "content": f"Product: {product}\nContext: {context}\nChart of accounts:\n{chart}"},
    ]))
