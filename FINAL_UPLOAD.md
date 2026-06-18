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

- SHA-256: `31ea246795aacd3be0c6be8d27813f4cedec1b36a8a7702c7ef1e1108ced29e9`
- Size: `171148` bytes
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
