from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping

from .canvas import Canvas
from .settings import ElkSettings

if TYPE_CHECKING:  # pragma: no cover
    from .builder import MinimalGraphIn


@dataclass(frozen=True)
class ResolvedProfileElkSettings:
    profile_id: str
    profile_version: int
    checksum: str
    settings: ElkSettings


def _require_bundle_field(bundle: Mapping[str, Any], key: str) -> Any:
    if key not in bundle:
        raise ValueError(f"Profile bundle is missing required field '{key}'.")
    return bundle[key]


def resolve_profile_elk_settings(bundle: Mapping[str, Any]) -> ResolvedProfileElkSettings:
    profile_id = str(_require_bundle_field(bundle, "profileId"))
    profile_version = int(_require_bundle_field(bundle, "profileVersion"))
    checksum = str(_require_bundle_field(bundle, "checksum"))
    elk_settings = _require_bundle_field(bundle, "elkSettings")

    if not isinstance(elk_settings, Mapping):
        raise ValueError("Profile bundle field 'elkSettings' must be an object.")

    # Canonicalize key order to keep downstream JSON dumps deterministic.
    canonical_settings = json.loads(
        json.dumps(elk_settings, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    )
    settings = ElkSettings.model_validate(canonical_settings)

    return ResolvedProfileElkSettings(
        profile_id=profile_id,
        profile_version=profile_version,
        checksum=checksum,
        settings=settings,
    )


def build_canvas_from_profile_bundle(
    graph: "MinimalGraphIn",
    bundle: Mapping[str, Any],
) -> tuple[Canvas, ResolvedProfileElkSettings]:
    from .builder import build_canvas

    resolved = resolve_profile_elk_settings(bundle)
    return build_canvas(graph, resolved.settings), resolved
