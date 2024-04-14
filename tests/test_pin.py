import pytest

from flask_googlemaps.pin import Pin


@pytest.fixture
def pin():
    return Pin()


def test_content(pin):
    content = pin.content()
    assert False
