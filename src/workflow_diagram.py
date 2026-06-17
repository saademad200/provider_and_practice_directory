from __future__ import annotations

import pandas as pd


def workflow_nodes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"node_id": "schedule", "label": "EventBridge Scheduler", "owner": "platform", "artifact": "AWS_PRODUCTION_ARCHITECTURE.md"},
            {"node_id": "source_registry", "label": "Source Connector Registry", "owner": "source_ops", "artifact": "SOURCE_CONNECTOR_REGISTRY.md"},
            {"node_id": "source_fetch", "label": "Source Retrieval Agents", "owner": "source_ops", "artifact": "evidence_tool_manifest.json"},
            {"node_id": "normalize", "label": "Evidence Normalization Agent", "owner": "data_quality", "artifact": "bedrock_extraction_contract.json"},
            {"node_id": "identity", "label": "Identity Resolution Agent", "owner": "identity_ops", "artifact": "DUPLICATE_MOVEMENT_DETECTION.md"},
            {"node_id": "conflict", "label": "Source Conflict Agent", "owner": "data_quality", "artifact": "SOURCE_CONFLICT_ADJUDICATION.md"},
            {"node_id": "score", "label": "Evidence Scoring Agent", "owner": "ml_ops", "artifact": "candidate_updates.csv"},
            {"node_id": "safety", "label": "Trajectory And Red-Team Evals", "owner": "ml_ops", "artifact": "RED_TEAM_EVALS.md"},
            {"node_id": "route", "label": "Auto-Apply Or Review Router", "owner": "directory_ops", "artifact": "review_queue.csv"},
            {"node_id": "review", "label": "Human Review Workbench", "owner": "directory_ops", "artifact": "REVIEW_DISPOSITION_AND_SLA.md"},
            {"node_id": "audit", "label": "Audit And Rollback Agent", "owner": "compliance", "artifact": "AUDIT_ROLLBACK_WORKFLOW.md"},
            {"node_id": "monitor", "label": "Monitoring And Learning Loop", "owner": "platform", "artifact": "MONITORING_ALERTS.md"},
        ]
    )


def workflow_edges() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"from": "schedule", "to": "source_registry", "handoff": "batch plan and source policy"},
            {"from": "source_registry", "to": "source_fetch", "handoff": "approved tools and freshness SLAs"},
            {"from": "source_fetch", "to": "normalize", "handoff": "raw evidence snapshots"},
            {"from": "normalize", "to": "identity", "handoff": "canonical evidence rows"},
            {"from": "identity", "to": "conflict", "handoff": "matched provider/practice candidates"},
            {"from": "conflict", "to": "score", "handoff": "adjudicated evidence and conflict flags"},
            {"from": "score", "to": "safety", "handoff": "candidate updates with confidence and traces"},
            {"from": "safety", "to": "route", "handoff": "passed evals and blocked forbidden outcomes"},
            {"from": "route", "to": "review", "handoff": "ambiguous or high-risk review queue"},
            {"from": "route", "to": "audit", "handoff": "safe auto-apply candidates"},
            {"from": "review", "to": "audit", "handoff": "review dispositions and audit event IDs"},
            {"from": "audit", "to": "monitor", "handoff": "applied updates, rollback plans, audit bundles"},
            {"from": "monitor", "to": "source_registry", "handoff": "source health, cost drift, reviewer feedback"},
        ]
    )


def mermaid_workflow() -> str:
    return """flowchart LR
    schedule[EventBridge Scheduler] --> source_registry[Source Connector Registry]
    source_registry --> source_fetch[Source Retrieval Agents]
    source_fetch --> normalize[Evidence Normalization Agent]
    normalize --> identity[Identity Resolution Agent]
    identity --> conflict[Source Conflict Agent]
    conflict --> score[Evidence Scoring Agent]
    score --> safety[Trajectory And Red-Team Evals]
    safety --> route{Auto-Apply Or Review?}
    route -->|safe low-risk update| audit[Audit And Rollback Agent]
    route -->|ambiguous/high-risk| review[Human Review Workbench]
    review --> audit
    audit --> monitor[Monitoring And Learning Loop]
    monitor --> source_registry

    classDef control fill:#e8f1f8,stroke:#1e6b9e,color:#16202a
    classDef human fill:#fff4df,stroke:#9a6b1d,color:#16202a
    classDef safety fill:#fbe7e7,stroke:#a33a3a,color:#16202a
    class source_registry,source_fetch,normalize,identity,conflict,score,audit,monitor control
    class review human
    class safety safety
"""
