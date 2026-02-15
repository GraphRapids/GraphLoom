from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from .base import Properties
from .edge import Edge
from .port import Port

class NodeLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties
    
class Node(BaseModel):
    id: str
    type: str
    icon: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None
    labels: List[NodeLabel]
    ports: List[Port] = Field(default_factory=list)
    children: List["Node"] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)
    properties: Properties

    @field_validator("ports")
    @classmethod
    def port_ids_unique(cls, v: List[Port]):
        ids = [p.id for p in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Port ids must be unique within a node")
        
        for i, p in enumerate(v):
            props = p.properties.model_dump()
            props["org.eclipse.elk.port.index"] = i
            props.pop("port.index", None)
            p.properties = Properties(**props)

        return v

    @field_validator("children")
    @classmethod
    def child_ids_unique(cls, v: List["Node"]):
        ids = [c.id for c in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Child node ids must be unique within a parent node")
        return v

    @field_validator("edges")
    @classmethod
    def edge_ids_unique(cls, v: List[Edge]):
        ids = [e.id for e in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Edge ids must be unique within a parent node")
        return v

    @model_validator(mode="after")
    def validate_dimensions_by_role(self):
        is_subgraph = bool(self.children or self.edges)
        if is_subgraph and (self.width is not None or self.height is not None):
            raise ValueError("Subgraph nodes must not define width or height")
        if not is_subgraph and (self.width is None or self.height is None):
            raise ValueError("Leaf nodes must define both width and height")
        return self


Node.model_rebuild()
