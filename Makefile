.PHONY: best verify public-triage package-status

best:
	python3 scripts/run_best_pipeline.py --out-dir outputs/local_best

verify:
	python3 scripts/verify_pipeline.py --package submissions/latest_final_package.zip --out-dir outputs/verify_latest

public-triage:
	python3 scripts/run_public_dataset_triage.py --input data/raw/kaggle_public_provider_directory/provider_directory_dataset.csv --out-dir outputs/public_dataset_triage --top-n 100

package-status:
	python3 -c 'from pathlib import Path; import hashlib; p = Path("submissions/latest_final_package.zip"); print(f"path={p}"); print(f"exists={p.exists()}"); print(f"size_bytes={p.stat().st_size}" if p.exists() else "size_bytes="); print(f"sha256={hashlib.sha256(p.read_bytes()).hexdigest()}" if p.exists() else "sha256=")'
