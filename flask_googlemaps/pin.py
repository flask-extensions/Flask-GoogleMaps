from dataclasses import dataclass, fields
from enum import Enum
from typing import Optional

from flask_googlemaps.marker_content import MarkerContent

pin_property_mapping = {
    "glyph_color": "glyphColor",
    "background": "background",
    "border_color": "borderColor",
    "glyph": "glyph",
    "scale": "scale",
}


class PinPropertyMapping(Enum):
    glyph_color = "glyphColor"
    background = "background"
    border_color = "borderColor"
    glyph = "glyph"
    scale = "scale"


@dataclass
class Pin(MarkerContent):

    def __post_init__(self):
        MarkerContent.__post_init__(self)
        self.dom = []
        for field in fields(Pin):
            if self.__getattribute__(field.name):
                self.dom.append(
                    f"\t{PinPropertyMapping.__getitem__(field.name).value}: "
                    f"'{self.__getattribute__(field.name)}',"
                )

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
    scale: Optional[float] = None

    def content(self) -> str:
        if self.dom:
            return f"{self.name}.element"
        return ""
