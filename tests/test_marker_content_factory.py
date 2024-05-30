from flask_googlemaps.marker_content_factory import MarkerContentFactory
from flask_googlemaps.pin import Pin


def test_marker_content_unknown_keys():
    marker_content_factory = MarkerContentFactory(**{"bla": "bla"})
    marker_content = marker_content_factory.marker_content
    assert isinstance(marker_content, Pin)
    assert marker_content.dom_element() is None


def test_marker_content_unknown():
    marker_content_factory = MarkerContentFactory(
        **{"background": "", "glyph_colors": ""}
    )
    marker_content = marker_content_factory.marker_content
    assert isinstance(marker_content, Pin)
    assert marker_content.dom_element() is None
