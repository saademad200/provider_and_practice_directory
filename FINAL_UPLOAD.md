# Final Upload Artifact

## Kaggle Upload File

Upload:

```text
submissions/latest_final_package.zip
```

## Current Artifact Fingerprint

- SHA-256: `14bb29fab3e2f157715df686391185e711f0a81c066ab4e0fdd74af9f2b97c0c`
- Size: `167146` bytes
- Curated package files: `62`
- Verification: `131 / 131` checks passing

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/final_upload_verify
```

Expected result:

```text
checks=131 passed=True failed=0
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
- prototype evidence-only cost per correct update `$0.005836`

Latest manual unzip smoke:

- Method: extracted the tracked upload zip into a temporary local folder and ran the package-local MVP command
- Result: F1 `0.948276`, auto-apply precision `1.0`, prototype evidence-only cost per correct update `$0.005836`
- Output files confirmed: candidate updates and review queue
