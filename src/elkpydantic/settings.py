from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LabelDefaults(BaseModel):
    text: str
    width: float
    height: float
    properties: Dict[str, Any] = Field(default_factory=dict)


class PortDefaults(BaseModel):
    width: float
    height: float
    label: LabelDefaults
    properties: Dict[str, Any] = Field(default_factory=dict)


class NodeDefaults(BaseModel):
    type: str
    icon: str
    width: float
    height: float
    label: LabelDefaults
    port: PortDefaults
    properties: Dict[str, Any] = Field(default_factory=dict)


class EdgeDefaults(BaseModel):
    label: LabelDefaults
    properties: Dict[str, Any] = Field(default_factory=dict)


class ElkSettings(BaseSettings):
    """Centralised defaults for building ELK JSON."""

    model_config = SettingsConfigDict(
        env_prefix="ELK_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    layout_options: Dict[str, Any]
    node_defaults: NodeDefaults
    type_overrides: Dict[str, NodeDefaults] = Field(default_factory=dict)
    edge_defaults: EdgeDefaults
    auto_create_missing_nodes: bool = True


# Handy in-code default configuration mirroring sample_output_01.json.
# Keeping it as a function prevents instantiation at import time.
def sample_settings() -> ElkSettings:
    return ElkSettings.model_validate(
        {
            "layout_options": {
                "org.eclipse.elk.nodeLabels.placement": "[H_CENTER,V_BOTTOM,OUTSIDE,H_PRIORITY]",
                "org.eclipse.elk.portLabels.placement": "[OUTSIDE]",
                "org.eclipse.elk.algorithm": "layered",
                "org.eclipse.elk.nodeSize.constraints": "MINIMUM_SIZE",
                "org.eclipse.elk.nodeSize.options": "DEFAULT_MINIMUM_SIZE",
                "org.eclipse.elk.layered.layering.strategy": "NETWORK_SIMPLEX",
                "org.eclipse.elk.aspectRatio": "1.414",
                "org.eclipse.elk.zoomToFit": True,
                "org.eclipse.elk.direction": "RIGHT",
            },
            "node_defaults": {
                "type": "router",
                "icon": "mdi:router",
                "width": 50,
                "height": 50,
                "label": {
                    "text": "Node",
                    "width": 150,
                    "height": 16,
                    "properties": {"font.size": 16},
                },
                "port": {
                    "width": 2.0,
                    "height": 2.0,
                    "label": {
                        "text": "Port",
                        "width": 100,
                        "height": 8,
                        "properties": {"font.size": 8},
                    },
                    "properties": {"port.index": 0},
                },
                "properties": {
                    "portConstraints": "[FIXED_ORDER]",
                    "portLabels.placement": "[OUTSIDE, NEXT_TO_PORT_IF_POSSIBLE]",
                    "nodeLabels.placement": "[OUTSIDE, V_BOTTOM, H_CENTER, H_PRIORITY]",
                },
            },
            "edge_defaults": {
                "label": {
                    "text": "Edge",
                    "width": 100,
                    "height": 10,
                    "properties": {"font.size": 10, "edgeLabels.inline": False},
                },
                "properties": {"edge.type": "UNDIRECTED", "edge.thickness": 1},
            },
        }
    )
