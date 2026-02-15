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


def test_minimal_input_schema_disallows_colon_in_node_names():
    schema = _load_schema()
    node_def = schema["$defs"]["MinimalNodeIn"]

    assert node_def["properties"]["name"]["pattern"] == "^[^:]*$"

    top_level_node_string_schema = next(
        item
        for item in schema["properties"]["nodes"]["items"]["anyOf"]
        if item.get("type") == "string"
    )
    nested_node_string_schema = next(
        item
        for item in node_def["properties"]["nodes"]["items"]["anyOf"]
        if item.get("type") == "string"
    )

    assert top_level_node_string_schema["pattern"] == "^[^:]*$"
    assert nested_node_string_schema["pattern"] == "^[^:]*$"


def test_minimal_input_schema_enforces_name_length_limits():
    schema = _load_schema()
    node_def = schema["$defs"]["MinimalNodeIn"]
    edge_def = schema["$defs"]["MinimalEdgeIn"]

    node_name = node_def["properties"]["name"]
    edge_label = edge_def["properties"]["label"]["anyOf"][0]

    assert node_name["minLength"] == 1
    assert node_name["maxLength"] == 20
    assert edge_label["minLength"] == 1
    assert edge_label["maxLength"] == 40

    from_endpoint = edge_def["properties"]["from"]
    to_endpoint = edge_def["properties"]["to"]
    endpoint_pattern = "^[^:]{1,20}(:[^:]{1,15})?$"

    assert from_endpoint["minLength"] == 1
    assert from_endpoint["maxLength"] == 36
    assert from_endpoint["pattern"] == endpoint_pattern
    assert to_endpoint["minLength"] == 1
    assert to_endpoint["maxLength"] == 36
    assert to_endpoint["pattern"] == endpoint_pattern
