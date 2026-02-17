# GraphLoom

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI](https://github.com/Faerkeren/GraphLoom/actions/workflows/ci.yml/badge.svg)](https://github.com/Faerkeren/GraphLoom/actions/workflows/ci.yml)
[![Tests](https://github.com/Faerkeren/GraphLoom/actions/workflows/test.yml/badge.svg)](https://github.com/Faerkeren/GraphLoom/actions/workflows/test.yml)
[![Secret Scan](https://github.com/Faerkeren/GraphLoom/actions/workflows/gitleaks.yml/badge.svg)](https://github.com/Faerkeren/GraphLoom/actions/workflows/gitleaks.yml)

GraphLoom enriches minimal graph JSON/YAML into fully-formed [ELK](https://www.eclipse.org/elk/) JSON.

It is designed for topology authoring workflows where source input should stay compact while node/port/edge defaults and layout options remain centralized.

## Features

- Minimal authoring format for nodes and links
- Link shorthand support (`"A:eth0 -> B:eth1"`)
- Automatic node and port creation from edge endpoints
- Type-to-icon mapping through settings
- Settings-driven node, edge, label, and layout defaults
- Optional local `elkjs` layout execution from CLI or Python API

## Requirements

- Python `>=3.10`
- `pydantic>=2`, `pydantic-settings>=2`, `PyYAML>=6`
- Optional: Node.js + npm when using `--layout`

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Quick Start

```bash
# Build enriched ELK JSON from minimal YAML input
graphloom examples/example_01.yaml -s examples/example.settings.toml -o /tmp/elk.json

# Build and run local elkjs layout
graphloom examples/example_01.yaml -s examples/example.settings.toml --layout -o /tmp/laid-out.json

# Save both enriched and laid-out payloads in one run
graphloom examples/example_01.yaml \
  -s examples/example.settings.toml \
  --layout \
  --enriched-output /tmp/enriched.json \
  -o /tmp/layout.json
```

## CLI Reference

```bash
graphloom <input.json|input.yaml> [-s settings.toml|settings.json] [-o output.json] [--enriched-output path] [--layout] [--elkjs-mode node|npm|npx] [--node-cmd node]
```

- `input`: minimal graph JSON/YAML file
- `-s`, `--settings`: optional settings file (`.toml` or `.json`)
- `-o`, `--output`: output ELK JSON path (stdout if omitted)
- `--enriched-output`: output pre-layout enriched JSON
- `--layout`: run local `elkjs` before writing final output
- `--elkjs-mode`: `node` (default), `npm`, or `npx` (alias of `npm`)
- `--node-cmd`: Node.js executable path/name (default `node`)

## Python API

```python
from graphloom import MinimalGraphIn, build_canvas, layout_with_elkjs, sample_settings

minimal = MinimalGraphIn.model_validate({
    "nodes": ["A", "B"],
    "links": ["A:eth0 -> B:eth1"],
})

canvas = build_canvas(minimal, sample_settings())
payload = canvas.model_dump(by_alias=True, exclude_none=True)

# Optional local layout
laid_out = layout_with_elkjs(payload, mode="node")
```

## Input Expectations

GraphLoom expects minimal graph authoring input:

- `nodes[]`: string or object (`name`, `type`, `id`, nested `nodes`, nested `links`)
- `links[]`: string shorthand or object (`id`, `label`, `type`, `from`, `to`)

Validation rules:

- Node name length: `1..20`, and must not contain `:`
- Port name length in endpoints: `1..15`
- Edge label length (when provided): `1..40`
- Graph must include at least one node or one link

Bundled schema:

- `src/graphloom/schemas/minimal-input.schema.json`

## Settings

Settings can be loaded from TOML/JSON and control all defaults:

- `layout_options`
- `node_defaults`
- `subgraph_defaults`
- `edge_defaults`
- `edge_type_overrides`
- `type_overrides`
- `type_icon_map`
- `auto_create_missing_nodes`
- `estimate_label_size_from_font`

Precedence:

- Node style: role defaults (`node_defaults` / `subgraph_defaults`) then `type_overrides`
- Edge style: `edge_defaults` then `edge_type_overrides`
- Edge label text: explicit `label`, then `edge_defaults.label.text`

## Troubleshooting

### `Unsupported input format`

Use `.json`, `.yaml`, or `.yml` inputs.

### `PyYAML is required for YAML input`

Install dependencies in editable mode:

```bash
python -m pip install -e .
```

### `Cannot find module 'elkjs'`

Either install `elkjs` in your Node environment or use:

```bash
graphloom ... --layout --elkjs-mode npm
```

## Development

```bash
python -m pytest -q
python -m graphloom.builder examples/example_01.yaml -s examples/example.settings.toml -o /tmp/graphloom-check.json
```

## Project Layout

```text
main.py                             # Local development entrypoint
src/graphloom/                      # Library code
src/graphloom/schemas/              # Input schema
examples/                           # Sample inputs/settings
tests/                              # Pytest suite
```

## Governance and Community

- Security policy: `SECURITY.md`
- Contribution guide: `CONTRIBUTING.md`
- Code of conduct: `CODE_OF_CONDUCT.md`
- Changelog: `CHANGELOG.md`
- Release process: `RELEASE.md`

## Automation

- CI build and sanity checks: `.github/workflows/ci.yml`
- Test matrix + coverage gate: `.github/workflows/test.yml`
- Secret scanning (gitleaks): `.github/workflows/gitleaks.yml`
- Tagged releases: `.github/workflows/release.yml`
- Dependency updates: `.github/dependabot.yml`

## Acknowledgements

- [Eclipse Layout Kernel (ELK)](https://www.eclipse.org/elk/)
- [elkjs](https://github.com/kieler/elkjs)
- [Pydantic](https://github.com/pydantic/pydantic)
- [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- [PyYAML](https://github.com/yaml/pyyaml)

## Third-Party Notices

See `THIRD_PARTY_NOTICES.md` for dependency and license notices.

## License

GraphLoom is licensed under Apache License 2.0. See `LICENSE`.
