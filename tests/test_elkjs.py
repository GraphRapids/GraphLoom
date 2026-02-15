import subprocess
from pathlib import Path

import pytest

from elkpydantic.elkjs import layout_with_elkjs


def test_layout_with_elkjs_node_mode_uses_node_command(monkeypatch):
    captured: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["input"] = kwargs["input"]
        assert kwargs["capture_output"] is True
        assert kwargs["text"] is True
        assert kwargs["check"] is False
        assert kwargs["cwd"] is None
        return subprocess.CompletedProcess(cmd, 0, '{"id":"canvas","x":12}', "")

    monkeypatch.setattr("elkpydantic.elkjs.subprocess.run", fake_run)

    result = layout_with_elkjs({"id": "canvas"}, mode="node", node_cmd="node")

    assert result["id"] == "canvas"
    assert result["x"] == 12
    assert captured["cmd"][0:2] == ["node", "-e"]


def test_layout_with_elkjs_npx_mode_uses_cached_npm_workspace(monkeypatch):
    captured: dict[str, object] = {}

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        captured["cwd"] = kwargs["cwd"]
        return subprocess.CompletedProcess(cmd, 0, '{"id":"canvas"}', "")

    monkeypatch.setattr("elkpydantic.elkjs.subprocess.run", fake_run)
    monkeypatch.setattr(
        "elkpydantic.elkjs._ensure_elkjs_npm_workspace",
        lambda: Path("/tmp/elkpydantic-elkjs-cache"),
    )

    result = layout_with_elkjs({"id": "canvas"}, mode="npx", node_cmd="node")

    assert result["id"] == "canvas"
    assert captured["cmd"][0:2] == ["node", "-e"]
    assert captured["cwd"] == "/tmp/elkpydantic-elkjs-cache"


def test_layout_with_elkjs_reports_missing_elkjs_module(monkeypatch):
    def fake_run(cmd, **kwargs):
        stderr = "Error: Cannot find module 'elkjs'"
        return subprocess.CompletedProcess(cmd, 1, "", stderr)

    monkeypatch.setattr("elkpydantic.elkjs.subprocess.run", fake_run)

    with pytest.raises(RuntimeError, match="Install elkjs with 'npm install elkjs' or use mode='npm'"):
        layout_with_elkjs({"id": "canvas"}, mode="node", node_cmd="node")
