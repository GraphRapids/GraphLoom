from typing import List, Optional
from pydantic import BaseModel, field_validator

from .base import Properties
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
            raise ValueError("Port ids must be unique within a node")
        
        for i, p in enumerate(v):
            props = p.properties.model_dump()
            props["org.eclipse.elk.port.index"] = i
            props.pop("port.index", None)
            p.properties = Properties(**props)

        return v
