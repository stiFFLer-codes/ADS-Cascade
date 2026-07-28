"""Model-agnostic AI adapter (architecture/09, ADR-011).

This package is the ONLY place an LLM provider is called. Swapping Groq (demo) for Claude
Haiku (production) is a change here plus an env var — no other module imports a provider.
"""
