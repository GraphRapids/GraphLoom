from uuid import uuid4

from pydantic import BaseModel


def _gen_id(prefix: str) -> str:
    """Generate a unique identifier with the given prefix.

    Produces a string of the form ``<prefix>_<hex>`` where ``<hex>`` is an
    8-character random hexadecimal suffix derived from a UUID4.

    Args:
        prefix: A string prepended to the generated identifier.

    Returns:
        A unique prefixed identifier, e.g. ``"node_a1b2c3d4"``.
    """
    return f"{prefix}_{uuid4().hex[:8]}"


class Properties(BaseModel):
    model_config = {"extra": "allow"}
