from __future__ import annotations

import json
import re
from collections import OrderedDict
from typing import Any, Dict, List, Tuple, Optional

try:  # Python 3.11+
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pydantic import BaseModel, Field

from .canvas import Canvas
from .options import (
    EdgeLayoutOptions,
    LabelLayoutOptions,
    LayoutOptions,
    NodeLayoutOptions,
    ParentLayoutOptions,
    PortLayoutOptions,
)
from .base import Properties, _gen_id
from .edge import Edge, EdgeLabel
from .node import Node, NodeLabel
from .port import Port, PortLabel
from .settings import ElkSettings, sample_settings


class MinimalNodeIn(BaseModel):
    l: str
    t: str | None = None
    id: str | None = None
    nodes: List["MinimalNodeIn"] = Field(default_factory=list)


class MinimalEdgeIn(BaseModel):
    l: str
    t: str | None = None
    a: str
    b: str


class MinimalGraphIn(BaseModel):
    nodes: List[MinimalNodeIn]
    edges: List[MinimalEdgeIn]


MinimalNodeIn.model_rebuild()


def sanitize_id(value: str) -> str:
    """Lowercase, replace non-alnum with underscores, collapse duplicates."""
    s = value.strip().lower()
    s = re.sub(r"[\s:/@-]+", "_", s)
    s = re.sub(r"[^a-z0-9_]", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "id"


def _candidate_aliases(label: str) -> List[str]:
    base = sanitize_id(label)
    tokens = [t for t in re.split(r"[\s_]+", base) if t]
    stop = {"router", "switch", "node", "host", "device"}
    filtered = [t for t in tokens if t not in stop]
    aliases = {base}
    if filtered:
        aliases.add("_".join(filtered))
    return list(aliases)


def split_endpoint(endpoint: str) -> Tuple[str, Optional[str]]:
    if ":" in endpoint:
        node_part, port_part = endpoint.split(":", 1)  # split once
        return node_part.strip(), port_part.strip()
    return endpoint.strip(), None


class _NodeRecord(BaseModel):
    id: str
    label: str
    type: str
    aliases: List[str]
    parent_id: str | None = None
    child_ids: List[str] = Field(default_factory=list)


def _layout_aliases(model_cls: type[BaseModel]) -> set[str]:
    return {f.alias or name for name, f in model_cls.model_fields.items()}


def _elk_option_identifiers() -> set[str]:
    return {
        *_layout_aliases(ParentLayoutOptions),
        *_layout_aliases(NodeLayoutOptions),
        *_layout_aliases(EdgeLayoutOptions),
        *_layout_aliases(PortLayoutOptions),
        *_layout_aliases(LabelLayoutOptions),
    }


_ELK_OPTION_IDENTIFIERS = _elk_option_identifiers()


def _normalize_properties(data: Dict[str, Any]) -> Dict[str, Any]:
    if not data:
        return {}
    normalized: Dict[str, Any] = {}

    # Preserve long-form keys first
    for key, value in data.items():
        if key.startswith("org.eclipse.elk."):
            normalized[key] = value

    # Map short-form keys to long-form when possible
    for key, value in data.items():
        if key.startswith("org.eclipse.elk."):
            continue
        long_key = f"org.eclipse.elk.{key}"
        if long_key in _ELK_OPTION_IDENTIFIERS:
            normalized.setdefault(long_key, value)
        else:
            normalized[key] = value

    return normalized


def _options_to_properties(model_cls: type[BaseModel], data: Dict[str, Any]) -> Dict[str, Any]:
    if not data:
        return {}
    model = model_cls(**data)
    return model.model_dump(by_alias=True, exclude_none=True)


def _split_layout_options(
    options: Dict[str, Any],
) -> tuple[
    LayoutOptions,
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
]:
    parent_aliases = _layout_aliases(ParentLayoutOptions)
    node_aliases = _layout_aliases(NodeLayoutOptions)
    edge_aliases = _layout_aliases(EdgeLayoutOptions)
    port_aliases = _layout_aliases(PortLayoutOptions)
    label_aliases = _layout_aliases(LabelLayoutOptions)

    parent_opts: Dict[str, Any] = {}
    node_opts: Dict[str, Any] = {}
    edge_opts: Dict[str, Any] = {}
    port_opts: Dict[str, Any] = {}
    label_common_opts: Dict[str, Any] = {}
    label_node_opts: Dict[str, Any] = {}
    label_edge_opts: Dict[str, Any] = {}
    unknown: List[str] = []

    for key, value in options.items():
        matched = False
        if key in parent_aliases:
            parent_opts[key] = value
            matched = True
        if key in node_aliases:
            node_opts[key] = value
            matched = True
        if key in edge_aliases:
            edge_opts[key] = value
            matched = True
        if key in port_aliases:
            port_opts[key] = value
            matched = True
        if key in label_aliases:
            if key.startswith("org.eclipse.elk.nodeLabels."):
                label_node_opts[key] = value
            elif key.startswith("org.eclipse.elk.edgeLabels."):
                label_edge_opts[key] = value
            else:
                label_common_opts[key] = value
            matched = True
        if not matched:
            unknown.append(key)

    if unknown:
        unknown_sorted = ", ".join(sorted(unknown))
        raise ValueError(f"Unknown layout option identifiers: {unknown_sorted}")

    parent_layout = LayoutOptions(**parent_opts)
    node_props = _options_to_properties(NodeLayoutOptions, node_opts)
    edge_props = _options_to_properties(EdgeLayoutOptions, edge_opts)
    port_props = _options_to_properties(PortLayoutOptions, port_opts)
    label_common_props = _options_to_properties(LabelLayoutOptions, label_common_opts)
    node_label_props = {
        **label_common_props,
        **_options_to_properties(LabelLayoutOptions, label_node_opts),
    }
    edge_label_props = {
        **label_common_props,
        **_options_to_properties(LabelLayoutOptions, label_edge_opts),
    }
    port_label_props = dict(label_common_props)
    return (
        parent_layout,
        node_props,
        edge_props,
        port_props,
        node_label_props,
        edge_label_props,
        port_label_props,
    )


def _merge_properties(base: Properties, extra: Dict[str, Any]) -> Properties:
    base_dict = _normalize_properties(base.model_dump())
    extra_dict = _normalize_properties(extra)
    if not base_dict and not extra_dict:
        return base
    merged = {**extra_dict, **base_dict}
    return Properties(**merged)


def build_canvas(data: MinimalGraphIn, settings: ElkSettings | None = None) -> Canvas:
    settings = settings or sample_settings()

    # 1) Prepare node records and alias index
    nodes: "OrderedDict[str, _NodeRecord]" = OrderedDict()
    root_node_ids: List[str] = []
    alias_index: Dict[str, str] = {}
    type_overrides_lc = {k.lower(): v for k, v in settings.type_overrides.items()}
    type_icon_map_lc = {k.lower(): v for k, v in settings.type_icon_map.items()}

    def register_node(
        label: str,
        node_type: str | None = None,
        parent_id: str | None = None,
    ) -> _NodeRecord:
        node_id = sanitize_id(label)
        if node_id in nodes:
            raise ValueError(f"Duplicate node id '{node_id}' derived from '{label}'")
        node_type_norm = (node_type or settings.node_defaults.type).lower()
        record = _NodeRecord(
            id=node_id,
            label=label,
            type=node_type_norm,
            aliases=_candidate_aliases(label),
            parent_id=parent_id,
        )
        nodes[node_id] = record
        if parent_id is None:
            root_node_ids.append(node_id)
        else:
            nodes[parent_id].child_ids.append(node_id)
        for a in record.aliases:
            alias_index.setdefault(a, record.id)
        alias_index.setdefault(node_id, node_id)
        return record

    def register_input_node(n: MinimalNodeIn, parent_id: str | None = None):
        node_id_source = n.id or n.l
        node_type = n.t or settings.node_defaults.type
        record = register_node(node_id_source, node_type, parent_id=parent_id)
        for child in n.nodes:
            register_input_node(child, record.id)

    for n in data.nodes:
        register_input_node(n)

    # 2) Collect ports from edges, auto-creating nodes as needed
    ports: Dict[str, OrderedDict[str, Dict[str, str]]] = {}

    def ensure_node(node_token: str) -> _NodeRecord:
        token_norm = sanitize_id(node_token)
        if token_norm in alias_index:
            node_id = alias_index[token_norm]
            return nodes[node_id]
        if not settings.auto_create_missing_nodes:
            raise ValueError(f"Unknown node '{node_token}' referenced by edge")
        return register_node(node_token)

    for e in data.edges:
        for endpoint in (e.a, e.b):
            node_part, port_part = split_endpoint(endpoint)
            node_rec = ensure_node(node_part)
            if port_part is None:
                continue  # node-to-node edge; no port to create
            port_key = sanitize_id(port_part)
            if node_rec.id not in ports:
                ports[node_rec.id] = OrderedDict()
            if port_key not in ports[node_rec.id]:
                ports[node_rec.id][port_key] = {
                    "label": port_part,
                    "id": f"{node_rec.id}_{port_key}",
                }

    # 3) Build concrete nodes
    (
        parent_layout,
        node_props,
        edge_props,
        port_props,
        node_label_props,
        edge_label_props,
        port_label_props,
    ) = _split_layout_options(settings.layout_options)

    def build_node(node_rec: _NodeRecord) -> Node:
        defaults = type_overrides_lc.get(node_rec.type) or settings.node_defaults
        icon = type_icon_map_lc.get(node_rec.type, defaults.icon)
        node_ports: List[Port] = []
        for port_data in ports.get(node_rec.id, OrderedDict()).values():
            port_defaults = defaults.port
            port_label = PortLabel(
                text=port_data["label"],
                width=port_defaults.label.width,
                height=port_defaults.label.height,
                properties=_merge_properties(
                    Properties(**port_defaults.label.properties),
                    port_label_props,
                ),
            )
            port = Port(
                id=port_data["id"],
                width=port_defaults.width,
                height=port_defaults.height,
                labels=[port_label],
                properties=_merge_properties(
                    Properties(**port_defaults.properties),
                    port_props,
                ),
            )
            node_ports.append(port)

        node_label = NodeLabel(
            text=node_rec.label,
            width=defaults.label.width,
            height=defaults.label.height,
            properties=_merge_properties(
                Properties(**defaults.label.properties),
                node_label_props,
            ),
        )
        child_nodes = [build_node(nodes[child_id]) for child_id in node_rec.child_ids]
        node_kwargs: Dict[str, Any] = {
            "id": node_rec.id,
            "type": node_rec.type,
            "icon": icon,
            "labels": [node_label],
            "ports": node_ports,
            "children": child_nodes,
            "properties": _merge_properties(
                Properties(**defaults.properties),
                node_props,
            ),
        }
        if not child_nodes:
            node_kwargs["width"] = defaults.width
            node_kwargs["height"] = defaults.height
        return Node(**node_kwargs)

    canvas_children: List[Node] = []
    for node_id in root_node_ids:
        canvas_children.append(
            build_node(nodes[node_id])
        )

    # 4) Build edges
    edge_ids: Dict[str, int] = {}
    canvas_edges: List[Edge] = []
    for e in data.edges:
        sources: List[str] = []
        targets: List[str] = []
        for endpoint, bucket in ((e.a, sources), (e.b, targets)):
            node_part, port_part = split_endpoint(endpoint)
            node_rec = ensure_node(node_part)
            if port_part is None:
                bucket.append(node_rec.id)
                continue
            port_key = sanitize_id(port_part)
            port_id = ports[node_rec.id][port_key]["id"]
            bucket.append(port_id)

        base_edge_id = sanitize_id(e.l or _gen_id("edge"))
        if base_edge_id in edge_ids:
            edge_ids[base_edge_id] += 1
            edge_id = f"{base_edge_id}_{edge_ids[base_edge_id]}"
        else:
            edge_ids[base_edge_id] = 1
            edge_id = base_edge_id

        edge_defaults = settings.edge_defaults
        edge_label = EdgeLabel(
            text=e.l,
            width=edge_defaults.label.width,
            height=edge_defaults.label.height,
            properties=_merge_properties(
                Properties(**edge_defaults.label.properties),
                edge_label_props,
            ),
        )
        canvas_edges.append(
            Edge(
                id=edge_id,
                sources=sources,
                targets=targets,
                labels=[edge_label],
                properties=_merge_properties(
                    Properties(**edge_defaults.properties),
                    edge_props,
                ),
            )
        )

    return Canvas(
        id="canvas",
        layoutOptions=parent_layout,
        children=canvas_children,
        edges=canvas_edges,
    )

def _load_settings(path: str | None) -> ElkSettings:
    if not path:
        return sample_settings()
    if path.endswith(".toml"):
        with open(path, "rb") as f:
            data = tomllib.load(f)
    elif path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        raise ValueError("Unsupported settings format; use .toml or .json")
    if "layout_options" in data and isinstance(data["layout_options"], dict):
        data["layout_options"] = _flatten_layout(data["layout_options"])
    data = _flatten_properties_blocks(data)
    return ElkSettings.model_validate(data)


def _flatten_layout(layout: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """Flatten nested layout dicts into dotted keys expected by LayoutOptions."""
    flat: Dict[str, Any] = {}
    for key, value in layout.items():
        new_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(_flatten_layout(value, new_key))
        else:
            flat[new_key] = value
    return flat


def _flatten_properties_blocks(config: Any) -> Any:
    """Flatten any dict stored under a 'properties' key using dotted keys."""
    if isinstance(config, dict):
        flattened: Dict[str, Any] = {}
        for key, value in config.items():
            if key == "properties" and isinstance(value, dict):
                flattened[key] = _flatten_layout(value)
            else:
                flattened[key] = _flatten_properties_blocks(value)
        return flattened
    if isinstance(config, list):
        return [_flatten_properties_blocks(item) for item in config]
    return config


def main(argv: List[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Enrich minimal graph JSON into ELK JSON.")
    parser.add_argument("input", help="Path to minimal input JSON")
    parser.add_argument("-o", "--output", help="Where to write ELK JSON (default: stdout)")
    parser.add_argument("-s", "--settings", help="Path to settings TOML/JSON (optional)")
    args = parser.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as f:
        data = MinimalGraphIn.model_validate_json(f.read())

    settings = _load_settings(args.settings)
    canvas = build_canvas(data, settings)
    payload = canvas.model_dump(by_alias=True, exclude_none=True)
    output = json.dumps(payload, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
