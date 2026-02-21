import json

import pytest
from pydantic import ValidationError

import graphloom.builder as builder_mod
from graphloom import MinimalGraphIn, sample_settings
from graphloom.base import Properties


def _write_json(path, payload) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_parse_link_shorthand_rejects_missing_arrow():
    with pytest.raises(ValueError, match="Invalid link shorthand"):
        builder_mod._parse_link_shorthand("A to B")


def test_parse_link_shorthand_rejects_missing_source_or_target():
    with pytest.raises(ValueError, match="Both source and target must be present"):
        builder_mod._parse_link_shorthand(" -> B")
    with pytest.raises(ValueError, match="Both source and target must be present"):
        builder_mod._parse_link_shorthand("A -> ")


def test_normalizers_handle_none_for_nested_and_top_level_collections():
    node = builder_mod.MinimalNodeIn.model_validate({"name": "A", "nodes": None, "links": None})
    assert node.nodes == []
    assert node.links == []

    graph_with_none_nodes = builder_mod.MinimalGraphIn.model_validate(
        {"nodes": None, "links": [{"from": "A", "to": "B"}]}
    )
    assert graph_with_none_nodes.nodes == []

    graph_with_none_links = builder_mod.MinimalGraphIn.model_validate({"nodes": ["A"], "links": None})
    assert graph_with_none_links.links == []


def test_normalizers_passthrough_non_list_values_to_pydantic_validation():
    with pytest.raises(ValidationError):
        builder_mod.MinimalNodeIn.model_validate({"name": "A", "nodes": {}, "links": []})
    with pytest.raises(ValidationError):
        builder_mod.MinimalNodeIn.model_validate({"name": "A", "nodes": [], "links": {}})
    with pytest.raises(ValidationError):
        builder_mod.MinimalGraphIn.model_validate({"nodes": {}, "links": [{"from": "A", "to": "B"}]})
    with pytest.raises(ValidationError):
        builder_mod.MinimalGraphIn.model_validate({"nodes": ["A"], "links": {}})


def test_load_settings_json_flattens_layout_and_properties(tmp_path):
    settings_data = sample_settings().model_dump()
    settings_data["layout_options"] = {
        "org": {
            "eclipse": {
                "elk": {
                    "algorithm": "layered",
                    "direction": "RIGHT",
                }
            }
        }
    }
    settings_data["node_defaults"]["label"]["properties"] = {
        "org": {
            "eclipse": {
                "elk": {
                    "font": {
                        "name": "Arial",
                        "size": 16,
                    }
                }
            }
        }
    }

    path = tmp_path / "settings.json"
    _write_json(path, settings_data)

    settings = builder_mod._load_settings(str(path))

    assert settings.layout_options["org.eclipse.elk.algorithm"] == "layered"
    assert settings.layout_options["org.eclipse.elk.direction"] == "RIGHT"
    assert settings.node_defaults.label.properties == {
        "org.eclipse.elk.font.name": "Arial",
        "org.eclipse.elk.font.size": 16,
    }


def test_load_settings_rejects_unsupported_settings_extension(tmp_path):
    path = tmp_path / "settings.yaml"
    path.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported settings format"):
        builder_mod._load_settings(str(path))


def test_load_input_supports_json_and_rejects_unsupported_extension(tmp_path):
    input_json = tmp_path / "graph.json"
    _write_json(input_json, {"nodes": ["A"], "links": []})

    loaded = builder_mod._load_input(str(input_json))
    assert loaded.nodes[0].name == "A"

    input_txt = tmp_path / "graph.txt"
    input_txt.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported input format"):
        builder_mod._load_input(str(input_txt))


def test_flatten_properties_blocks_handles_lists_recursively():
    config = {
        "items": [
            {"properties": {"a": {"b": 1}}},
            {"properties": {"x": {"y": "z"}}},
        ]
    }

    flattened = builder_mod._flatten_properties_blocks(config)

    assert flattened["items"][0]["properties"] == {"a.b": 1}
    assert flattened["items"][1]["properties"] == {"x.y": "z"}


def test_merge_properties_normalizes_short_and_long_keys():
    merged = builder_mod._merge_properties(
        Properties(**{"org.eclipse.elk.direction": "RIGHT"}),
        {"direction": "LEFT", "custom": "value"},
    )
    payload = merged.model_dump()

    assert payload["org.eclipse.elk.direction"] == "RIGHT"
    assert payload["custom"] == "value"


def test_build_canvas_rejects_unknown_layout_option_identifier():
    settings = sample_settings()
    settings.layout_options["not.a.valid.option"] = "x"

    with pytest.raises(ValueError, match="Unknown layout option identifiers"):
        builder_mod.build_canvas(MinimalGraphIn(nodes=["A"], links=[]), settings)


def test_estimate_label_dimensions_handles_invalid_and_non_positive_font_size():
    settings = sample_settings()
    settings.estimate_label_size_from_font = True

    invalid_size = builder_mod._estimate_label_dimensions(
        text="Label",
        width=10,
        height=5,
        properties=Properties(
            **{
                "org.eclipse.elk.font.name": "Arial",
                "org.eclipse.elk.font.size": "bad",
            }
        ),
        settings=settings,
    )
    non_positive_size = builder_mod._estimate_label_dimensions(
        text="Label",
        width=10,
        height=5,
        properties=Properties(
            **{
                "org.eclipse.elk.font.name": "Arial",
                "org.eclipse.elk.font.size": 0,
            }
        ),
        settings=settings,
    )

    assert invalid_size == (10, 5)
    assert non_positive_size == (10, 5)


def test_build_canvas_rejects_duplicate_sanitized_node_ids():
    minimal = MinimalGraphIn.model_validate(
        {
            "nodes": ["Node 1", "Node-1"],
            "links": [],
        }
    )

    with pytest.raises(ValueError, match="Duplicate node id"):
        builder_mod.build_canvas(minimal, sample_settings())


def test_build_canvas_rejects_unknown_nodes_when_auto_create_disabled():
    minimal = MinimalGraphIn.model_validate(
        {
            "nodes": ["A"],
            "links": [{"from": "A", "to": "B"}],
        }
    )
    settings = sample_settings()
    settings.auto_create_missing_nodes = False

    with pytest.raises(ValueError, match="Unknown node 'B' referenced by edge"):
        builder_mod.build_canvas(minimal, settings)


def test_build_canvas_falls_back_to_node_defaults_when_subgraph_defaults_missing():
    minimal = MinimalGraphIn.model_validate(
        {
            "nodes": [{"name": "Group", "nodes": ["A"]}],
            "links": [],
        }
    )
    settings = sample_settings()
    settings.estimate_label_size_from_font = False
    settings.subgraph_defaults = None

    canvas = builder_mod.build_canvas(minimal, settings)
    group = canvas.children[0]

    assert group.type == "subgraph"
    assert group.labels[0].width == settings.node_defaults.label.width
    assert group.labels[0].height == settings.node_defaults.label.height


def test_duplicate_edge_ids_are_suffixed():
    minimal = MinimalGraphIn.model_validate(
        {
            "nodes": ["A", "B", "C"],
            "links": [
                {"label": "dup", "from": "A", "to": "B"},
                {"label": "dup", "from": "A", "to": "C"},
            ],
        }
    )

    canvas = builder_mod.build_canvas(minimal, sample_settings())
    assert [edge.id for edge in canvas.edges] == ["dup", "dup_2"]


def test_main_prints_output_when_no_output_path(tmp_path, capsys):
    input_path = tmp_path / "input.json"
    _write_json(
        input_path,
        {
            "nodes": ["A", "B"],
            "links": ["A -> B"],
        },
    )

    exit_code = builder_mod.main([str(input_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"id": "canvas"' in captured.out
