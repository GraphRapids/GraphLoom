from __future__ import annotations

from typing import Any, Mapping

from .settings import ElkSettings

_FONT_NAME_KEY = "org.eclipse.elk.font.name"
_FONT_SIZE_KEY = "org.eclipse.elk.font.size"
_EDGE_THICKNESS_KEY = "org.eclipse.elk.edge.thickness"


def apply_theme_metrics(settings: ElkSettings, metrics: Mapping[str, Any]) -> ElkSettings:
    """Apply GraphTheme metrics to ELK settings used by GraphLoom."""
    themed = settings.model_copy(deep=True)

    font_family = metrics.get("font_family")
    font_size = metrics.get("font_size_px")
    line_height = metrics.get("label_line_height_px")
    edge_thickness = metrics.get("edge_thickness_px")
    hpad = metrics.get("node_label_horizontal_padding_px", 0)
    vpad = metrics.get("node_label_vertical_padding_px", 0)

    if font_family is not None:
        _set_font_family(themed, str(font_family))

    if font_size is not None:
        try:
            parsed_font_size = float(font_size)
        except (TypeError, ValueError):
            parsed_font_size = None
        if parsed_font_size is not None and parsed_font_size > 0:
            _set_font_size(themed, parsed_font_size)
            themed.estimate_label_size_from_font = True

    if line_height is not None:
        try:
            parsed_line_height = float(line_height)
        except (TypeError, ValueError):
            parsed_line_height = None
        if parsed_line_height is not None and parsed_line_height > 0:
            _set_label_heights(themed, parsed_line_height, hpad=hpad, vpad=vpad)

    if edge_thickness is not None:
        try:
            parsed_edge_thickness = float(edge_thickness)
        except (TypeError, ValueError):
            parsed_edge_thickness = None
        if parsed_edge_thickness is not None and parsed_edge_thickness > 0:
            themed.edge_defaults.properties[_EDGE_THICKNESS_KEY] = parsed_edge_thickness

    return themed


def resolve_theme_settings(settings: ElkSettings, theme_id: str | None) -> ElkSettings:
    """Return settings with theme metrics applied when a theme id is provided."""
    if not theme_id:
        return settings
    try:
        from graphtheme import get_theme_metrics
    except Exception as exc:
        raise RuntimeError(
            "GraphTheme integration requires the 'GraphTheme' package to be installed."
        ) from exc
    metrics = get_theme_metrics(theme_id)
    return apply_theme_metrics(settings, metrics)


def _set_font_family(settings: ElkSettings, font_family: str) -> None:
    settings.node_defaults.label.properties[_FONT_NAME_KEY] = font_family
    settings.node_defaults.port.label.properties[_FONT_NAME_KEY] = font_family
    settings.edge_defaults.label.properties[_FONT_NAME_KEY] = font_family
    if settings.subgraph_defaults is not None:
        settings.subgraph_defaults.label.properties[_FONT_NAME_KEY] = font_family
        settings.subgraph_defaults.port.label.properties[_FONT_NAME_KEY] = font_family


def _set_font_size(settings: ElkSettings, font_size: float) -> None:
    settings.node_defaults.label.properties[_FONT_SIZE_KEY] = font_size
    settings.node_defaults.port.label.properties[_FONT_SIZE_KEY] = font_size
    settings.edge_defaults.label.properties[_FONT_SIZE_KEY] = font_size
    if settings.subgraph_defaults is not None:
        settings.subgraph_defaults.label.properties[_FONT_SIZE_KEY] = font_size
        settings.subgraph_defaults.port.label.properties[_FONT_SIZE_KEY] = font_size


def _set_label_heights(
    settings: ElkSettings,
    line_height: float,
    *,
    hpad: Any,
    vpad: Any,
) -> None:
    try:
        vertical_padding = float(vpad)
    except (TypeError, ValueError):
        vertical_padding = 0.0
    try:
        horizontal_padding = float(hpad)
    except (TypeError, ValueError):
        horizontal_padding = 0.0

    target_height = max(1.0, line_height + (2.0 * vertical_padding))
    min_width = max(1.0, line_height + (2.0 * horizontal_padding))

    for label in (
        settings.node_defaults.label,
        settings.node_defaults.port.label,
        settings.edge_defaults.label,
    ):
        label.height = max(float(label.height), target_height)
        if horizontal_padding > 0:
            label.width = max(float(label.width), min_width)

    if settings.subgraph_defaults is not None:
        settings.subgraph_defaults.label.height = max(
            float(settings.subgraph_defaults.label.height),
            target_height,
        )
        settings.subgraph_defaults.port.label.height = max(
            float(settings.subgraph_defaults.port.label.height),
            target_height,
        )
        if horizontal_padding > 0:
            settings.subgraph_defaults.label.width = max(
                float(settings.subgraph_defaults.label.width),
                min_width,
            )
            settings.subgraph_defaults.port.label.width = max(
                float(settings.subgraph_defaults.port.label.width),
                min_width,
            )
