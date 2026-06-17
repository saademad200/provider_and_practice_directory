# AWS Bedrock LLM Fallback Contract

This experiment defines when the pipeline may use an LLM for messy provider pages and how outputs are constrained, validated, priced, and routed. The normal path remains deterministic extraction; Bedrock is a review-assist fallback, not the source of automatic truth.

## Current Pipeline Context

- F1: 0.93913
- Precision: 0.947368
- Recall: 0.931034
- Auto-apply precision: 1.0

## Official AWS Surfaces

- Amazon Bedrock overview: https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Bedrock Converse API: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html
- Structured JSON outputs: https://docs.aws.amazon.com/bedrock/latest/userguide/structured-output.html
- Tool schema reference: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolInputSchema.html

## Fixture Results

| Fixture | Call LLM | Gate Reasons | Estimated Cost | Grounded Output | Warnings |
|---|---:|---|---:|---:|---|
| clean_regex_page | False |  | $0.001097 | True |  |
| messy_location_page | True | deterministic_extraction_sparse, location_hint_without_address, provider_hint_without_specialty | $0.001116 | True | missing_structured_contact_fields, llm_low_confidence_review_only |
| unsupported_span | False |  | $0.00109 | False | schema_or_grounding_error_review_only |

## Guardrails

- Call Bedrock only when deterministic extraction is sparse, the page is complex, or location/provider hints imply missing fields.
- Use JSON-schema structured output with temperature 0 and a small max-output budget.
- Require evidence spans to appear in the source page text.
- Route every LLM-derived fact to review unless independently corroborated by stronger sources.
- Redact patient data and send only the minimum public provider-page snippet.
- Log model id, prompt version, schema version, source URL, retrieved timestamp, raw output hash, validation result, and reviewer disposition.
- Apply a hard per-page cost gate before calling any model.
