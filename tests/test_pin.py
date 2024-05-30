import json

import pytest

from flask_googlemaps.pin import Pin, PinPropertyMapping


@pytest.fixture
def empty_pin():
    return Pin()


@pytest.fixture
def pin():
    return Pin(border_color="red", scale=2.0)


def test_content_empty(empty_pin):
    content = empty_pin.content()
    assert content == ""


def test_content(pin):
    content = pin.content()
    assert content.startswith("var_")
    assert len(content) == 20


@pytest.mark.parametrize(
    "p",
    [
        Pin(border_color="blue", scale=3.0),
        Pin(background="red", glyph_color="black", scale=2.0),
        Pin(glyph="Test", border_color="red"),
    ],
)
def test_dom_element(p):
    dom_element = p.dom_element()
    _, js_element = dom_element.split(" = ")

    js_element = js_element_to_dict(js_element)
    reversed_dict = {item.value: item.name for item in list(PinPropertyMapping)}

    for property_name, value in js_element.items():
        if property_name == "scale":
            value = float(value)
        assert value == p.__getattribute__(reversed_dict[property_name])


def js_element_to_dict(js_element: str) -> dict:
    js_element = (
        js_element.strip("new PinElement(")
        .strip(");\n")
        .replace("\n", "")
        .replace("\t", "")
        .replace("'", '"')
        .replace("{", '{"')
        .replace(",}", "}")
        .replace(",", ',"')
        .replace(":", '":')
    )

    return json.loads(js_element)
