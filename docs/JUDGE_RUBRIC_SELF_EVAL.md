# Judge Rubric Coverage Self Eval

Curated-package refresh against `submissions/latest_final_package.zip`. This is an internal coverage check, not an official judge score: it asks whether each published evaluation criterion has concrete evidence in the upload and whether the numeric proxy gates pass.

## Coverage Result

- Weighted coverage: 100.0 / 100
- Coverage percent: 100.0%
- Criteria with complete evidence: 12 / 12

## Current Prototype Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0
- Review queue count: 55

## Rubric

| Criterion | Weight | Score | Weighted | Metric Detail |
|---|---:|---:|---:|---|
| accuracy | 16 | 5.0 | 16.0 | f1=0.948276 threshold=0.93 passed=True; auto_apply_precision=1.0 threshold=0.99 passed=True |
| scalability | 10 | 5.0 | 10.0 | no numeric threshold |
| cost_efficiency | 8 | 5.0 | 8.0 | cost_per_correct_update_usd=0.005836 threshold=0.01 passed=True |
| practicality | 10 | 5.0 | 10.0 | no numeric threshold |
| explainability | 8 | 5.0 | 8.0 | no numeric threshold |
| data_quality | 8 | 5.0 | 8.0 | no numeric threshold |
| source_reliability | 8 | 5.0 | 8.0 | no numeric threshold |
| human_review | 8 | 5.0 | 8.0 | review_count=55.0 threshold=30 passed=True; auto_apply_precision=1.0 threshold=0.99 passed=True |
| audit_and_rollback | 8 | 5.0 | 8.0 | no numeric threshold |
| privacy_security | 6 | 5.0 | 6.0 | no numeric threshold |
| agentic_innovation | 6 | 5.0 | 6.0 | no numeric threshold |
| operational_verifiability | 4 | 5.0 | 4.0 | no numeric threshold |
