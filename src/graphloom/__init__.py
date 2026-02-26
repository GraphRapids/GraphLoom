from __future__ import annotations

from typing import TYPE_CHECKING

from .canvas import Canvas
from .base import Properties
from .enums import (
    Direction,
    LayeringStrategy,
    NodeLabelPlacement,
    NodeSizeConstraint,
    NodeSizeOption,
    PortConstraints,
    PortLabelPlacement,
    PortSide,
    SizeConstraint,
    SizeOptions,
)
from .node import Node, NodeLabel
from .options import (
    EdgeLayoutOptions,
    LabelLayoutOptions,
    LayoutOptions,
    NodeLayoutOptions,
    ParentLayoutOptions,
    PortLayoutOptions,
)
from .port import Port, PortLabel
from .edge import Edge,EdgeLabel
from .profile import (
    ResolvedProfileElkSettings,
    build_canvas_from_profile_bundle,
    resolve_profile_elk_settings,
)
from .settings import ElkSettings, sample_settings

if TYPE_CHECKING:  # pragma: no cover
    from .builder import MinimalGraphIn, MinimalEdgeIn, MinimalNodeIn, build_canvas, sanitize_id
    from .elkjs import layout_with_elkjs

__all__ = [
    "Node",
    "Port",
    "Edge",
    "NodeLabel",
    "PortLabel",
    "EdgeLabel",
    "Canvas",
    "LayoutOptions",
    "ParentLayoutOptions",
    "NodeLayoutOptions",
    "EdgeLayoutOptions",
    "PortLayoutOptions",
    "LabelLayoutOptions",
    "Properties",
    "Direction",
    "LayeringStrategy",
    "NodeLabelPlacement",
    "NodeSizeConstraint",
    "NodeSizeOption",
    "PortConstraints",
    "PortLabelPlacement",
    "PortSide",
    "SizeConstraint",
    "SizeOptions",
    "MinimalGraphIn",
    "MinimalEdgeIn",
    "MinimalNodeIn",
    "build_canvas",
    "layout_with_elkjs",
    "sanitize_id",
    "ElkSettings",
    "sample_settings",
    "ResolvedProfileElkSettings",
    "resolve_profile_elk_settings",
    "build_canvas_from_profile_bundle",
]


def __getattr__(name: str):
    if name in {"MinimalGraphIn", "MinimalEdgeIn", "MinimalNodeIn", "build_canvas", "sanitize_id"}:
        from . import builder as _builder

        return getattr(_builder, name)
    if name == "layout_with_elkjs":
        from . import elkjs as _elkjs

        return _elkjs.layout_with_elkjs
    raise AttributeError(f"module 'graphloom' has no attribute '{name}'")
