from enum import Enum
from typing import List, Union
from pydantic import BaseModel, field_validator

from .base import Properties
from .port import Port

class NodeLabelPlacement(str, Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    H_LEFT = "H_LEFT"
    H_CENTER = "H_CENTER"
    H_RIGHT = "H_RIGHT"
    V_TOP = "V_TOP"
    V_CENTER = "V_CENTER"
    V_BOTTOM = "V_BOTTOM"
    H_PRIORITY = "H_PRIORITY"

class NodeSizeConstraint(str, Enum):
    PORTS = "PORTS"
    PORT_LABELS = "PORT_LABELS"
    NODE_LABELS = "NODE_LABELS"
    MINIMUM_SIZE = "MINIMUM_SIZE"

class NodeSizeOption(str, Enum):
    DEFAULT_MINIMUM_SIZE = "DEFAULT_MINIMUM_SIZE"
    MINIMUM_SIZE_ACCOUNTS_FOR_PADDING = "MINIMUM_SIZE_ACCOUNTS_FOR_PADDING"
    COMPUTE_PADDING = "COMPUTE_PADDING"
    OUTSIDE_NODE_LABELS_OVERHANG = "OUTSIDE_NODE_LABELS_OVERHANG"
    PORTS_OVERHANG = "PORTS_OVERHANG"
    UNIFORM_PORT_SPACING = "UNIFORM_PORT_SPACING"
    FORCE_TABULAR_NODE_LABELS = "FORCE_TABULAR_NODE_LABELS"
    ASYMMETRICAL = "ASYMMETRICAL"

NodePlacementInput = Union[str, List[NodeLabelPlacement]]

class NodeLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties
    
class Node(BaseModel):
    id: str
    type: str
    icon: str
    width: float
    height: float
    labels: List[NodeLabel]
    ports: List[Port]
    properties: Properties

    @field_validator("ports")
    @classmethod
    def port_ids_unique(cls, v: List[Port]):
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("port ids must be unique within a node")
        
        for i, p in enumerate(v):
            p.properties = p.properties.model_copy(update={"port.index": i})

        return v
