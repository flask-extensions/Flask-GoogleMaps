from typing import Optional, List, Any, Dict

from flask_googlemaps.marker_content import MarkerContent
from flask_googlemaps.pin import Pin

DEFAULT_PIN = Pin()


# from json import JSONEncoder
#
#
# def wrapped_default(self, obj):
#     return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)
#
#
# wrapped_default.default = JSONEncoder().default
#
# # apply the patch
# JSONEncoder.original_default = JSONEncoder.default
# JSONEncoder.default = wrapped_default


class Marker(dict):

    def __init__(
        self,
        latitude: float,
        longitude: float,
        infobox: Optional[str] = None,
        content: Optional[MarkerContent] = None,
        label: Optional[str] = None,
    ):
        self.latitude = Marker.verify_latitude(latitude)
        self.longitude = Marker.verify_longitude(longitude)
        self.infobox = infobox
        self.marker_icon = content
        self.content = content.content()
        self.dom_element = content.dom_element()
        self.label = label

        dict.__init__(
            self,
            {
                "latitude": self.latitude,
                "longitude": self.longitude,
                "infobox": self.infobox,
                "content": self.content,
                "id": self.marker_icon.name,
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
    def from_list(markers: List[Dict[str, Any]]) -> List["Marker"]:
        return list(map(lambda marker: Marker(**marker), markers))
