import subprocess

import pytest

import graphloom.elkjs as elkjs_mod


def test_elkjs_command_rejects_unsupported_mode():
    with pytest.raises(ValueError, match="Unsupported elkjs mode"):
        elkjs_mod._elkjs_command("invalid", "node")


def test_expected_elkjs_version_returns_empty_when_spec_has_no_version(monkeypatch):
    monkeypatch.setattr(elkjs_mod, "_ELKJS_NPM_SPEC", "elkjs")
    assert elkjs_mod._expected_elkjs_version() == ""


def test_installed_elkjs_version_handles_missing_and_invalid_package_json(tmp_path):
    module_dir = tmp_path / "node_modules" / "elkjs"
    module_dir.mkdir(parents=True, exist_ok=True)

    assert elkjs_mod._installed_elkjs_version(module_dir) == ""

    package_json = module_dir / "package.json"
    package_json.write_text("{invalid json", encoding="utf-8")
    assert elkjs_mod._installed_elkjs_version(module_dir) == ""

    package_json.write_text('{"version":"0.11.0"}', encoding="utf-8")
    assert elkjs_mod._installed_elkjs_version(module_dir) == "0.11.0"


def test_ensure_workspace_raises_when_npm_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(elkjs_mod.Path, "home", lambda: tmp_path)

    def fake_run(*_args, **_kwargs):
        raise FileNotFoundError("npm")

    monkeypatch.setattr(elkjs_mod.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="'npm' was not found in PATH"):
        elkjs_mod._ensure_elkjs_npm_workspace()


def test_ensure_workspace_raises_on_npm_install_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(elkjs_mod.Path, "home", lambda: tmp_path)

    def fake_run(cmd, **_kwargs):
        return subprocess.CompletedProcess(cmd, 2, "", "registry unavailable")

    monkeypatch.setattr(elkjs_mod.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="Failed to install elkjs automatically \\(exit 2\\)"):
        elkjs_mod._ensure_elkjs_npm_workspace()


def test_layout_with_elkjs_reports_missing_node_binary(monkeypatch):
    def fake_run(*_args, **_kwargs):
        raise FileNotFoundError("node")

    monkeypatch.setattr(elkjs_mod.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="was not found in PATH"):
        elkjs_mod.layout_with_elkjs({"id": "canvas"}, mode="node", node_cmd="node-missing")


def test_layout_with_elkjs_rejects_non_json_output(monkeypatch):
    def fake_run(cmd, **_kwargs):
        return subprocess.CompletedProcess(cmd, 0, "not-json", "")

    monkeypatch.setattr(elkjs_mod.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="non-JSON output"):
        elkjs_mod.layout_with_elkjs({"id": "canvas"}, mode="node", node_cmd="node")
