import pandas as pd

from scripts.run_best_pipeline import BEST_CFG
from src.data import build_candidate_updates, load_dataset
from src.metrics import score_candidate_updates


def test_pipeline_metrics_and_auto_policy():
    providers, evidence, gold = load_dataset()
    candidates = build_candidate_updates(providers, evidence, BEST_CFG)
    metrics = score_candidate_updates(candidates, gold)
    assert metrics["f1"] == 0.948276
    assert metrics["auto_apply_precision"] == 1.0
    assert metrics["auto_apply_count"] == 3
    auto = candidates[candidates["decision"] == "auto_apply"]
    assert set(auto["field"]).issubset({"phone", "specialty"})
    assert (auto["confidence"] >= 0.94).all()
    assert (auto["distinct_sources"] >= 3).all()


def test_high_risk_fields_do_not_auto_apply():
    providers, evidence, _ = load_dataset()
    candidates = build_candidate_updates(providers, evidence, BEST_CFG)
    high_risk = candidates[candidates["field"].isin(["address", "license_status", "accepting_new_patients"])]
    assert not (high_risk["decision"] == "auto_apply").any()
