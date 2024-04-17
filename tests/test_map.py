from typing import Dict, List, Any

import pytest

from flask_googlemaps import Map


@pytest.fixture
def map_properties() -> Dict[str, Any]:
    return dict(identifier="gmap",
                varname="gmap",
                lat=37.4419,
                lng=-122.1419)


@pytest.fixture
def markers() -> List[Dict]:
    return [
        {
            "content": {"icon_url": "http://maps.google.com/"
                                    "mapfiles/ms/icons/green-dot.png"},
            "latitude": 37.4419,
            "longitude": -122.1419,
            "infobox": "<b>Hello World</b>",
        },
        {
            "latitude": 37.4300,
            "longitude": -122.1400,
            "infobox": "<b>Hello World from other place</b>",
            "content": {
                "border_color": "",
                "glyph_colors": "",
                "background": "",
                "glyph": "",
                "scale": 2.0,
            }
        },
    ]


def test_map_markers(markers: List[Dict], map_properties):
    assert len(Map(markers=markers, **map_properties).markers) == 2


def test_map_markers_expected_errors(markers: List[Dict], map_properties):
    markers.append({"latitude": -1, "longitude": 250})
    with pytest.raises(AttributeError) as exception_info:
        Map(markers=markers, **map_properties)
    assert str(exception_info.value) == (
        "Longitude must be between -180 and 180 degrees inclusive."
    )
