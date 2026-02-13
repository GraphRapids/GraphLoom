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
    icon: str | None = None
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
    type_icon_map: Dict[str, str] = Field(default_factory=dict)
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
                "type": "default",
                "icon": None,
                "width": 50,
                "height": 50,
                "label": {
                    "text": "Node",
                    "width": 150,
                    "height": 16,
                    "properties": {"org.eclipse.elk.font.size": 16},
                },
                "port": {
                    "width": 2.0,
                    "height": 2.0,
                    "label": {
                        "text": "Port",
                        "width": 50,
                        "height": 6,
                        "properties": {"org.eclipse.elk.font.size": 6},
                    },
                    "properties": {"org.eclipse.elk.port.index": 0},
                },
                "properties": {
                    "org.eclipse.elk.portConstraints": "[FIXED_ORDER]",
                    "org.eclipse.elk.portLabels.placement": "[OUTSIDE, NEXT_TO_PORT_IF_POSSIBLE]",
                    "org.eclipse.elk.nodeLabels.placement": "[OUTSIDE, V_BOTTOM, H_CENTER, H_PRIORITY]",
                },
            },
            "edge_defaults": {
                "label": {
                    "text": "Edge",
                    "width": 100,
                    "height": 10,
                    "properties": {
                        "org.eclipse.elk.font.size": 10,
                        "org.eclipse.elk.edgeLabels.inline": False,
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
