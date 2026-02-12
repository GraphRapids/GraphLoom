from typing import List
from pydantic import BaseModel

from .base import Properties
from .enums import EdgeLabelPlacement, EdgeType
from .options import EdgeLayoutOptions, LabelLayoutOptions
    
class EdgeLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties
    layoutOptions: LabelLayoutOptions | None = None

class Edge(BaseModel):
    id: str
    sources: List[str]
    targets: List[str]
    labels: List[EdgeLabel]
    properties: Properties
    layoutOptions: EdgeLayoutOptions | None = None
