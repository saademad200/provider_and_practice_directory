# Final Upload Artifact

## Kaggle Upload File

Upload:

```text
submissions/latest_final_package.zip
```

## Current Artifact Fingerprint

- SHA-256: `8d64e073ff0c4ba7916d2663346ef81afdc9ff864d197169473a6850e199a42d`
- Size: `171180` bytes
- Curated package files: `67`
- Verification: `101 / 101` checks passing

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/final_upload_verify
```

Expected result:

```text
checks=101 passed=True failed=0
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

Latest manual unzip smoke:

- Command path: `outputs/manual_judge_unzip/healthlynked_option_c_clean`
- Result: F1 `0.948276`, auto-apply precision `1.0`, cost per correct update `$0.005836`
- Output files confirmed: candidate updates and review queue
