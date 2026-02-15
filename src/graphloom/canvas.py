from typing import List
from pydantic import BaseModel, Field, field_validator

from .edge import Edge
from .enums import Direction, EdgeRouting, EdgeRoutingMode, LayeringStrategy
from .node import Node
from .options import LayoutOptions

class Canvas(BaseModel):
    model_config = {"populate_by_name": True}

    id: str = "canvas"
    layoutOptions: LayoutOptions
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
