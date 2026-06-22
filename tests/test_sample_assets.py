import json
from pathlib import Path


def test_sample_recommendations_have_required_evidence():
    data = json.loads(Path("assets/sample_recommendations.json").read_text())
    assert data["metrics_snapshot"]["f1"] == 0.948276
    for rec in data["recommendations"]:
        assert rec["audit_required"] is True
        for change in rec["changes"]:
            assert change["supporting_sources"]
            assert change["source_observations"]
            assert change["evidence_hash"]
            assert change["policy_version"]
