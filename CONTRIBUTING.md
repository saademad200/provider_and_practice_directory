# Contributing

This project is organized around small, evidence-backed pipeline changes.

## Development Rules

- Keep the MVP and production docs aligned.
- Route identity-sensitive, conflicting, or high-risk updates to review.
- Prefer deterministic source connectors and normalization before LLM fallback.
- Keep every proposed update explainable with source, confidence, reason, and audit metadata.
- Do not add secrets, paid API keys, private records, or raw production data.

## Verification

Run:

```bash
make verify
```

For research iterations:

```bash
python3 scripts/run_one_research_iteration.py
```

Log meaningful changes in `autoresearch/JOURNAL.md` and keep the final package handoff synchronized when a new best result is promoted.
