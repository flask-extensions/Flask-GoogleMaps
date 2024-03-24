from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Pin:
    border_color: str
    glyph_color: str
    background: str
    glyph: Optional[str] = None
    scale: float = 1.0
