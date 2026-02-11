# ElkPydantic
Enrich minimal graph JSON into fully-formed [ELK](https://www.eclipse.org/elk/) JSON using Pydantic.  
Focus: keep authoring input tiny; derive ports/nodes from edges; centralize defaults in settings.

## What it does
- Accepts **minimal input**: nodes with labels/types, edges with endpoints like `NodeA:Eth0`.
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
elkpydantic json/sample_input_01.json \
  -s json/elk_settings.example.toml \
  -o /tmp/elk.json

# Or directly
python -m elkpydantic.builder json/sample_input_01.json -s json/elk_settings.example.toml
```
Flags:
- `-i/--input` minimal graph JSON (default `json/sample_input_01.json`)
- `-s/--settings` settings TOML/JSON (default `json/elk_settings.example.toml`; falls back to built-in sample if missing)
- `-o/--output` write to file (stdout if omitted)

## Library usage
```python
from elkpydantic import MinimalGraphIn, build_canvas, sample_settings

minimal = MinimalGraphIn.model_validate({
    "nodes": [{"l": "BGP 1", "t": "router"}],
    "edges": [{"l": "uplink", "a": "BGP 1:xe-0/0/0", "b": "BGP 2:xe-0/0/1"}],
})
settings = sample_settings()  # or ElkSettings.model_validate_file(...)
canvas = build_canvas(minimal, settings)
elk_json = canvas.model_dump_json(indent=2, by_alias=True)
```

## Minimal input schema
- **nodes[]**: `{ "l": "<label>", "t": "<type>", "id": "<optional custom id>" }`
- **edges[]**: `{ "l": "<label>", "t": "<class>", "a": "Node:Port", "b": "Node:Port" }`
Unknown nodes referenced in edges are auto-created when `auto_create_missing_nodes` is true (default).

## Settings (TOML/JSON or env, see `json/elk_settings.example.toml`)
- `layout_options`: ELK keys (flattened by builder) e.g. `org.eclipse.elk.algorithm`.
- `node_defaults`: sizes, label defaults, port defaults, properties; `type="default"`, `icon=""` (None).
- `edge_defaults`: label defaults and properties.
- `type_overrides`: per-type full NodeDefaults block.
- `type_icon_map`: mapping type → icon (full list in example file).
- `auto_create_missing_nodes`: bool.

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
- Example run: `elkpydantic json/sample_input_01.json -s json/elk_settings.example.toml`
