import json
from pathlib import Path


def _load_schema() -> dict:
    schema_path = Path("examples/minimal-input.schema.json")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def test_minimal_input_schema_is_canonical_only_top_level():
    schema = _load_schema()

    assert schema.get("additionalProperties") is False
    assert set(schema["properties"].keys()) == {"nodes", "links"}


def test_minimal_input_schema_rejects_alias_keys_for_nodes_and_edges():
    schema = _load_schema()

    node_def = schema["$defs"]["MinimalNodeIn"]
    edge_def = schema["$defs"]["MinimalEdgeIn"]

    assert node_def.get("additionalProperties") is False
    assert edge_def.get("additionalProperties") is False

    node_keys = set(node_def["properties"].keys())
    edge_keys = set(edge_def["properties"].keys())

    assert {"name", "type", "id", "nodes", "links"} <= node_keys
    assert not {"l", "t", "edges"}.intersection(node_keys)

    assert {"label", "type", "id", "from", "to"} <= edge_keys
    assert not {"name", "l", "t", "a", "b"}.intersection(edge_keys)
