from __future__ import annotations

import pytest

from graphloom import MinimalGraphIn, sample_settings
from graphloom.profile import build_canvas_from_profile_bundle, resolve_profile_elk_settings


def _bundle_with_settings(elk_settings: dict) -> dict:
    return {
        "schemaVersion": "v1",
        "profileId": "runtime",
        "profileVersion": 2,
        "checksum": "abc123",
        "name": "runtime",
        "nodeTypes": ["router"],
        "linkTypes": ["directed"],
        "elkSettings": elk_settings,
        "renderCss": ".node.router {}",
        "updatedAt": "2026-01-01T00:00:00Z",
    }


def test_resolve_profile_elk_settings_validates_and_preserves_metadata() -> None:
    settings_payload = sample_settings().model_dump(by_alias=True, exclude_none=True, mode="json")
    bundle = _bundle_with_settings(settings_payload)

    resolved = resolve_profile_elk_settings(bundle)

    assert resolved.profile_id == "runtime"
    assert resolved.profile_version == 2
    assert resolved.checksum == "abc123"
    assert resolved.settings.layout_options["org.eclipse.elk.algorithm"] == "layered"


def test_resolve_profile_elk_settings_is_deterministic_for_key_order() -> None:
    settings_payload = sample_settings().model_dump(by_alias=True, exclude_none=True, mode="json")
    settings_payload_reordered = {
        "edge_defaults": settings_payload["edge_defaults"],
        "layout_options": settings_payload["layout_options"],
        "node_defaults": settings_payload["node_defaults"],
        "subgraph_defaults": settings_payload["subgraph_defaults"],
        "type_overrides": settings_payload["type_overrides"],
        "type_icon_map": settings_payload["type_icon_map"],
        "edge_type_overrides": settings_payload["edge_type_overrides"],
        "auto_create_missing_nodes": settings_payload["auto_create_missing_nodes"],
        "estimate_label_size_from_font": settings_payload["estimate_label_size_from_font"],
    }

    bundle_a = _bundle_with_settings(settings_payload)
    bundle_b = _bundle_with_settings(settings_payload_reordered)

    resolved_a = resolve_profile_elk_settings(bundle_a)
    resolved_b = resolve_profile_elk_settings(bundle_b)

    assert resolved_a.settings.model_dump(by_alias=True, exclude_none=True) == resolved_b.settings.model_dump(
        by_alias=True,
        exclude_none=True,
    )


def test_build_canvas_from_profile_bundle_integrates_with_layout_pipeline() -> None:
    bundle = _bundle_with_settings(sample_settings().model_dump(by_alias=True, exclude_none=True, mode="json"))
    graph = MinimalGraphIn.model_validate({"nodes": ["A"], "links": []})

    canvas, resolved = build_canvas_from_profile_bundle(graph, bundle)

    assert resolved.profile_id == "runtime"
    assert canvas.layoutOptions.org_eclipse_elk_algorithm == "layered"


def test_resolve_profile_elk_settings_rejects_invalid_payloads() -> None:
    with pytest.raises(ValueError, match="missing required field 'elkSettings'"):
        resolve_profile_elk_settings(
            {
                "profileId": "runtime",
                "profileVersion": 1,
                "checksum": "x",
            }
        )

    with pytest.raises(ValueError, match="field 'elkSettings' must be an object"):
        resolve_profile_elk_settings(
            {
                "profileId": "runtime",
                "profileVersion": 1,
                "checksum": "x",
                "elkSettings": [],
            }
        )
