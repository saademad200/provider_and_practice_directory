# Security Policy

This repository is intended for a private competition and implementation handoff.

## Data Boundary

- Do not commit `.env` files, API keys, Kaggle tokens, AWS credentials, paid API tokens, private provider/customer data, or production HealthLynked records.
- Use `data/sample/` and final synthetic/proxy artifacts for reproducible demos.
- Treat real provider-directory exports as customer data unless explicitly approved for repository storage.

## Reporting Issues

Report security or data-exposure issues directly to the repository owner. Do not open public issues containing credentials, source tokens, provider records, or vulnerable endpoint details.

## Local Checks

Before pushing:

```bash
make verify
git status --short
```

The final package also includes `NO_SECRETS_SCAN.md`, `no_secrets_findings.csv`, and `no_secrets_summary.json`.
