from dataclasses import dataclass
from typing import Optional

from flask_googlemaps.marker_content import MarkerContent


@dataclass
class Pin(MarkerContent):

    def __post_init__(self):
        MarkerContent.__post_init__(self)
        self.dom = []
        if self.glyph_color:
            self.dom.append(f"\tglyphColor: '{self.glyph_color}',")
        if self.background:
            self.dom.append(f"\tbackground: '{self.background}',")
        if self.border_color:
            self.dom.append(f"\tborderColor: '{self.border_color}',")
        if self.glyph:
            self.dom.append(f"\tglyph: '{self.glyph}',")
        if self.dom:
            self.dom.insert(0, f"const {self.name} = new PinElement({{")
            self.dom.append("\t\t});\n")

    def dom_element(self) -> Optional[str]:

        if self.dom:
            return "\n".join(self.dom)
        return None

    border_color: str = ""
    glyph_color: str = ""
    background: str = ""
    glyph: Optional[str] = ""
    scale: float = 1.0

    def content(self) -> str:
        if self.dom:
            return f"{self.name}.element"
        return ""
