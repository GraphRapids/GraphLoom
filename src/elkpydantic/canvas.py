from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field, field_serializer, field_validator

from .base import Properties
from .node import Node, NodeLabelPlacement, NodePlacementInput, NodeSizeConstraint, NodeSizeOption
from .port import PortLabelPlacement
from .edge import Edge

class Direction(str, Enum):
    UNDEFINED = "UNDEFINED"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    DOWN = "DOWN"
    UP = "UP"

class LayeringStrategy(str, Enum):
    NETWORK_SIMPLEX = "NETWORK_SIMPLEX"
    LONGEST_PATH = "LONGEST_PATH"
    LONGEST_PATH_SOURCE = "LONGEST_PATH_SOURCE"
    COFFMAN_GRAHAM = "COFFMAN_GRAHAM"
    INTERACTIVE = "INTERACTIVE"
    STRETCH_WIDTH = "STRETCH_WIDTH"
    MIN_WIDTH = "MIN_WIDTH"
    BF_MODEL_ORDER = "BF_MODEL_ORDER"
    DF_MODEL_ORDER = "DF_MODEL_ORDER"

class LayoutOptions(BaseModel):
    model_config = {"extra": "allow", "populate_by_name": True}

    # Must be emitted as a string "[H_CENTER,V_BOTTOM,OUTSIDE,H_PRIORITY]"" 
    org_eclipse_elk_nodeLabels_placement: List[NodeLabelPlacement] = Field(
        alias="org.eclipse.elk.nodeLabels.placement",
    )

    @field_serializer("org_eclipse_elk_nodeLabels_placement")
    def serialize_node_labels_placement(self, v: List[NodeLabelPlacement], _info):
        return "[" + ",".join(item.value for item in v) + "]"
    
    @field_validator("org_eclipse_elk_nodeLabels_placement", mode="before")
    @classmethod
    def parse_placement(cls, v: NodePlacementInput):
        if isinstance(v, list):
            return v

        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                s = s[1:-1].strip()

            if not s:
                return []

            parts = [p.strip() for p in s.split(",") if p.strip()]
            return [NodeLabelPlacement(p) for p in parts]

        return v

    org_eclipse_elk_portLabels_placement: List[PortLabelPlacement] = Field(
        alias="org.eclipse.elk.portLabels.placement",
    )

    @field_serializer("org_eclipse_elk_portLabels_placement")
    def serialize_port_labels_placement(self, v: List[PortLabelPlacement], _info):
        return "[" + ",".join(item.value for item in v) + "]"

    @field_validator("org_eclipse_elk_portLabels_placement", mode="before")
    @classmethod
    def parse_port_placement(cls, v: Union[str, List[PortLabelPlacement]]):

        if isinstance(v, list):
            return v

        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                s = s[1:-1].strip()

            if not s:
                return []

            parts = [p.strip() for p in s.split(",") if p.strip()]
            return [PortLabelPlacement(p) for p in parts]

        return v

    org_eclipse_elk_algorithm: str = Field(
        alias="org.eclipse.elk.algorithm"
    )
    org_eclipse_elk_nodeSize_constraints: NodeSizeConstraint = Field(
        alias="org.eclipse.elk.nodeSize.constraints"
    )
    org_eclipse_elk_nodeSize_options: NodeSizeOption = Field(
        alias="org.eclipse.elk.nodeSize.options"
    )
    org_eclipse_elk_layered_layering_strategy: str = Field(
        alias="org.eclipse.elk.layered.layering.strategy"
    )
    org_eclipse_elk_aspectRatio: str = Field(
        alias="org.eclipse.elk.aspectRatio"
    )
    org_eclipse_elk_zoomToFit: bool = Field(
        alias="org.eclipse.elk.zoomToFit"
    )
    org_eclipse_elk_direction: Direction = Field(
        alias="org.eclipse.elk.direction"
    )

    @field_validator("org_eclipse_elk_nodeSize_constraints", mode="before")
    @classmethod
    def parse_node_size_constraints(cls, v: Union[str, NodeSizeConstraint]):
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                s = s[1:-1].strip()
            if not s:
                return NodeSizeConstraint.MINIMUM_SIZE
            return NodeSizeConstraint(s)
        return v

    @field_validator("org_eclipse_elk_nodeSize_options", mode="before")
    @classmethod
    def parse_node_size_options(cls, v: Union[str, NodeSizeOption]):
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("[") and s.endswith("]"):
                s = s[1:-1].strip()
            if not s:
                return NodeSizeOption.DEFAULT_MINIMUM_SIZE
            return NodeSizeOption(s)
        return v

class Canvas(BaseModel):
    model_config = {"populate_by_name": True}

    id: str = "canvas"
    layoutOptions: LayoutOptions = Field(default_factory=LayoutOptions)
    children: List[Node]
    edges: List[Edge] = Field(default_factory=list)

    @field_validator("children")
    @classmethod
    def children_ids_unique(cls, v: List[Node]):
        ids = [c.id for c in v]
        if len(ids) != len(set(ids)):
            raise ValueError("children id values must be unique")
        return v

    @field_validator("edges")
    @classmethod
    def edge_ids_unique(cls, v: List[Edge]):
        ids = [e.id for e in v]
        if len(ids) != len(set(ids)):
            raise ValueError("edge id values must be unique")
        return v
