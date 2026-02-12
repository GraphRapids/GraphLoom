from typing import List, Optional
from pydantic import BaseModel, field_validator

from .base import Properties
from .enums import NodeLabelPlacement, NodeSizeConstraint, NodeSizeOption, PortLabelPlacement
from .options import LabelLayoutOptions, NodeLayoutOptions
from .port import Port

class NodeLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties
    layoutOptions: LabelLayoutOptions | None = None
    
class Node(BaseModel):
    id: str
    type: str
    icon: Optional[str] = None
    width: float
    height: float
    labels: List[NodeLabel]
    ports: List[Port]
    properties: Properties
    layoutOptions: NodeLayoutOptions | None = None

    @field_validator("ports")
    @classmethod
    def port_ids_unique(cls, v: List[Port]):
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Port ids must be unique within a node")
        
        for i, p in enumerate(v):
            p.properties = p.properties.model_copy(update={"port.index": i})

        return v
