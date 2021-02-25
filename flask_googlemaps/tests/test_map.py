import pytest
from flask_googlemaps import Map


class TestFunctionAddMarker:
    """
        This Class is to test function add marker.
    """

    google_map = None

    @pytest.fixture(autouse=True)
    def config_test(self):
        self.google_map = Map(
            identifier="view-side",  # for DOM element
            varname="mymap",  # for JS object name
            lat=37.4419,
            lng=-122.1419,
        )

    @pytest.mark.parametrize("marker", [{}, {"lat": 1}, {"lng": 1}])
    def test_should_raise_attribute_error_when_is_missing_params(self, marker):
        """
            Test check the validation of marker.
            This should raise expetion when the lat, lng or both are missing.
        """
        with pytest.raises(AttributeError) as error:
            self.google_map.add_marker(**marker)

        assert str(error.value) == "lat and lng required"

    @pytest.mark.parametrize(
        "marker",
        [
            {"lat": 10, "lng": 20, "icon": "red"},
            {"lat": 10, "lng": 20, "icon": "red", "infobox": "teste"},
        ],
    )
    def test_it_should_add_to_marker_list_a_new_valid_marker(self, marker):
        """
            Test check if add_marker is adding a new market to markers_list.
        """
        self.google_map.add_marker(**marker)
        assert len(self.google_map.markers) == 1
