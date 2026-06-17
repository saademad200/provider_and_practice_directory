# Agentic Whitepaper Insights

Source PDFs:

- `AgenticWhitepapers/The New SDLC With Vibe Coding_Day_1.pdf`
- `AgenticWhitepapers/Agent Tools & Interoperability_Day_2.pdf`

## Takeaways For This Competition

The submission should be framed as agentic engineering, not casual automation. The winning artifact is the harness: source connectors, schemas, evals, review queues, dashboards, audit events, rollback plans, and monitoring.

The local benchmark is not enough by itself. Every important capability should have an artifact-level eval or diagnostic: extraction fixtures, source ablation, missing-source robustness, conflict adjudication, inactive-provider detection, LLM fallback validation, and package verification.

Avoid a single-agent monolith in the production design. Use specialized lanes or agents:

- source discovery and retrieval
- NPPES/state/license connectors
- web extraction and Bedrock fallback
- provider/practice identity resolution
- evidence scoring and source conflict adjudication
- human review prioritization
- audit, rollback, and monitoring

Tool and agent interfaces should be explicit contracts. Prefer versioned connector schemas, dashboard data contracts, audit-event schemas, and eventually MCP/A2A-style discoverability over hidden custom glue.

Human-in-the-loop is not a weakness here. For healthcare directory updates, HITL is the safety boundary: show source inputs, proposed changes, authority conflicts, confidence, cost, and rollback status before risky updates.

Context engineering is a cost lever. Keep model calls sparse and high-signal, gate Bedrock fallback to messy pages only, and preserve deterministic extraction as the default path.

The judge-facing story should distinguish demo from production. The demo proves the loop can run; the production plan proves repeatability, governance, observability, scoped permissions, source legality, and failure recovery.

## New Iteration Bias

Future experiments should prefer improvements in one of these harness dimensions:

- eval coverage and regression checks
- source/tool contract clarity
- agent or workflow decomposition
- observability, traceability, and cost accounting
- review ergonomics and decision quality
- rollback and correction safety
- deployment readiness on AWS
