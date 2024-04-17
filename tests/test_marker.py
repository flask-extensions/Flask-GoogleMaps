import pytest

from flask_googlemaps.marker import Marker
from flask_googlemaps.pin import Pin


@pytest.fixture
def marker_pin_object() -> Marker:
    return Marker(
        latitude=37.4419,
        longitude=-122.1419,
        content=dict(border_color="", glyph_color="", background=""),
        infobox="<b>Hello World</b>",
    )


@pytest.fixture
def marker_pin_url() -> Marker:
    return Marker(
        latitude=37.4419,
        longitude=-122.1419,
        content={
            "icon_url": "https://developers.google.com/maps/"
            "documentation/javascript/examples/"
            "full/images/beachflag.png"
        },
        infobox="<b>Hello World</b>",
    )


def test_marker_without_lat_long():
    with pytest.raises(TypeError):
        Marker()


def test_marker_with_wrong_latitude():
    with pytest.raises(AttributeError) as exception_info:
        Marker(latitude=150, longitude=150)
    assert str(exception_info.value) == (
        "Latitude must be between -90 and 90 degrees inclusive."
    )


def test_marker_with_wrong_longitude():
    with pytest.raises(AttributeError) as exception_info:
        Marker(latitude=90, longitude=-190)
    assert str(exception_info.value) == (
        "Longitude must be between -180 and 180 degrees inclusive."
    )


def test_marker_with_pin_object(marker_pin_object):
    assert isinstance(marker_pin_object.marker_content, Pin)
