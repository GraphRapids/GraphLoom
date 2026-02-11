from uuid import uuid4

from pydantic import BaseModel


def _gen_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:8]}"


class Properties(BaseModel):
    model_config = {"extra": "allow"}
