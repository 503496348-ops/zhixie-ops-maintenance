import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "competitor-monitor.py"
spec = importlib.util.spec_from_file_location("competitor_monitor", MODULE_PATH)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def test_unseen_commits_uses_compare_range_and_returns_only_new_shas(monkeypatch):
    def fake_api(path):
        assert path == "/repos/acme/tool/compare/oldsha...newsha"
        return {"commits": [{"sha": "newsha"}, {"sha": "midsha"}]}

    monkeypatch.setattr(monitor, "github_api", fake_api)
    assert monitor.unseen_commit_shas("acme/tool", "oldsha", "newsha") == ["newsha", "midsha"]


def test_candidate_pool_upsert_preserves_decision_history(tmp_path, monkeypatch):
    monkeypatch.setattr(monitor, "CANDIDATE_POOL_FILE", tmp_path / "pool.json")
    first = monitor.upsert_candidate({"repo": "acme/tool", "head_sha": "abc", "status": "pending"})
    second = monitor.upsert_candidate({"repo": "acme/tool", "head_sha": "def", "status": "review"})
    assert first["status"] == "pending"
    assert second["status"] == "review"
    loaded = monitor.load_candidate_pool()
    assert loaded["candidates"]["acme/tool"]["head_sha"] == "def"
    assert len(loaded["candidates"]["acme/tool"]["history"]) == 2
