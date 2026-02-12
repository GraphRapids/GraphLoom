from typing import List
from pydantic import BaseModel

from .base import Properties
from .enums import PortConstraint, PortSide
from .options import LabelLayoutOptions, PortLayoutOptions

class PortLabel(BaseModel):
    text: str
    width: float
    height: float
    properties: Properties
    layoutOptions: LabelLayoutOptions | None = None

class Port(BaseModel):
    id: str
    width: float
    height: float
    labels: List[PortLabel]
    properties: Properties
    layoutOptions: PortLayoutOptions | None = None
