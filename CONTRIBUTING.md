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

For judge-facing changes, keep `FINAL_UPLOAD.md`, `submissions/latest_final_package.zip`, and `submissions/healthlynked_option_c_clean/` synchronized before pushing.
