# ElkPydantic
Enrich minimal graph JSON into fully-formed [ELK](https://www.eclipse.org/elk/) JSON using Pydantic.  
Focus: keep authoring input tiny; derive ports/nodes from edges; centralize defaults in settings.

## What it does
- Accepts **minimal input JSON/YAML**: nodes and links with endpoints like `NodeA:Eth0`.
- Supports shorthand for readability: node strings (`"Node A"`) and link strings (`"Node A:eth0 -> Node B:eth1"`).
- **Auto-creates ports and nodes** from edge endpoints; preserves port order and sets `port.index`.
- **Type→icon mapping**: picks icons from settings map (see below) or leaves icon `null` for default type.
- All **layout options, sizes, fonts, properties** come from settings (TOML/JSON or env), not hardcoded.
- Emits **ELK JSON** with proper aliases for layout keys.

## Install
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

## CLI usage
```bash
# Using installed console script
elkpydantic examples/example_01.json \
  -s examples/example.settings.toml \
  -o /tmp/elk.json

# YAML input works too
elkpydantic examples/example_01.yaml \
  -s examples/example.settings.toml \
  -o /tmp/elk.json

# Or directly
python -m elkpydantic.builder examples/example_01.json -s examples/example.settings.toml
```
Flags:
- `input` minimal graph JSON/YAML (required positional arg)
- `-s/--settings` settings TOML/JSON (optional; uses built-in sample settings when omitted)
- `-o/--output` write to file (stdout if omitted)

## Library usage
```python
from elkpydantic import MinimalGraphIn, build_canvas, sample_settings

minimal = MinimalGraphIn.model_validate({
    "nodes": [
        {
            "name": "Subgraph 1",
            "nodes": [{"name": "Node 1", "type": "router"}, {"name": "Node 2", "type": "switch"}],
            "links": [{"label": "Fabric 1", "type": "100G", "from": "Node 1:xe0", "to": "Node 2:xe0"}],
        },
        {"name": "Node 3", "type": "router"},
    ],
    "links": [{"label": "Uplink 1", "type": "MPLS", "from": "Subgraph 1", "to": "Node 3"}],
})
settings = sample_settings()  # or ElkSettings.model_validate_file(...)
canvas = build_canvas(minimal, settings)
elk_json = canvas.model_dump_json(indent=2, by_alias=True)
```

### Library usage with YAML input
```python
from pathlib import Path

import yaml

from elkpydantic import MinimalGraphIn, build_canvas, sample_settings

yaml_path = Path("examples/example_01.yaml")
raw = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}

minimal = MinimalGraphIn.model_validate(raw)
settings = sample_settings()
canvas = build_canvas(minimal, settings)

payload = canvas.model_dump(by_alias=True, exclude_none=True)
elk_json = canvas.model_dump_json(indent=2, by_alias=True)
```

## Minimal input schema
- **nodes[]**: either a string (`"Node 1"`) or `{ "name": "<label>", "type": "<type>", "id": "<optional custom id>", "nodes": [ ... ], "links": [ ... ] }`
  - `nodes` and `links` on a node define a recursive subgraph scope.
  - Subgraph nodes are emitted without `width`/`height`, and carry nested `children` + `edges` in output.
- **links[] / edges[]**: each item can be:
  - string shorthand: `"Node A:eth0 -> Node B:eth1"`
  - object: `{ "label": "<optional edge label>", "type": "<optional link type>", "from": "Node:Port", "to": "Node:Port" }`
Unknown nodes referenced in edges are auto-created when `auto_create_missing_nodes` is true (default).
- JSON Schema: `examples/minimal-input.schema.json`

Backwards-compatible aliases are accepted for input:
- node: `l` -> `name`, `t` -> `type`
- edge: `l`/`name` -> `label`, `t` -> `type`, `a` -> `from`, `b` -> `to`

## Settings (TOML/JSON or env)
See `examples/example.settings.toml`
- `layout_options`: canvas-level ELK keys only (for root `layoutOptions`), e.g. `org.eclipse.elk.algorithm`.
- `node_defaults`: defaults for leaf nodes; sizes, label defaults, port defaults, properties; `type="default"`, `icon=""` (None).
- `subgraph_defaults`: defaults for subgraph nodes (nodes with children). `width`/`height` are optional and ignored for subgraphs.
- `edge_defaults`: label defaults and properties.
- `edge_type_overrides`: per-type EdgeDefaults block (for example `100g`, `mpls`).
- `type_overrides`: per-type full NodeDefaults block.
- `type_icon_map`: mapping type → icon (full list in example file).
- `auto_create_missing_nodes`: bool.

Precedence:
- Node styling and node-level ELK options: role defaults (`node_defaults`/`subgraph_defaults`) then `type_overrides` for the effective type.
- Edge styling: `edge_defaults` then `edge_type_overrides` (when edge `type` matches).
- Edge label text: explicit `label`, then fallback to `edge_defaults.label.text`.

### Type→icon mapping (excerpt)
```
router=mdi:router
switch=clarity:network-switch-line
firewall=clarity:firewall-line
cloud=material-symbols:cloud-outline
...
ubiquiti=simple-icons:ubiquiti
```
Default type is `default` with no icon; mapping wins when present, otherwise override, otherwise None.

## Development
- Run tests: `. .venv/bin/activate && pytest -q`
- Example run: `elkpydantic examples/example_01.yaml -s examples/example.settings.toml`
