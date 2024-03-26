import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Pin:
    border_color: str
    glyph_color: str
    background: str
    glyph: Optional[str] = None
    uuid: Optional[str] = field(default_factory=lambda: f"_{str(uuid.uuid1())[0:8]}")
    scale: float = 1.0
