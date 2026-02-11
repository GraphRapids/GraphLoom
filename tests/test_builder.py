import json

from elkpydantic.builder import MinimalGraphIn, build_canvas
from elkpydantic.settings import sample_settings


def load_sample() -> MinimalGraphIn:
    with open("json/sample_input_01.json", "r", encoding="utf-8") as f:
        return MinimalGraphIn.model_validate_json(f.read())


def test_sample_build():
    data = load_sample()
    settings = sample_settings()

    canvas = build_canvas(data, settings)

    assert canvas.id == "canvas"
    assert len(canvas.children) == 2

    child_ids = [c.id for c in canvas.children]
    assert all(cid == cid.lower() for cid in child_ids)

    # Ports derived from edges
    for child in canvas.children:
        assert len(child.ports) == 2
        for idx, port in enumerate(child.ports):
            assert port.properties.model_dump().get("port.index") == idx

    # Edge wiring
    n1 = "bgp_router_1"
    n2 = "bgp_router_2"
    assert canvas.edges[0].sources == [f"{n1}_hu0_0_0_0"]
    assert canvas.edges[0].targets == [f"{n2}_hu0_0_0_0"]
    assert canvas.edges[1].sources == [f"{n1}_hu0_0_0_1"]
    assert canvas.edges[1].targets == [f"{n2}_hu0_0_0_1"]

    # Layout options sourced from settings
    assert canvas.layoutOptions.org_eclipse_elk_algorithm == "layered"


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
