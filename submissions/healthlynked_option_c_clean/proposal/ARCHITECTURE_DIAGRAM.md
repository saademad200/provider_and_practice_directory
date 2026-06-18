# Architecture Diagram

## Render-Free Diagram

```text
HealthLynked directory
  -> risk scanner
  -> trusted source connector orchestrator
  -> evidence store
  -> normalization
  -> provider / practice / location matching
  -> validation logic
  -> confidence score
  -> decision router
       -> no change: confirm current record
       -> safe high-confidence update: auto-update
       -> conflict or low confidence: human review
  -> audit log + rollback plan
  -> directory update + feedback loop
```

LLM extraction is a gated fallback for approved but messy pages. It is not the default retrieval path.

## Mermaid Diagram

```mermaid
flowchart TD
    A[HealthLynked Provider and Practice Directory] --> B[Risk Scanner]
    B --> C{Refresh Needed?}
    C -->|No| N[No Change / Confirm Current Record]
    C -->|Yes| D[Trusted Source Connector Orchestrator]

    D --> S1[NPPES / NPI Registry]
    D --> S2[State Licensing Boards]
    D --> S3[CMS / Public Datasets]
    D --> S4[Practice Websites]
    D --> S5[Health System Directories]
    D --> S6[Guarded Business Listing Fallback]

    S1 --> E[Evidence Store]
    S2 --> E
    S3 --> E
    S4 --> E
    S5 --> E
    S6 --> E

    E --> F[Clean and Normalize Data]
    F --> G[Provider / Practice Matching]
    G --> H[Validation Logic]
    H --> I[Confidence Score]

    I --> J{Decision}
    J -->|Record confirmed| N
    J -->|High-confidence update| K[Safe Auto Update]
    J -->|Low confidence or conflict| L[Human Review]

    K --> M[Audit Log + Rollback Plan]
    L --> M
    N --> M
    M --> O[Update Directory + Feedback Loop]
    O --> B

    P[LLM Extraction Fallback] -. gated only .-> F
    D -. messy approved page .-> P
```
