"""
The idea is to implement all icons from here:
http://kml4earth.appspot.com/icons.html#mapfiles
and
http://jg.org/mapping/icons.html
and
http://mabp.kiev.ua/2010/01/12/google-map-markers/
"""

__all__ = ['dots', 'alpha', 'shapes', 'pushpin', 'paddle']


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
    options=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'X', 'Z', 'W', 'Y']
)

shapes = Icon(
    base_url='//maps.google.com/mapfiles/kml/shapes/{0}.png',
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
    base_url='//maps.google.com/mapfiles/kml/pushpin/{0}.png',
    options=['blue-pushpin', 'grn-pushpin', 'ltblu-pushpin', 'pink-pushpin', 
             'purple-pushpin', 'red-pushpin', 'wht-pushpin', 'ylw-pushpin']
)

paddle = Icon(
    base_url='//maps.google.com/mapfiles/kml/paddle/{0}.png',
    options=['1-lv','2-lv','3-lv','4-lv','5-lv','6-lv','7-lv','8-lv','9-lv','10-lv',
             '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
             'X', 'W', 'Y', 'Z',
             'blu-blank-lv', 'blu-blank', 'blu-circle-lv', 'blu-circle', 'blu-diamond-lv', 'blu-diamond', 'blu-square-lv', 'blu-square', 'blu-stars-lv', 'blu-stars', 
             'grn-blank-lv', 'grn-blank', 'grn-circle-lv', 'grn-circle', 'grn-diamond-lv', 'grn-diamond', 'grn-square-lv', 'grn-square', 'grn-stars-lv', 'grn-stars', 
             'ltblu-blank', 'ltblu-circle', 'ltblu-diamond', 'ltblu-square', 'ltblu-stars',
             'pink-blank', 'pink-circle', 'pink-diamond', 'pink-square', 'pink-stars',
             'purple-blank', 'purple-circle-lv', 'purple-circle', 'purple-diamond-lv', 'purple-diamond', 'purple-square-lv', 'purple-square', 'purple-stars-lv', 'purple-stars',
             'red-circle-lv', 'red-circle', 'red-diamond-lv', 'red-diamond', 'red-square-lv', 'red-square', 'red-stars-lv', 'red-stars',
             'wht-blank', 'wht-blank-lv', 'wht-circle-lv', 'wht-circle', 'wht-diamond-lv', 'wht-diamond', 'wht-square-lv', 'wht-square', 'wht-stars-lv', 'wht-stars',
             'ylw-blank', 'ylw-blank-lv', 'ylw-circle-lv', 'ylw-circle', 'ylw-diamond-lv', 'ylw-diamond', 'ylw-square-lv', 'ylw-square', 'ylw-stars-lv', 'ylw-stars',
             'orange-blank',  'orange-circle', 'orange-diamond', 'orange-square', 'orange-stars', 
             'go-lv', 'go', 'pause-lv', 'pause', 'stop-lv', 'stop', 'route'
            ]
)
