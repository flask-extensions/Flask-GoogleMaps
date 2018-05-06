"""
The idea is to implement all icons from here:
http://kml4earth.appspot.com/icons.html#mapfiles
and
http://jg.org/mapping/icons.html
and
http://mabp.kiev.ua/2010/01/12/google-map-markers/
"""

__all__ = ['dots', 'alpha','shapes','pushpin']


class Icon(object):
    """Dynamically return dot icon url"""

    def __init__(self, base_url, options=None):
        self.base_url = base_url
        self.options = options

    def __getattr__(self, item):
        return self.base_url.format(item)


dots = Icon(
    base_url='//maps.google.com/mapfiles/ms/icons/{0}-dot.png',
    options=['blue', 'yellow', 'green', 'red', 'pink', 'purple', 'red']
)

alpha = Icon(
    base_url='//www.google.com/mapfiles/marker{0}.png',
    options=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'X', 'Z', 'W', 'Y']
)

shapes = Icon(
    base_url='//www.google.com/mapsfiles/kml/shapes/{0}.png',
    options=['airports', 'arrow', 'arrow-reverse', 'arts', 'bars', 
             'broken_link', 'bus', 'cabs', 'camera', 'campfire', 'campground', 
             'capital_big', 'capital_big_highlight', 'capital_small', 
             'capital_small_highlight', 'caution', 'church', 'coffee', 'convenience', 
             'cross-hairs', 'cross-hairs_highlight', 'cycling', 'dining', 'dollar', 
             'donut', 'earthquake', 'electronics', 'euro', 'falling_rocks', 'ferry', 
             'firedept', 'fishing', 'flag', 'forbidden', 'gas_stations', 'golf', 
             'grocery', 'heliport', 'highway', 'hiker', 'homegardenbusiness',
             'horsebackriding', 'hospitals', 'info', 'info-i', 'info_circle', 
             'lodging', 'man', 'marina', 'mechanic', 'motorcycling', 'mountains', 
             'movies', 'open-diamond', 'parking_lot', 'parks', 'partly_cloudy', 
             'pharmacy_rx', 'phone', 'picnic', 'placemark_circle', 
             'placemark_circle_highlight', 'placemark_square', 
             'placemark_square_highlight', 'play', 'poi', 'police', 
             'polygon', 'post_office', 'rail', 'rainy', 'ranger_station', 
             'realestate', 'road_shield1', 'road_shield2', 'road_shield3', 
             'ruler', 'sailing', 'salon', 'schools', 'shaded_dot', 'shopping', 
             'ski', 'snack_bar', 'snowflake_simple', 'square', 'star', 'subway', 
             'sunny', 'swimming', 'target', 'terrain', 'thunderstorm', 'toilets', 
             'trail', 'tram', 'triangle', 'truck', 'volcano', 'water', 'webcam', 
             'wheel_chair_accessible', 'woman', 'yen']
)
pushpin = Icon(
    base_url='//www.google.com/mapsfiles/kml/pushpin/{0}.png',
    options=['blue-pushpin', 'grn-pushpin', 'ltblu-pushpin', 'pink-pushpin', 
             'purple-pushpin', 'red-pushpin', 'wht-pushpin', 'ylw-pushpin']
)
