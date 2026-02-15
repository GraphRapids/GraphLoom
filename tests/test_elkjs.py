import subprocess
from pathlib import Path
import shutil

import pytest

from elkpydantic.elkjs import layout_with_elkjs
import elkpydantic.elkjs as elkjs_mod


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


def test_layout_with_elkjs_real_node_execution_strips_internal_fields(monkeypatch, tmp_path):
    if shutil.which("node") is None:
        pytest.skip("node is required for elkjs integration test")

    workspace = tmp_path / "elkjs-workspace"
    module_dir = workspace / "node_modules" / "elkjs" / "lib"
    module_dir.mkdir(parents=True, exist_ok=True)
    (module_dir / "elk.bundled.js").write_text(
        """
module.exports = class ELK {
  async layout(graph) {
    graph.$H = 99;
    graph.children = graph.children || [];
    if (graph.children[0]) {
      graph.children[0].$H = 42;
    }
    graph.x = 1;
    return graph;
  }
};
""".strip()
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "elkpydantic.elkjs._ensure_elkjs_npm_workspace",
        lambda: workspace,
    )

    result = layout_with_elkjs({"id": "canvas", "children": [{"id": "n1"}]}, mode="npm", node_cmd="node")

    assert result["id"] == "canvas"
    assert result["x"] == 1
    assert "$H" not in result
    assert "$H" not in result["children"][0]


def test_ensure_workspace_installs_pinned_elkjs_version(monkeypatch, tmp_path):
    captured: dict[str, object] = {}

    monkeypatch.setattr(elkjs_mod.Path, "home", lambda: tmp_path)

    def fake_run(cmd, **kwargs):
        captured["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(elkjs_mod.subprocess, "run", fake_run)

    elkjs_mod._ensure_elkjs_npm_workspace()

    assert captured["cmd"][0:4] == ["npm", "install", "--no-fund", "--no-audit"]
    assert "elkjs@0.11.0" in captured["cmd"]
