from __future__ import annotations

import json
import re
from collections import OrderedDict
from typing import Any, Dict, List, Tuple, Optional

try:  # Python 3.11+
    import tomllib  # type: ignore
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator

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
from .elkjs import layout_with_elkjs
from .node import Node, NodeLabel
from .port import Port, PortLabel
from .settings import ElkSettings, sample_settings

NODE_NAME_MIN_LENGTH = 1
NODE_NAME_MAX_LENGTH = 20
PORT_NAME_MIN_LENGTH = 1
PORT_NAME_MAX_LENGTH = 15
EDGE_NAME_MIN_LENGTH = 1
EDGE_NAME_MAX_LENGTH = 40


def _validate_length(value: str, *, field_name: str, min_len: int, max_len: int) -> str:
    length = len(value)
    if length < min_len or length > max_len:
        raise ValueError(f"{field_name} must be between {min_len} and {max_len} characters.")
    return value


class MinimalNodeIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(validation_alias=AliasChoices("name", "l"))
    type: str | None = Field(default=None, validation_alias=AliasChoices("type", "t"))
    id: str | None = None
    nodes: List["MinimalNodeIn | str"] = Field(default_factory=list)
    edges: List["MinimalEdgeIn | str"] = Field(
        default_factory=list,
        alias="links",
        validation_alias=AliasChoices("edges", "links"),
    )

    @field_validator("nodes", mode="before")
    @classmethod
    def normalize_nodes(cls, v: Any):
        if v is None:
            return []
        if not isinstance(v, list):
            return v
        normalized: List[Any] = []
        for node in v:
            if isinstance(node, str):
                normalized.append({"name": node})
            else:
                normalized.append(node)
        return normalized

    @field_validator("edges", mode="before")
    @classmethod
    def normalize_edges(cls, v: Any):
        if v is None:
            return []
        if not isinstance(v, list):
            return v
        return [_normalize_edge_entry(edge) for edge in v]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if ":" in value:
            raise ValueError(
                "Node name cannot contain ':' because edge endpoints use 'node:port' syntax."
            )
        return _validate_length(
            value,
            field_name="Node name",
            min_len=NODE_NAME_MIN_LENGTH,
            max_len=NODE_NAME_MAX_LENGTH,
        )


class MinimalEdgeIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str | None = None
    name: str | None = Field(default=None, validation_alias=AliasChoices("name"))
    label: str | None = Field(default=None, validation_alias=AliasChoices("label", "l"))
    type: str | None = Field(default=None, validation_alias=AliasChoices("type", "t"))
    source: str = Field(
        validation_alias=AliasChoices("from", "a"),
        serialization_alias="from",
    )
    target: str = Field(
        validation_alias=AliasChoices("to", "b"),
        serialization_alias="to",
    )

    @field_validator("name", "label")
    @classmethod
    def validate_edge_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _validate_length(
            value,
            field_name="Edge name",
            min_len=EDGE_NAME_MIN_LENGTH,
            max_len=EDGE_NAME_MAX_LENGTH,
        )

    @field_validator("source", "target")
    @classmethod
    def validate_endpoint(cls, value: str) -> str:
        node_part, port_part = split_endpoint(value)
        _validate_length(
            node_part,
            field_name="Node name",
            min_len=NODE_NAME_MIN_LENGTH,
            max_len=NODE_NAME_MAX_LENGTH,
        )
        if port_part is not None:
            if ":" in port_part:
                raise ValueError(
                    "Port name cannot contain ':' because edge endpoints use 'node:port' syntax."
                )
            _validate_length(
                port_part,
                field_name="Port name",
                min_len=PORT_NAME_MIN_LENGTH,
                max_len=PORT_NAME_MAX_LENGTH,
            )
        return value


class MinimalGraphIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    nodes: List[MinimalNodeIn | str]
    edges: List[MinimalEdgeIn | str] = Field(
        default_factory=list,
        alias="links",
        validation_alias=AliasChoices("edges", "links"),
    )

    @field_validator("nodes", mode="before")
    @classmethod
    def normalize_nodes(cls, v: Any):
        if v is None:
            return []
        if not isinstance(v, list):
            return v
        normalized: List[Any] = []
        for node in v:
            if isinstance(node, str):
                normalized.append({"name": node})
            else:
                normalized.append(node)
        return normalized

    @field_validator("edges", mode="before")
    @classmethod
    def normalize_edges(cls, v: Any):
        if v is None:
            return []
        if not isinstance(v, list):
            return v
        return [_normalize_edge_entry(edge) for edge in v]


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


def _parse_link_shorthand(link: str) -> Dict[str, str]:
    left, sep, right = link.partition("->")
    if not sep:
        raise ValueError(
            f"Invalid link shorthand '{link}'. Expected format: 'Source[:Port] -> Target[:Port]'"
        )
    source = left.strip()
    target = right.strip()
    if not source or not target:
        raise ValueError(
            f"Invalid link shorthand '{link}'. Both source and target must be present."
        )
    return {"from": source, "to": target}


def _normalize_edge_entry(edge: Any) -> Any:
    if isinstance(edge, str):
        return _parse_link_shorthand(edge)
    return edge


def _as_node(node: "MinimalNodeIn | str") -> "MinimalNodeIn":
    if isinstance(node, MinimalNodeIn):
        return node
    return MinimalNodeIn.model_validate({"name": node})


def _as_edge(edge: "MinimalEdgeIn | str") -> "MinimalEdgeIn":
    if isinstance(edge, MinimalEdgeIn):
        return edge
    return MinimalEdgeIn.model_validate(_normalize_edge_entry(edge))


class _NodeRecord(BaseModel):
    id: str
    label: str
    type: str
    aliases: List[str]
    input_node: MinimalNodeIn | None = None


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


def _canvas_layout_options(options: Dict[str, Any]) -> LayoutOptions:
    disallowed = sorted(key for key in options if key not in _ELK_OPTION_IDENTIFIERS)
    if disallowed:
        disallowed_list = ", ".join(disallowed)
        raise ValueError(f"Unknown layout option identifiers: {disallowed_list}")
    return LayoutOptions(**options)


def _merge_properties(base: Properties, extra: Dict[str, Any]) -> Properties:
    base_dict = _normalize_properties(base.model_dump())
    extra_dict = _normalize_properties(extra)
    if not base_dict and not extra_dict:
        return base
    merged = {**extra_dict, **base_dict}
    return Properties(**merged)


def build_canvas(data: MinimalGraphIn, settings: ElkSettings | None = None) -> Canvas:
    settings = settings or sample_settings()
    parent_layout = _canvas_layout_options(settings.layout_options)

    type_overrides_lc = {k.lower(): v for k, v in settings.type_overrides.items()}
    type_icon_map_lc = {k.lower(): v for k, v in settings.type_icon_map.items()}
    edge_type_overrides_lc = {k.lower(): v for k, v in settings.edge_type_overrides.items()}

    def build_scope(graph_data: MinimalGraphIn) -> tuple[List[Node], List[Edge]]:
        nodes: "OrderedDict[str, _NodeRecord]" = OrderedDict()
        alias_index: Dict[str, str] = {}
        ports: Dict[str, OrderedDict[str, Dict[str, str]]] = {}

        def register_node(
            label: str,
            node_type: str | None = None,
            node_id_override: str | None = None,
            input_node: MinimalNodeIn | None = None,
        ) -> _NodeRecord:
            node_id_source = node_id_override or label
            node_id = sanitize_id(node_id_source)
            if node_id in nodes:
                raise ValueError(f"Duplicate node id '{node_id}' derived from '{node_id_source}'")
            node_type_norm = (node_type or settings.node_defaults.type).lower()
            aliases = _candidate_aliases(label)
            if node_id_override:
                aliases.extend(_candidate_aliases(node_id_override))
            aliases = list(dict.fromkeys(aliases))
            record = _NodeRecord(
                id=node_id,
                label=label,
                type=node_type_norm,
                aliases=aliases,
                input_node=input_node,
            )
            nodes[node_id] = record
            for alias in record.aliases:
                alias_index.setdefault(alias, node_id)
            alias_index.setdefault(node_id, node_id)
            return record

        for node_raw in graph_data.nodes:
            node = _as_node(node_raw)
            register_node(
                label=node.name,
                node_type=node.type,
                node_id_override=node.id,
                input_node=node,
            )

        def ensure_node(node_token: str) -> _NodeRecord:
            token_norm = sanitize_id(node_token)
            if token_norm in alias_index:
                node_id = alias_index[token_norm]
                return nodes[node_id]
            if not settings.auto_create_missing_nodes:
                raise ValueError(f"Unknown node '{node_token}' referenced by edge")
            return register_node(label=node_token)

        for edge_raw in graph_data.edges:
            edge = _as_edge(edge_raw)
            for endpoint in (edge.source, edge.target):
                node_part, port_part = split_endpoint(endpoint)
                node_rec = ensure_node(node_part)
                if port_part is None:
                    continue
                port_key = sanitize_id(port_part)
                if node_rec.id not in ports:
                    ports[node_rec.id] = OrderedDict()
                if port_key not in ports[node_rec.id]:
                    ports[node_rec.id][port_key] = {
                        "label": port_part,
                        "id": f"{node_rec.id}_{port_key}",
                    }

        def build_node(node_rec: _NodeRecord) -> Node:
            child_nodes: List[Node] = []
            child_edges: List[Edge] = []
            if node_rec.input_node and (node_rec.input_node.nodes or node_rec.input_node.edges):
                child_nodes, child_edges = build_scope(
                    MinimalGraphIn(
                        nodes=node_rec.input_node.nodes,
                        edges=node_rec.input_node.edges,
                    )
                )

            is_subgraph = bool(child_nodes or child_edges)
            effective_type = "subgraph" if is_subgraph else node_rec.type
            role_defaults = settings.subgraph_defaults if is_subgraph else settings.node_defaults
            if role_defaults is None:
                role_defaults = settings.node_defaults
            defaults = type_overrides_lc.get(effective_type) or role_defaults
            icon = type_icon_map_lc.get(effective_type, defaults.icon)

            node_ports: List[Port] = []
            for port_data in ports.get(node_rec.id, OrderedDict()).values():
                port_defaults = defaults.port
                port_label = PortLabel(
                    text=port_data["label"],
                    width=port_defaults.label.width,
                    height=port_defaults.label.height,
                    properties=_merge_properties(
                        Properties(**port_defaults.label.properties),
                        {},
                    ),
                )
                node = Port(
                    id=port_data["id"],
                    width=port_defaults.width,
                    height=port_defaults.height,
                    labels=[port_label],
                    properties=_merge_properties(
                        Properties(**port_defaults.properties),
                        {},
                    ),
                )
                node_ports.append(node)

            node_label = NodeLabel(
                text=node_rec.label,
                width=defaults.label.width,
                height=defaults.label.height,
                properties=_merge_properties(
                    Properties(**defaults.label.properties),
                    {},
                ),
            )

            node_kwargs: Dict[str, Any] = {
                "id": node_rec.id,
                "type": effective_type,
                "icon": icon,
                "labels": [node_label],
                "ports": node_ports,
                "children": child_nodes,
                "edges": child_edges,
                "properties": _merge_properties(
                    Properties(**defaults.properties),
                    {},
                ),
            }
            if not is_subgraph:
                node_kwargs["width"] = defaults.width
                node_kwargs["height"] = defaults.height
            return Node(**node_kwargs)

        scope_children: List[Node] = [build_node(node) for node in nodes.values()]

        edge_ids: Dict[str, int] = {}
        scope_edges: List[Edge] = []
        for edge_raw in graph_data.edges:
            edge = _as_edge(edge_raw)
            sources: List[str] = []
            targets: List[str] = []
            for endpoint, bucket in ((edge.source, sources), (edge.target, targets)):
                node_part, port_part = split_endpoint(endpoint)
                node_rec = ensure_node(node_part)
                if port_part is None:
                    bucket.append(node_rec.id)
                    continue
                port_key = sanitize_id(port_part)
                port_id = ports[node_rec.id][port_key]["id"]
                bucket.append(port_id)

            edge_id_source = edge.id or edge.label or edge.name or _gen_id("edge")
            base_edge_id = sanitize_id(edge_id_source)
            if base_edge_id in edge_ids:
                edge_ids[base_edge_id] += 1
                edge_id = f"{base_edge_id}_{edge_ids[base_edge_id]}"
            else:
                edge_ids[base_edge_id] = 1
                edge_id = base_edge_id

            edge_type_norm = (edge.type or "").strip().lower()
            edge_defaults = edge_type_overrides_lc.get(edge_type_norm) or settings.edge_defaults
            edge_label_text = edge.label or edge.name or edge_defaults.label.text
            edge_runtime_props: Dict[str, Any] = {}
            if edge.type:
                edge_runtime_props["elkpydantic.edgeType"] = edge.type
            edge_label = EdgeLabel(
                text=edge_label_text,
                width=edge_defaults.label.width,
                height=edge_defaults.label.height,
                properties=_merge_properties(
                    Properties(**edge_defaults.label.properties),
                    {},
                ),
            )
            scope_edges.append(
                Edge(
                    id=edge_id,
                    sources=sources,
                    targets=targets,
                    labels=[edge_label],
                    properties=_merge_properties(
                        Properties(**edge_defaults.properties),
                        edge_runtime_props,
                    ),
                )
            )

        return scope_children, scope_edges

    canvas_children, canvas_edges = build_scope(data)

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


def _load_input(path: str) -> MinimalGraphIn:
    if path.endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return MinimalGraphIn.model_validate(data)

    if path.endswith(".yaml") or path.endswith(".yml"):
        try:
            import yaml  # type: ignore
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "PyYAML is required for YAML input. Install dependencies with 'pip install -e .'."
            ) from exc
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return MinimalGraphIn.model_validate(data)

    raise ValueError("Unsupported input format; use .json, .yaml, or .yml")


def main(argv: List[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Enrich minimal graph JSON/YAML into ELK JSON.")
    parser.add_argument("input", help="Path to minimal input JSON or YAML")
    parser.add_argument("-o", "--output", help="Where to write ELK JSON (default: stdout)")
    parser.add_argument("-s", "--settings", help="Path to settings TOML/JSON (optional)")
    parser.add_argument(
        "--layout",
        action="store_true",
        help="Run local elkjs layout and include computed positions/sizes in output.",
    )
    parser.add_argument(
        "--elkjs-mode",
        choices=["node", "npm", "npx"],
        default="node",
        help="elkjs mode for --layout: node (preinstalled), npm (auto-install cache), npx (alias of npm).",
    )
    parser.add_argument(
        "--node-cmd",
        default="node",
        help="Node.js executable used by --layout (default: node).",
    )
    args = parser.parse_args(argv)

    data = _load_input(args.input)
    settings = _load_settings(args.settings)
    canvas = build_canvas(data, settings)
    payload = canvas.model_dump(by_alias=True, exclude_none=True)
    if args.layout:
        payload = layout_with_elkjs(payload, mode=args.elkjs_mode, node_cmd=args.node_cmd)
    output = json.dumps(payload, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
