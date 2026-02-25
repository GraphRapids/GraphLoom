# GraphLoom - Project Context

## Purpose
GraphLoom converts minimal graph JSON/YAML into enriched ELK JSON, applying defaults, validation, and optional local ELKJS layout.

## Primary Goals
- Keep authoring input compact while producing deterministic enriched output.
- Apply schema/domain validation with clear errors.
- Keep settings-driven defaults centralized and composable.
- Support optional local layout execution for end-to-end pipelines.

## Package Snapshot
- Python package: `graphloom`
- Entry points:
  - `graphloom` CLI
  - `main.py`
- Core source:
  - `src/graphloom/`
  - `src/graphloom/schemas/minimal-input.schema.json`

## Contract Surface
Core inputs:
- `nodes`: string/object forms, including nested `nodes` and `links`
- `links`: shorthand (`A:eth0 -> B:eth1`) or object forms

Core outputs:
- Enriched ELK-compatible JSON payload.
- Optional laid-out ELK payload when `--layout` is enabled.

Behavior expectations:
- Auto-create missing nodes/ports from link endpoints (subject to settings).
- Keep output deterministic for identical input/settings.
- Preserve explicit user-provided values over defaults.

## Settings Contract
Primary settings groups:
- `layout_options`
- `node_defaults` / `subgraph_defaults`
- `edge_defaults` / `edge_type_overrides`
- `type_overrides` / `type_icon_map`
- `auto_create_missing_nodes`

## Integration Notes
- Upstream authoring: GraphEditor / GraphYamlEditor.
- Downstream render: GraphRender.
- API exposure and orchestration: GraphAPI.
- Theme metrics source: GraphTheme.

## Testing Expectations
- `python -m pytest -q`
- `python -m graphloom.builder examples/example_01.yaml -s examples/example.settings.toml -o /tmp/graphloom-check.json`

## Open Decisions / TODO
- [ ] Expand schema + tests for recursive subgraph edge-case validation.
- [ ] Add golden tests for enriched payload stability across settings changes.
- [ ] Define compatibility/versioning policy for minimal input schema evolution.

## How To Maintain This File
- Update after schema, settings, validation, or output behavior changes.
- Keep contracts mapped to real files and runtime behavior.
