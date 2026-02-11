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
