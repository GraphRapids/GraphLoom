from __future__ import annotations

from typing import Any

from .enums import EdgeMarker, EdgeStyle

EDGE_MARKER_START_KEY = "graphrapids.edge.marker_start"
EDGE_MARKER_END_KEY = "graphrapids.edge.marker_end"
EDGE_STYLE_KEY = "graphrapids.edge.style"


def normalize_graphrapids_edge_properties(
    properties: dict[str, Any] | None,
    *,
    apply_defaults: bool,
) -> dict[str, Any]:
    normalized = dict(properties or {})

    if apply_defaults:
        normalized.setdefault(EDGE_MARKER_START_KEY, EdgeMarker.NONE.value)
        normalized.setdefault(EDGE_MARKER_END_KEY, EdgeMarker.NONE.value)
        normalized.setdefault(EDGE_STYLE_KEY, EdgeStyle.SOLID.value)

    _validate_and_normalize_enum_value(normalized, EDGE_MARKER_START_KEY, EdgeMarker)
    _validate_and_normalize_enum_value(normalized, EDGE_MARKER_END_KEY, EdgeMarker)
    _validate_and_normalize_enum_value(normalized, EDGE_STYLE_KEY, EdgeStyle)
    return normalized


def _validate_and_normalize_enum_value(
    properties: dict[str, Any],
    key: str,
    enum_cls: type[EdgeMarker] | type[EdgeStyle],
) -> None:
    if key not in properties:
        return
    value = properties[key]
    try:
        properties[key] = enum_cls(value).value
    except ValueError as exc:
        allowed = ", ".join(item.value for item in enum_cls)
        raise ValueError(f"Invalid value for '{key}': {value!r}. Expected one of: {allowed}.") from exc
