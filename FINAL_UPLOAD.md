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

- SHA-256: `37e60309526b193476098c0e612a5522e86a53e7106c3db8d5c79fe3e4101367`
- Size: `169812` bytes
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
