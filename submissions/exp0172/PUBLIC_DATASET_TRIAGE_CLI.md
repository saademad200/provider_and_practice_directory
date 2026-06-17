# Public Dataset Triage CLI

Run the public Kaggle provider-directory transfer check with:

```bash
python3 scripts/run_public_dataset_triage.py --out-dir outputs/public_dataset_triage
```

Expected outputs:

- `public_dataset_profile_summary.json`
- `public_dataset_missingness.csv`
- `public_dataset_issue_counts.csv`
- `public_dataset_triage_action_counts.csv`
- `public_dataset_triage_top500.csv`

The current local run processed 42000 rows and 37 columns from the downloaded Kaggle-adjacent public dataset. This is not treated as official leaderboard truth or real-world truth; it is a transfer and operations-readiness check for the Option C Hybrid pipeline.
