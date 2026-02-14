from elkpydantic.builder import MinimalGraphIn, build_canvas
from elkpydantic.settings import sample_settings


def load_sample() -> MinimalGraphIn:
    with open("examples/example_01.json", "r", encoding="utf-8") as f:
        return MinimalGraphIn.model_validate_json(f.read())


def test_sample_build():
    data = load_sample()
    settings = sample_settings()

    canvas = build_canvas(data, settings)

    assert canvas.id == "canvas"
    assert len(canvas.children) == 2

    subgraph = next(child for child in canvas.children if child.id == "a_subgraph")
    assert subgraph.type == "subgraph"
    assert subgraph.width is None
    assert subgraph.height is None
    assert [child.id for child in subgraph.children] == ["bgp_1", "bgp_2"]

    leaf_nodes = subgraph.children + [next(child for child in canvas.children if child.id == "unconnected_router")]
    assert all(node.width is not None and node.height is not None for node in leaf_nodes)

    # Ports derived from edges
    for child in subgraph.children:
        assert len(child.ports) == 2
        for idx, port in enumerate(child.ports):
            assert port.properties.model_dump().get("org.eclipse.elk.port.index") == idx
    assert leaf_nodes[-1].ports == []

    all_ids = [c.id for c in canvas.children] + [c.id for c in subgraph.children]
    assert all(node_id == node_id.lower() for node_id in all_ids)

    # Edge wiring
    n1 = "bgp_1"
    n2 = "bgp_2"
    assert canvas.edges[0].sources == [f"{n1}_hu0_0_0_0"]
    assert canvas.edges[0].targets == [f"{n2}_hu0_0_0_0"]
    assert canvas.edges[1].sources == [f"{n1}_hu0_0_0_1"]
    assert canvas.edges[1].targets == [f"{n2}_hu0_0_0_1"]

    # Layout options sourced from settings
    assert canvas.layoutOptions.org_eclipse_elk_algorithm == "layered"


def test_subgraph_dimensions_omitted_in_payload():
    minimal = MinimalGraphIn(
        nodes=[
            {
                "l": "Cluster",
                "nodes": [{"l": "A"}, {"l": "B"}],
            }
        ],
        edges=[],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)
    payload = canvas.model_dump(by_alias=True, exclude_none=True)

    cluster = payload["children"][0]
    assert cluster["type"] == "subgraph"
    assert "width" not in cluster
    assert "height" not in cluster
    assert cluster["children"][0]["width"] == settings.node_defaults.width
    assert cluster["children"][0]["height"] == settings.node_defaults.height


def test_subgraph_type_overrides_explicit_input_type():
    minimal = MinimalGraphIn(
        nodes=[
            {
                "l": "Cluster",
                "t": "router",
                "nodes": [{"l": "A"}],
            }
        ],
        edges=[],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    assert canvas.children[0].type == "subgraph"


def test_icon_mapping():
    minimal = MinimalGraphIn(
        nodes=[{"l": "FW1", "t": "firewall"}],
        edges=[],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)
    assert canvas.children[0].icon == "clarity:firewall-line"


def test_default_icon_none():
    minimal = MinimalGraphIn(
        nodes=[{"l": "Node1"}],  # no type specified -> default
        edges=[],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)
    assert canvas.children[0].type == "default"
    assert canvas.children[0].icon is None


def test_node_to_node_edge_without_ports():
    minimal = MinimalGraphIn(
        nodes=[{"l": "A"}, {"l": "B"}],
        edges=[{"l": "link", "a": "A", "b": "B"}],  # no ports specified
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    assert canvas.children[0].ports == []
    assert canvas.children[1].ports == []
    assert canvas.edges[0].sources == [canvas.children[0].id]
    assert canvas.edges[0].targets == [canvas.children[1].id]


def test_port_name_with_colons():
    minimal = MinimalGraphIn(
        nodes=[{"l": "Router1"}, {"l": "Router2"}],
        edges=[{"l": "weird", "a": "Router1:Fo:1/0/0", "b": "Router2:Fo:2/0/0"}],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    # Port ids should include sanitized portion after first colon only
    assert canvas.edges[0].sources[0] == "router1_fo_1_0_0"
    assert canvas.edges[0].targets[0] == "router2_fo_2_0_0"


def test_icon_mapping_case_insensitive():
    minimal = MinimalGraphIn(
        nodes=[{"l": "R1", "t": "Router"}],  # capitalized type
        edges=[],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)
    assert canvas.children[0].icon == "mdi:router"


def test_toml_properties_are_flattened():
    from elkpydantic.builder import _load_settings

    settings = _load_settings("examples/example.settings.toml")

    # dotted keys preserved instead of nested objects
    assert settings.node_defaults.label.properties == {"org.eclipse.elk.font.size": 16}
    assert settings.node_defaults.port.properties == {"org.eclipse.elk.port.index": 0}
    assert settings.edge_defaults.label.properties == {
        "org.eclipse.elk.font.size": 10,
        "org.eclipse.elk.edgeLabels.inline": False,
    }
