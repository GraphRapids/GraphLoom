from enum import Enum
from typing import List, Union
from pydantic import BaseModel

from .base import Properties

class PortLabelPlacement(str, Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    NEXT_TO_PORT_IF_POSSIBLE = "NEXT_TO_PORT_IF_POSSIBLE"
    ALWAYS_SAME_SIDE = "ALWAYS_SAME_SIDE"
    ALWAYS_OTHER_SAME_SIDE = "ALWAYS_OTHER_SAME_SIDE"
    SPACE_EFFICIENT = "SPACE_EFFICIENT"

class PortSide(str, Enum):
    UNDEFINED = "UNDEFINED"
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

class PortConstraint(str, Enum):
    UNDEFINED = "UNDEFINED"
    FREE = "FREE"
    FIXED_SIDE = "FIXED_SIDE"
    FIXED_ORDER = "FIXED_ORDER"
    FIXED_RATIO = "FIXED_RATIO"
    FIXED_POS = "FIXED_POS"

PortPlacementInput = Union[str, List[PortLabelPlacement]]

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
