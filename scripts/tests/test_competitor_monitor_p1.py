import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "competitor-monitor.py"
spec = importlib.util.spec_from_file_location("competitor_monitor_p1", MODULE_PATH)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


def test_semantic_change_signals_detect_runtime_schema_permission_and_symbols():
    files = [
        {"filename": "src/runtime/router.py", "patch": "+class ToolRouter:\n+    def dispatch(self):\n+        pass"},
        {"filename": "api/openapi/schema.json", "patch": "+{\"type\": \"object\"}"},
        {"filename": "config/permissions.yaml", "patch": "+permissions:\n+  - network:egress"},
        {"filename": "tests/test_router.py", "patch": "+def test_dispatch():\n+    assert True"},
    ]
    signals = monitor.semantic_change_signals(files)
    assert {"runtime", "schema", "permission", "test_harness", "new_symbol"} <= set(signals["tags"])
    assert signals["new_symbols"] == ["ToolRouter", "dispatch", "test_dispatch"]


def test_candidate_status_maps_triage_to_a_state_machine():
    assert monitor.candidate_state("可融合候选") == "pending_review"
    assert monitor.candidate_state("观察/人工复核") == "watching"
    assert monitor.candidate_state("仅记录") == "recorded"
