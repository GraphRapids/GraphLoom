from typing import List
from pydantic import BaseModel

from .base import Properties

class PortLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties

class Port(BaseModel):
    id: str
    width: float
    height: float
    labels: List[PortLabel]
    properties: Properties
