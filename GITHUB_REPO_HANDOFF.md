# GitHub Repository Handoff

This workspace is prepared as a local Git repository for a private GitHub handoff.

## Recommended Repository Settings

- Visibility: private until after competition judging.
- Default branch: `main`.
- Required check: `verify-package`.
- Protect `.env` and all credentials through repository secrets only.
- Do not commit raw Kaggle credentials, paid API tokens, or private provider/customer records.

## Create Remote With Plain Git

Create an empty GitHub repository in the browser, then run:

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git branch -M main
git push -u origin main
```

HTTPS alternative:

```bash
git remote add origin https://github.com/<owner>/<repo>.git
git branch -M main
git push -u origin main
```

## Files To Review First

- `README.md`
- `SUBMISSION.md`
- `submissions/exp0172/ONE_PAGE_JUDGE_GUIDE.md`
- `submissions/exp0172/COMBINED_ABC_PIPELINE_COVERAGE.md`
- `submissions/exp0172/EXECUTIVE_SUMMARY.md`
- `submissions/exp0172/ARTIFACT_INDEX.md`

## CI

The workflow in `.github/workflows/verify.yml` installs dependencies and verifies:

- Python modules compile.
- The best pipeline CLI runs.
- Metrics meet threshold.
- The latest final package contains required artifacts.

Run the same check locally:

```bash
make verify
```
