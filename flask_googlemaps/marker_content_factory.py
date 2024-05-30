from enum import Enum
from typing import Optional

from flask_googlemaps.image import Image
from flask_googlemaps.marker_content import MarkerContent
from flask_googlemaps.pin import Pin


class MarkerContentType(Enum):
    PIN = 1
    IMAGE = 2


class MarkerContentFactory:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if "icon_url" in kwargs:
            self.__content_type = MarkerContentType.IMAGE
        elif (
            "border_color" in kwargs
            or "glyph_color" in kwargs
            or "background" in kwargs
            or "glyph" in kwargs
            or "scale" in kwargs
        ):
            self.__content_type = MarkerContentType.PIN
        else:
            self.__content_type = None

    @property
    def marker_content(self) -> Optional[MarkerContent]:
        if self.__content_type is MarkerContentType.PIN:
            try:
                return Pin(**self.kwargs)
            except TypeError as e:
                print(e)
                return Pin()
        elif self.__content_type is MarkerContentType.IMAGE:
            try:
                return Image(**self.kwargs)
            except TypeError as e:
                print(e)
                return Pin()
        else:
            return Pin()
