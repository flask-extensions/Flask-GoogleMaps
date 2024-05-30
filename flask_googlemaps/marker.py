from typing import Optional, List, Any, Dict, Tuple

from flask_googlemaps.marker_content_factory import MarkerContentFactory


class Marker(dict):

    def __init__(
        self,
        latitude: float,
        longitude: float,
        infobox: Optional[str] = None,
        content: Optional[dict] = {},
    ):
        self.latitude = Marker.verify_latitude(latitude)
        self.longitude = Marker.verify_longitude(longitude)
        self.infobox = infobox
        self.marker_content = MarkerContentFactory(**content).marker_content
        self.content = self.marker_content.content()
        self.dom_element = self.marker_content.dom_element()

        dict.__init__(
            self,
            {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "infobox": self.infobox,
                "content": self.content,
                "id": self.marker_content.name,
            },
        )

    @staticmethod
    def verify_latitude(latitude: float) -> Optional[float]:
        if not (90 >= latitude >= -90):
            raise AttributeError(
                "Latitude must be between -90 and 90 degrees inclusive."
            )
        return latitude

    @staticmethod
    def verify_longitude(longitude: float) -> Optional[float]:
        if not (180 >= longitude >= -180):
            raise AttributeError(
                "Longitude must be between -180 and 180 degrees inclusive."
            )
        return longitude

    @staticmethod
    def from_list(
        markers: List[Optional[Dict[str, Any] | Tuple[float, float]]]
    ) -> List["Marker"]:
        if not markers:
            return []
        return list(map(marker_constructor, markers))


def marker_constructor(marker: Dict[str, Any] | Tuple[float, float]) -> Marker:
    if isinstance(marker, dict):
        return Marker(**marker)
    elif isinstance(marker, tuple):
        return Marker(latitude=marker[0], longitude=marker[1])
    else:
        raise TypeError("Marker must be either a dict or a tuple.")
