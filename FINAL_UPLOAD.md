# Final Upload Artifact

## Kaggle Upload File

Upload:

```text
submissions/latest_final_package.zip
```

## Current Artifact Fingerprint

- SHA-256: `07b3a24b67c07aa46721449ef069c61a7e2cbab53d3e502658d9c419c68fe394`
- Size: `168444` bytes
- Curated package files: `69`
- Verification: `110 / 110` checks passing

## Verify Before Upload

```bash
python3 scripts/verify_pipeline.py \
  --package submissions/latest_final_package.zip \
  --out-dir outputs/final_upload_verify
```

Expected result:

```text
checks=110 passed=True failed=0
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

- Method: extracted the tracked upload zip into a temporary local folder and ran the package-local MVP command
- Result: F1 `0.948276`, auto-apply precision `1.0`, cost per correct update `$0.005836`
- Output files confirmed: candidate updates and review queue
