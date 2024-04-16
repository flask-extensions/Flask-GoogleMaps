import pytest

from flask_googlemaps.image import Image


@pytest.fixture
def image():
    return Image(
        icon_url="https://developers.google.com/maps/documentation/"
        "javascript/examples/full/images/beachflag.png"
    )


def test_content(image):
    content = image.content()
    assert content.startswith("var_")
    assert len(content) == 12


def test_dom_image_element(image):
    variable, url_set = image.dom_element().split("\n")
    assert variable == f"const {image.name} = document.createElement('img');"
    assert url_set == f"{image.name}.src = '{image.icon_url}';"
