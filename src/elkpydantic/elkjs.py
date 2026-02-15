from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict

_ELKJS_NPM_SPEC = "elkjs@0.11.0"

_ELKJS_LAYOUT_SCRIPT = r"""
const fs = require('fs');

let ELK;
try {
  ELK = require('elkjs/lib/elk.bundled.js');
} catch (err) {
  ELK = require('elkjs');
}

async function main() {
  const input = fs.readFileSync(0, 'utf8');
  const graph = JSON.parse(input || '{}');
  const elk = new ELK();
  const result = await elk.layout(graph);
  process.stdout.write(JSON.stringify(result));
}

main().catch((err) => {
  const message = err && err.stack ? err.stack : String(err);
  process.stderr.write(message + '\n');
  process.exit(2);
});
""".strip()


def _elkjs_command(mode: str, node_cmd: str) -> list[str]:
    if mode == "node":
        return [node_cmd, "-e", _ELKJS_LAYOUT_SCRIPT]
    if mode in {"npm", "npx"}:
        return [node_cmd, "-e", _ELKJS_LAYOUT_SCRIPT]
    raise ValueError(f"Unsupported elkjs mode '{mode}'. Use 'node', 'npm', or 'npx'.")


def _expected_elkjs_version() -> str:
    if "@" not in _ELKJS_NPM_SPEC:
        return ""
    return _ELKJS_NPM_SPEC.split("@", 1)[1]


def _installed_elkjs_version(module_dir: Path) -> str:
    package_json = module_dir / "package.json"
    if not package_json.exists():
        return ""
    try:
        data = json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    version = data.get("version")
    return str(version) if version else ""


def _ensure_elkjs_npm_workspace() -> Path:
    workspace = Path.home() / ".cache" / "elkpydantic" / "elkjs"
    workspace.mkdir(parents=True, exist_ok=True)

    package_json = workspace / "package.json"
    if not package_json.exists():
        package_json.write_text(
            json.dumps(
                {
                    "name": "elkpydantic-elkjs-cache",
                    "private": True,
                    "description": "Local cache used by elkpydantic for elkjs layout.",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    module_dir = workspace / "node_modules" / "elkjs"
    expected_version = _expected_elkjs_version()
    if module_dir.exists() and _installed_elkjs_version(module_dir) == expected_version:
        return workspace

    try:
        proc = subprocess.run(
            ["npm", "install", "--no-fund", "--no-audit", _ELKJS_NPM_SPEC],
            cwd=str(workspace),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Failed to install elkjs automatically: 'npm' was not found in PATH.") from exc

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        raise RuntimeError(
            f"Failed to install elkjs automatically (exit {proc.returncode}).\n{stderr}"
        )

    return workspace


def _strip_elkjs_internal_fields(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: Dict[str, Any] = {}
        for key, item in value.items():
            if isinstance(key, str) and key.startswith("$"):
                continue
            cleaned[key] = _strip_elkjs_internal_fields(item)
        return cleaned
    if isinstance(value, list):
        return [_strip_elkjs_internal_fields(item) for item in value]
    return value


def layout_with_elkjs(
    graph: Dict[str, Any],
    *,
    mode: str = "node",
    node_cmd: str = "node",
) -> Dict[str, Any]:
    """Run local elkjs layout and return the positioned graph JSON.

    mode:
      - "node": requires elkjs to be available to the local node runtime.
      - "npm": auto-installs elkjs into ~/.cache/elkpydantic/elkjs when missing.
      - "npx": alias of "npm".
    """
    cmd = _elkjs_command(mode, node_cmd)
    run_cwd: str | None = None
    if mode in {"npm", "npx"}:
        run_cwd = str(_ensure_elkjs_npm_workspace())
    payload = json.dumps(graph)
    try:
        proc = subprocess.run(
            cmd,
            cwd=run_cwd,
            input=payload,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        missing = cmd[0]
        raise RuntimeError(
            f"Failed to run elkjs layout: '{missing}' was not found in PATH."
        ) from exc

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        hint = ""
        if "Cannot find module 'elkjs'" in stderr:
            hint = " Install elkjs with 'npm install elkjs' or use mode='npm'."
        raise RuntimeError(
            f"elkjs layout failed with exit code {proc.returncode}.{hint}\n{stderr}"
        )

    try:
        raw = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("elkjs returned non-JSON output.") from exc
    return _strip_elkjs_internal_fields(raw)
