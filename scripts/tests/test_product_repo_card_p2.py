import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "product-repo-card.py"
spec = importlib.util.spec_from_file_location("product_repo_card_p2", MODULE_PATH)
card_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(card_module)


def test_audit_health_summarizes_grade_distribution_and_flags_non_a(tmp_path, monkeypatch):
    path = tmp_path / "audit.json"
    path.write_text('{"audit_date":"2026-07-12T00:00:00","total_products":3,"grade_distribution":{"A":2,"B":1},"results":[{"product":"x","grade":"B","issues":["missing test"]}]}', encoding="utf-8")
    monkeypatch.setattr(card_module, "AUDIT_REPORT_PATH", path)
    health = card_module.load_audit_health()
    assert health["healthy"] == 2
    assert health["attention"] == 1
    assert health["attention_products"] == ["x"]


def test_card_renders_audit_health_summary():
    card = card_module.build_card([], {}, [], [], audit_health={"available": True, "healthy": 2, "attention": 1, "audit_date": "2026-07-12", "attention_products": ["x"]})
    assert "质量健康" in str(card)
    assert "x" in str(card)
