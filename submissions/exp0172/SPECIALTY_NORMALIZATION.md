# Specialty Normalization

This experiment adds specialty alias handling so public-source taxonomies can map into the local directory vocabulary. It specifically handles NPPES-style taxonomy labels such as `Orthopaedic Surgery`.

## Current Metrics

- F1: 0.948276
- Precision: 0.948276
- Recall: 0.948276
- Auto-apply precision: 1.0

## Fixture Checks

| Raw Specialty | Normalized |
|---|---|
| Orthopaedic Surgery | orthopedics |
| Cardiovascular Disease | cardiology |
| Family Practice | family medicine |
| Paediatrics | pediatrics |
| Dermatologic Surgery | dermatology |
| Neurological Surgery | neurology |

## Alias Table

| Raw Alias | Canonical Specialty |
|---|---|
| cardiovascular disease | cardiology |
| clinical neurophysiology | neurology |
| dermatologic surgery | dermatology |
| family practice | family medicine |
| general practice | family medicine |
| internal medicine | family medicine |
| interventional cardiology | cardiology |
| neurological surgery | neurology |
| orthopaedic surgery | orthopedics |
| orthopaedics | orthopedics |
| orthopedic surgery | orthopedics |
| paediatrics | pediatrics |
| pediatric medicine | pediatrics |
| primary care | family medicine |

## Production Notes

- Keep this alias table small and auditable at first.
- Expand with NPPES taxonomy codes and HealthLynked specialty taxonomy after real data profiling.
- Treat unknown specialties as reviewable normalization gaps, not model failures.
