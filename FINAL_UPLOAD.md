# Final Upload Artifact

## Kaggle Upload File

Upload:

```text
submissions/latest_final_package.zip
```

Equivalent copy:

```text
submissions/healthlynked_option_c_clean.zip
```

## Current Artifact Fingerprint

- SHA-256: `9176360b4b262d56cb831a1e1e20c4c847ca1a50929e5dc3d1126910e5557320`
- Size: `169818` bytes
- Curated package files: `66`
- Verification: `98 / 98` checks passing

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/final_upload_verify
```

Expected result:

```text
checks=98 passed=True failed=0
```

## Judge Smoke Test

After unzipping the package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_best_pipeline.py --out-dir outputs/judge_smoke
```

Expected proof points:

- F1 `0.948276`
- auto-apply precision `1.0`
- cost per correct update `$0.005836`
