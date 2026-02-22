from __future__ import annotations

import graphloom.builder as builder_mod
from graphloom.settings import sample_settings
from graphloom.theme import apply_theme_metrics


def test_apply_theme_metrics_updates_font_and_edge_defaults() -> None:
    settings = sample_settings()
    themed = apply_theme_metrics(
        settings,
        {
            "font_family": "Inter, Arial, sans-serif",
            "font_size_px": 13,
            "label_line_height_px": 16,
            "edge_thickness_px": 2.25,
            "node_label_horizontal_padding_px": 4,
            "node_label_vertical_padding_px": 3,
        },
    )

    assert themed.node_defaults.label.properties["org.eclipse.elk.font.name"] == "Inter, Arial, sans-serif"
    assert themed.node_defaults.label.properties["org.eclipse.elk.font.size"] == 13.0
    assert themed.edge_defaults.properties["org.eclipse.elk.edge.thickness"] == 2.25
    assert themed.estimate_label_size_from_font is True
    assert themed.node_defaults.label.height >= 22


def test_main_applies_theme_id_before_build(monkeypatch, tmp_path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text('{"nodes":["A"],"links":[]}', encoding="utf-8")

    captured: dict[str, object] = {}

    def fake_resolve(settings, theme_id):
        captured["theme_id"] = theme_id
        return settings

    monkeypatch.setattr(builder_mod, "resolve_theme_settings", fake_resolve)

    exit_code = builder_mod.main([str(input_path), "--theme-id", "default"])

    assert exit_code == 0
    assert captured["theme_id"] == "default"
