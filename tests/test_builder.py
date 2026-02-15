import pytest
from pydantic import ValidationError

from elkpydantic.builder import MinimalGraphIn, build_canvas
from elkpydantic.settings import ElkSettings, sample_settings


def load_sample() -> MinimalGraphIn:
    with open("examples/example_01.json", "r", encoding="utf-8") as f:
        return MinimalGraphIn.model_validate_json(f.read())


def test_sample_build():
    data = load_sample()
    settings = sample_settings()

    canvas = build_canvas(data, settings)

    assert canvas.id == "canvas"
    assert len(canvas.children) == 3

    subgraph = next(child for child in canvas.children if child.id == "subgraph_1")
    assert subgraph.type == "subgraph"
    assert subgraph.width is None
    assert subgraph.height is None
    assert [child.id for child in subgraph.children] == ["node_1", "node_2"]
    assert len(subgraph.edges) == 1
    assert subgraph.edges[0].sources == ["node_1_hu0_0_0_0"]
    assert subgraph.edges[0].targets == ["node_2_hu0_0_0_0"]
    assert subgraph.edges[0].labels[0].text == "Fabric 1"
    assert subgraph.edges[0].properties.model_dump().get("elkpydantic.edgeType") == "100G"
    assert subgraph.children[0].type == "router"
    assert subgraph.children[1].type == "switch"

    node_3 = next(child for child in canvas.children if child.id == "node_3")
    node_4 = next(child for child in canvas.children if child.id == "node_4")
    leaf_nodes = subgraph.children + [node_3, node_4]
    assert all(node.width is not None and node.height is not None for node in leaf_nodes)
    assert node_3.type == "router"
    assert node_4.type == "firewall"

    # Ports derived from edges
    for child in subgraph.children:
        assert len(child.ports) == 1
        for idx, port in enumerate(child.ports):
            assert port.properties.model_dump().get("org.eclipse.elk.port.index") == idx
    assert len(node_3.ports) == 1
    assert len(node_4.ports) == 1

    all_ids = [c.id for c in canvas.children] + [c.id for c in subgraph.children]
    assert all(node_id == node_id.lower() for node_id in all_ids)

    # Edge wiring
    assert canvas.edges[0].sources == ["subgraph_1"]
    assert canvas.edges[0].targets == ["node_3"]
    assert canvas.edges[1].sources == ["node_3_eth0"]
    assert canvas.edges[1].targets == ["node_4_eth1"]
    assert canvas.edges[0].labels[0].text == "Uplink 1"
    assert canvas.edges[1].labels[0].text == settings.edge_defaults.label.text
    assert canvas.edges[0].properties.model_dump().get("elkpydantic.edgeType") == "MPLS"

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


def test_new_field_aliases_name_type_from_to():
    minimal = MinimalGraphIn(
        nodes=[{"name": "A"}, {"name": "B"}],
        edges=[{"name": "link", "from": "A", "to": "B"}],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    assert canvas.edges[0].sources == ["a"]
    assert canvas.edges[0].targets == ["b"]


def test_node_name_rejects_colon():
    with pytest.raises(ValidationError, match="Node name cannot contain ':'"):
        MinimalGraphIn.model_validate(
            {
                "nodes": [{"name": "A:B"}],
                "links": [],
            }
        )

    with pytest.raises(ValidationError, match="Node name cannot contain ':'"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A:B"],
                "links": [],
            }
        )


def test_name_length_constraints_for_node_port_and_edge():
    MinimalGraphIn.model_validate(
        {
            "nodes": [{"name": "N" * 20}, {"name": "B"}],
            "links": [{"label": "E" * 40, "from": "N" * 20, "to": "B:" + ("p" * 15)}],
        }
    )

    with pytest.raises(ValidationError, match="Node name must be between 1 and 20 characters"):
        MinimalGraphIn.model_validate({"nodes": [{"name": ""}], "links": []})

    with pytest.raises(ValidationError, match="Node name must be between 1 and 20 characters"):
        MinimalGraphIn.model_validate({"nodes": [{"name": "N" * 21}], "links": []})

    with pytest.raises(ValidationError, match="Port name must be between 1 and 15 characters"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A", "B"],
                "links": [{"from": "A:" + ("p" * 16), "to": "B"}],
            }
        )

    with pytest.raises(ValidationError, match="Port name must be between 1 and 15 characters"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A", "B"],
                "links": [{"from": "A:", "to": "B"}],
            }
        )

    with pytest.raises(ValidationError, match="Edge name must be between 1 and 40 characters"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A", "B"],
                "links": [{"label": "", "from": "A", "to": "B"}],
            }
        )

    with pytest.raises(ValidationError, match="Edge name must be between 1 and 40 characters"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A", "B"],
                "links": [{"label": "E" * 41, "from": "A", "to": "B"}],
            }
        )

    with pytest.raises(ValidationError, match="Edge name must be between 1 and 40 characters"):
        MinimalGraphIn.model_validate(
            {
                "nodes": ["A", "B"],
                "links": [{"name": "E" * 41, "from": "A", "to": "B"}],
            }
        )


def test_links_alias_and_string_shorthand():
    minimal = MinimalGraphIn(
        nodes=["A", "B"],
        links=["A:eth0 -> B:eth1"],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    assert canvas.edges[0].sources == ["a_eth0"]
    assert canvas.edges[0].targets == ["b_eth1"]
    assert canvas.edges[0].labels[0].text == settings.edge_defaults.label.text


def test_edge_label_prefers_label_field_over_name():
    minimal = MinimalGraphIn(
        nodes=["A", "B"],
        links=[{"name": "Legacy Name", "label": "Preferred Label", "from": "A", "to": "B"}],
    )
    settings = sample_settings()
    canvas = build_canvas(minimal, settings)

    assert canvas.edges[0].labels[0].text == "Preferred Label"
    assert canvas.edges[0].id == "preferred_label"


def test_edge_type_overrides_apply_for_matching_type():
    minimal = MinimalGraphIn(
        nodes=["A", "B"],
        links=[{"type": "100G", "from": "A", "to": "B"}],
    )
    settings = sample_settings()
    override = settings.edge_defaults.model_copy(deep=True)
    override.label.text = "100G default label"
    override.label.width = 222
    override.properties["org.eclipse.elk.edge.thickness"] = 7
    settings.edge_type_overrides["100g"] = override

    canvas = build_canvas(minimal, settings)

    assert canvas.edges[0].labels[0].text == "100G default label"
    assert canvas.edges[0].labels[0].width == 222
    assert canvas.edges[0].properties.model_dump()["org.eclipse.elk.edge.thickness"] == 7
    assert canvas.edges[0].properties.model_dump()["elkpydantic.edgeType"] == "100G"


def test_role_defaults_apply_separately_for_subgraph_and_leaf_nodes():
    minimal = MinimalGraphIn(
        nodes=[
            {
                "l": "Cluster",
                "nodes": [{"l": "Leaf"}],
            }
        ],
        edges=[],
    )
    settings = sample_settings()
    settings.node_defaults.label.width = 111
    settings.node_defaults.icon = "leaf-icon"
    assert settings.subgraph_defaults is not None
    settings.subgraph_defaults.label.width = 222
    settings.subgraph_defaults.icon = "subgraph-icon"

    canvas = build_canvas(minimal, settings)

    cluster = canvas.children[0]
    leaf = cluster.children[0]
    assert cluster.type == "subgraph"
    assert cluster.labels[0].width == 222
    assert cluster.icon == "subgraph-icon"
    assert leaf.labels[0].width == 111
    assert leaf.icon == "leaf-icon"


def test_subgraph_defaults_fallback_to_node_defaults_when_omitted():
    raw = sample_settings().model_dump()
    raw.pop("subgraph_defaults", None)
    settings = ElkSettings.model_validate(raw)

    minimal = MinimalGraphIn(
        nodes=[{"l": "Cluster", "nodes": [{"l": "Leaf"}]}],
        edges=[],
    )
    canvas = build_canvas(minimal, settings)

    cluster = canvas.children[0]
    assert cluster.type == "subgraph"
    assert cluster.labels[0].width == settings.node_defaults.label.width


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


def test_port_name_with_colons_is_rejected():
    with pytest.raises(ValidationError, match="Port name cannot contain ':'"):
        MinimalGraphIn(
            nodes=[{"l": "Router1"}, {"l": "Router2"}],
            edges=[{"l": "weird", "a": "Router1:Fo:1/0/0", "b": "Router2:Fo:2/0/0"}],
        )


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
    assert settings.subgraph_defaults is not None
    assert settings.subgraph_defaults.width is None
    assert settings.subgraph_defaults.height is None
    assert settings.subgraph_defaults.label.properties == {"org.eclipse.elk.font.size": 20}
    assert settings.subgraph_defaults.port.properties == {"org.eclipse.elk.port.index": 0}
    assert settings.edge_defaults.label.properties == {
        "org.eclipse.elk.font.size": 10,
        "org.eclipse.elk.edgeLabels.inline": False,
    }
    assert settings.edge_type_overrides["100g"].label.properties == {
        "org.eclipse.elk.font.size": 11,
        "org.eclipse.elk.edgeLabels.inline": False,
    }
    assert settings.edge_type_overrides["100g"].properties == {
        "org.eclipse.elk.edge.type": "UNDIRECTED",
        "org.eclipse.elk.edge.thickness": 3,
    }


def test_yaml_input_loader():
    from elkpydantic.builder import _load_input

    data = _load_input("examples/example_01.yaml")
    settings = sample_settings()
    canvas = build_canvas(data, settings)

    assert len(canvas.children) == 3
    assert len(canvas.edges) == 2


def test_layout_options_are_not_merged_into_node_properties():
    minimal = MinimalGraphIn(
        nodes=["A"],
        edges=[],
    )
    settings = sample_settings()
    settings.layout_options["org.eclipse.elk.nodeLabels.placement"] = "[OUTSIDE]"
    settings.node_defaults.properties.pop("org.eclipse.elk.nodeLabels.placement", None)

    canvas = build_canvas(minimal, settings)
    payload = canvas.model_dump(by_alias=True, exclude_none=True)

    assert payload["layoutOptions"]["org.eclipse.elk.nodeLabels.placement"] == "[OUTSIDE]"
    assert "org.eclipse.elk.nodeLabels.placement" not in payload["children"][0]["properties"]
