# Synthetic Volume Benchmark And AWS Throughput Plan

## Current Quality Context

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Local Throughput Benchmark

| Providers | Evidence Rows | Candidate Updates | Runtime Seconds | Providers / Second | F1 | Auto-Apply Precision |
|---:|---:|---:|---:|---:|---:|---:|
| 72 | 1224 | 58 | 0.2181 | 330.08 | 0.948276 | 1.0 |
| 720 | 12240 | 580 | 1.0816 | 665.68 | 0.948276 | 1.0 |
| 3600 | 61200 | 2900 | 5.447 | 660.91 | 0.948276 | 1.0 |
| 7200 | 122400 | 5800 | 10.6573 | 675.59 | 0.948276 | 1.0 |

## AWS Step Functions Plan

| Scenario | Providers | Batch Size | Max Parallel Batches | Batches | Waves | Estimated Parallel Minutes |
|---|---:|---:|---:|---:|---:|---:|
| daily_delta_refresh | 10000 | 500 | 20 | 20 | 1 | 0.01 |
| regional_refresh | 100000 | 1000 | 40 | 100 | 3 | 0.07 |
| national_backfill | 1000000 | 2000 | 80 | 500 | 7 | 0.35 |
