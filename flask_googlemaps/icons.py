"""
The idea is to implement all icons from here:
http://kml4earth.appspot.com/icons.html#mapfiles
and
http://jg.org/mapping/icons.html
"""

__all__ = ['dots']


class Dots(object):
    """Dynbamically return dot icon url"""

    all = [
        'blue', 'yellow', 'green', 'red', 'pink', 'purple', 'red'
    ]

    def __getattr__(self, item):
        return '//maps.google.com/mapfiles/ms/icons/{0}-dot.png'.format(item)


dots = Dots()
