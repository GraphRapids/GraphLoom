import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import graphloom.builder as builder_mod


def _write_minimal_input(path: Path) -> None:
    payload = {
        "nodes": ["A", "B"],
        "links": ["A -> B"],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _load_dev_main_module():
    module_path = Path("main.py").resolve()
    spec = importlib.util.spec_from_file_location("graphloom_dev_main", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_builder_main_writes_output_file(tmp_path):
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "out.json"
    _write_minimal_input(input_path)

    exit_code = builder_mod.main([str(input_path), "-o", str(output_path)])

    assert exit_code == 0
    output = json.loads(output_path.read_text(encoding="utf-8"))
    assert output["id"] == "canvas"
    assert len(output["children"]) == 2


def test_builder_main_layout_forwards_mode_and_node_cmd(tmp_path, monkeypatch):
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "out.json"
    _write_minimal_input(input_path)

    captured: dict[str, object] = {}

    def fake_layout(payload, *, mode, node_cmd):
        captured["mode"] = mode
        captured["node_cmd"] = node_cmd
        captured["payload_id"] = payload.get("id")
        return {"id": payload.get("id"), "layoutApplied": True}

    monkeypatch.setattr(builder_mod, "layout_with_elkjs", fake_layout)

    exit_code = builder_mod.main(
        [
            str(input_path),
            "--layout",
            "--elkjs-mode",
            "npm",
            "--node-cmd",
            "node-custom",
            "-o",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert captured == {"mode": "npm", "node_cmd": "node-custom", "payload_id": "canvas"}
    out = json.loads(output_path.read_text(encoding="utf-8"))
    assert out["layoutApplied"] is True


def test_dev_main_delegates_to_builder_main(monkeypatch):
    dev_main = _load_dev_main_module()
    captured: dict[str, object] = {}

    def fake_builder_main(argv):
        captured["argv"] = argv
        return 123

    monkeypatch.setattr(dev_main, "_builder_main", fake_builder_main)

    result = dev_main.main(["input.json"])

    assert result == 123
    assert captured["argv"] == ["input.json"]


def test_python_module_invocation_has_no_runtime_warning(tmp_path):
    input_path = tmp_path / "input.json"
    output_path = tmp_path / "out.json"
    _write_minimal_input(input_path)

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "graphloom.builder",
            str(input_path),
            "-o",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert proc.returncode == 0
    assert "RuntimeWarning" not in proc.stderr
