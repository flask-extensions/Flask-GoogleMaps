from dataclasses import dataclass

from flask_googlemaps.marker_content import MarkerContent


@dataclass
class Image(MarkerContent):
    icon_url: str

    def content(self) -> str:
        return self.name

    def dom_element(self) -> str:
        return (
            f"const {self.name} = document.createElement('img');\n"
            f"{self.name}.src = '{self.icon_url}';"
        )
