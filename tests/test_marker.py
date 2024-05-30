from typing import Dict

import pytest

from flask_googlemaps.marker import Marker
from flask_googlemaps.pin import Pin


@pytest.fixture
def coordinates() -> Dict[str, float]:
    return dict(latitude=37.4419, longitude=-122.1419)


@pytest.fixture
def marker_pin_object(coordinates) -> Marker:
    return Marker(
        content=dict(border_color="", glyph_color="", background=""),
        infobox="<b>Hello World</b>",
        **coordinates
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


def test_from_list_dictionary(coordinates):
    markers = Marker.from_list([coordinates])
    for marker in markers:
        assert isinstance(marker, Marker)


def test_from_list_tuple(coordinates):
    markers = Marker.from_list(
        [(coordinates["latitude"], coordinates["longitude"])]
    )
    for marker in markers:
        assert isinstance(marker, Marker)


def test_from_list_mixed_tuple_dict(coordinates):
    markers = Marker.from_list(
        [(coordinates["latitude"], coordinates["longitude"]), coordinates]
    )
    for marker in markers:
        assert isinstance(marker, Marker)


def test_from_list_type_error(coordinates):
    with pytest.raises(TypeError) as exception_info:
        Marker.from_list([[coordinates["latitude"], coordinates["longitude"]]])
    assert str(exception_info.value) == (
        "Marker must be either a dict or a tuple."
    )
