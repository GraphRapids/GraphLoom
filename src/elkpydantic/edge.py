from typing import List, Optional
from pydantic import BaseModel

from .base import Properties
    
class EdgeLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties

class Edge(BaseModel):
    id: str
    type: Optional[str] = None
    sources: List[str]
    targets: List[str]
    labels: List[EdgeLabel]
    properties: Properties
