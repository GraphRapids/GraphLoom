from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator
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
    icon: str | None = None
    width: float
    height: float
    label: LabelDefaults
    port: PortDefaults
    properties: Dict[str, Any] = Field(default_factory=dict)


class SubgraphDefaults(BaseModel):
    type: str
    icon: str | None = None
    width: float | None = None
    height: float | None = None
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
    subgraph_defaults: Optional[SubgraphDefaults] = None
    type_overrides: Dict[str, NodeDefaults] = Field(default_factory=dict)
    type_icon_map: Dict[str, str] = Field(default_factory=dict)
    edge_defaults: EdgeDefaults
    edge_type_overrides: Dict[str, EdgeDefaults] = Field(default_factory=dict)
    auto_create_missing_nodes: bool = True
    estimate_label_size_from_font: bool = False

    @model_validator(mode="after")
    def ensure_subgraph_defaults(self) -> "ElkSettings":
        if self.subgraph_defaults is None:
            copied = self.node_defaults.model_dump()
            copied["type"] = "subgraph"
            copied["width"] = None
            copied["height"] = None
            self.subgraph_defaults = SubgraphDefaults.model_validate(copied)
        return self


# Handy in-code default configuration mirroring sample_output_01.json.
# Keeping it as a function prevents instantiation at import time.
def sample_settings() -> ElkSettings:
    return ElkSettings.model_validate(
        {
            "auto_create_missing_nodes": True,
            "estimate_label_size_from_font": True,
            "layout_options": {
                "org.eclipse.elk.algorithm": "layered",
                "org.eclipse.elk.layered.layering.strategy": "NETWORK_SIMPLEX",
                "org.eclipse.elk.layered.nodePlacement.strategy": "NETWORK_SIMPLEX",
                "org.eclipse.elk.portConstraints": "FREE",
                "org.eclipse.elk.nodeSize.constraints": "MINIMUM_SIZE",
                "org.eclipse.elk.nodeSize.options": "[DEFAULT_MINIMUM_SIZE,COMPUTE_PADDING,MINIMUM_SIZE_ACCOUNTS_FOR_PADDING]",
                "org.eclipse.elk.hierarchyHandling": "INCLUDE_CHILDREN",
                "org.eclipse.elk.aspectRatio": "1.414",
                "org.eclipse.elk.zoomToFit": True,
                "org.eclipse.elk.direction": "RIGHT",
                "org.eclipse.elk.padding": "[top=60,left=60,bottom=60,right=60]",
                "org.eclipse.elk.spacing.labelPortHorizontal": 1,
                "org.eclipse.elk.spacing.labelPortVertical": -3.5,
            },
            "node_defaults": {
                "type": "default",
                "width": 60,
                "height": 60,
                "label": {
                    "text": "Node",
                    "width": 150,
                    "height": 16,
                    "properties": {"org.eclipse.elk.font.name": "Arial", "org.eclipse.elk.font.size": 16},
                },
                "port": {
                    "width": 1.0,
                    "height": 1.0,
                    "label": {
                        "text": "Port",
                        "width": 0,
                        "height": 2,
                        "properties": {"org.eclipse.elk.font.name": "Arial", "org.eclipse.elk.font.size": 4},
                    },
                    "properties": {},
                },
                "properties": {
                    "org.eclipse.elk.portConstraints": "FREE",
                    "org.eclipse.elk.portLabels.treatAsGroup": True,
                    "org.eclipse.elk.portLabels.placement": "[OUTSIDE,NEXT_TO_PORT_IF_POSSIBLE]",
                    "org.eclipse.elk.nodeLabels.placement": "[OUTSIDE, V_BOTTOM, H_CENTER, H_PRIORITY]",
                },
            },
            "subgraph_defaults": {
                "type": "subgraph",
                "label": {
                    "text": "Subgraph",
                    "width": 300,
                    "height": 20,
                    "properties": {"org.eclipse.elk.font.name": "Arial", "org.eclipse.elk.font.size": 20},
                },
                "port": {
                    "width": 2.0,
                    "height": 2.0,
                    "label": {
                        "text": "Port",
                        "width": 0,
                        "height": 2,
                        "properties": {"org.eclipse.elk.font.name": "Arial", "org.eclipse.elk.font.size": 4},
                    },
                    "properties": {},
                },
                "properties": {
                    "org.eclipse.elk.portConstraints": "FREE",
                    "org.eclipse.elk.portLabels.placement": "[OUTSIDE, NEXT_TO_PORT_IF_POSSIBLE]",
                    "org.eclipse.elk.nodeLabels.placement": "[INSIDE, V_TOP, H_CENTER]",
                },
            },
                "edge_defaults": {
                    "label": {
                        "text": "",
                        "width": 200,
                        "height": 10,
                        "properties": {
                        "org.eclipse.elk.font.name": "Arial",
                        "org.eclipse.elk.font.size": 10,
                        "org.eclipse.elk.edgeLabels.inline": True,
                    },
                },
                "properties": {
                    "org.eclipse.elk.edge.type": "UNDIRECTED",
                    "org.eclipse.elk.edge.thickness": 1,
                },
            },
            "type_icon_map": {
                "router": "mdi:router",
                "switch": "clarity:network-switch-line",
                "mpls": "mdi:cloud-braces",
                "vpn": "material-symbols:cloud-lock-outline",
                "firewall": "clarity:firewall-line",
                "cloud": "material-symbols:cloud-outline",
                "datacenter": "material-symbols:data-table-outline",
                "azure": "codicon:azure",
                "internet": "mdi:web",
                "cpe": "material-symbols:router-outline",
                "database": "mdi:database-outline",
                "server": "mdi:server-outline",
                "host": "clarity:host-line",
                "ran": "mdi:radio-tower",
                "radio": "material-symbols:cell-tower",
                "splitter": "mdi:axis-arrow",
                "devices": "mdi:devices",
                "satelliteuplink": "mdi:satellite-uplink",
                "satellite": "mdi:satellite-variant",
                "broadcast": "mdi:cast-audio-variant",
                "lan": "mdi:lan",
                "diagnostics": "mdi:bug-outline",
                "analytics": "mdi:chart-line",
                "monitor": "mdi:monitor-dashboard",
                "logging": "mdi:book-edit-outline",
                "iam": "material-symbols:identity-platform-outline",
                "idea": "mdi:lightbulb-on-outline",
                "tools": "mdi:tools",
                "cctv": "mdi:cctv",
                "process": "mdi:cog-refresh-outline",
                "cooling": "mdi:fan",
                "security": "mdi:lock-outline",
                "console": "mdi:remote-desktop",
                "gis": "mdi:map-marker-outline",
                "city": "mdi:home-city-outline",
                "settlement": "mdi:home-group",
                "sdu": "mdi:home-outline",
                "mdu": "mdi:office-building-outline",
                "company": "mdi:domain",
                "farm": "mdi:farm-home-outline",
                "airport": "mdi:airplane",
                "mine": "mdi:hammer",
                "fieldservice": "mdi:briefcase-variant-outline",
                "facility": "mdi:garage-variant-lock",
                "energy": "mdi:battery-50",
                "transmission": "material-symbols:graph-3",
                "ip": "streamline:cloud-share",
                "mobilecore": "mdi:mobile-phone-settings-variant",
                "access": "mdi:connection",
                "operation": "mdi:account-cog-outline",
                "controller": "mdi:account-tie-hat-outline",
                "product": "mdi:cart-outline",
                "consumer": "mdi:account-outline",
                "fortinet": "simple-icons:fortinet",
                "juniper": "simple-icons:junipernetworks",
                "ericsson": "simple-icons:ericsson",
                "huawei": "simple-icons:huawei",
                "cisco": "simple-icons:cisco",
                "mikrotik": "simple-icons:mikrotik",
                "dell": "simple-icons:dell",
                "ubiquiti": "simple-icons:ubiquiti",
            },
        }
    )
