# Synthetic Volume Benchmark And AWS Throughput Plan

This experiment closes the scalability gap identified by `PRODUCTION_READINESS_SCORECARD.md`. It expands the local benchmark in memory with unique provider, practice, NPI, evidence URL, and gold IDs, then measures candidate-generation throughput without changing the canonical sample dataset.

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Local Throughput Benchmark

| Providers | Evidence Rows | Candidate Updates | Runtime Seconds | Providers / Second | F1 | Auto-Apply Precision |
|---:|---:|---:|---:|---:|---:|---:|
| 72 | 1224 | 57 | 0.1535 | 469.04 | 0.93913 | 1.0 |
| 720 | 12240 | 570 | 1.0076 | 714.57 | 0.93913 | 1.0 |
| 3600 | 61200 | 2850 | 5.0587 | 711.65 | 0.93913 | 1.0 |
| 7200 | 122400 | 5700 | 10.1243 | 711.16 | 0.93913 | 1.0 |

## AWS Step Functions Plan

| Scenario | Providers | Batch Size | Max Parallel Batches | Batches | Waves | Estimated Parallel Minutes |
|---|---:|---:|---:|---:|---:|---:|
| daily_delta_refresh | 10000 | 500 | 20 | 20 | 1 | 0.01 |
| regional_refresh | 100000 | 1000 | 40 | 100 | 3 | 0.07 |
| national_backfill | 1000000 | 2000 | 80 | 500 | 7 | 0.33 |

## Production Interpretation

- Use EventBridge Scheduler for recurring refreshes and Step Functions Map states for provider-batch fan-out.
- Run large source normalization in AWS Batch or Glue and keep raw/normalized evidence in immutable S3 partitions.
- Keep directory mutation outside source-fetch workers; workers emit candidate rows, audit events, and review queue records.
- Use SQS dead-letter queues for failed provider batches, CloudWatch alarms for source freshness and cost drift, and idempotent batch IDs for reruns.
- Treat these timings as local CPU throughput, not a cloud SLA. The value is comparative sizing and an explicit scaling plan.
