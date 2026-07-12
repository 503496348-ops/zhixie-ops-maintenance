import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "competitor-monitor.py"
spec = importlib.util.spec_from_file_location("competitor_monitor_p2", MODULE_PATH)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def test_trend_windows_calculate_star_growth_from_history():
    history = [
        {"generated_at": "2026-06-12T00:00:00+00:00", "repos": {"acme/tool": {"stars": 100}}},
        {"generated_at": "2026-07-05T00:00:00+00:00", "repos": {"acme/tool": {"stars": 120}}},
        {"generated_at": "2026-07-11T00:00:00+00:00", "repos": {"acme/tool": {"stars": 127}}},
    ]
    trend = monitor.trend_windows("acme/tool", 130, history, "2026-07-12T00:00:00+00:00")
    assert trend == {"stars_7d": 10, "stars_30d": 30}


def test_release_summary_handles_missing_release_without_failure(monkeypatch):
    monkeypatch.setattr(monitor, "github_api", lambda path: {"message": "Not Found"})
    assert monitor.fetch_release_summary("acme/tool") == {"tag": "", "published_at": ""}
    assert monitor.fetch_security_policy("acme/tool") is False
