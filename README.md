# ElkPydantic
Enriches minimal JSON input to valid ELK JSON output

## Usage
```bash
python -m elkpydantic.builder json/sample_input_01.json -o /tmp/elk.json -s json/elk_settings.example.toml
```

## Concepts
- Provide a minimal graph JSON: nodes with labels/types and edges with endpoints like `NodeA:Eth0`.
- Defaults (sizes, fonts, layout options, port/node properties) live in a settings file, not in the models.
- Ports are generated from edge endpoints; nodes/ports are auto-created when referenced.
