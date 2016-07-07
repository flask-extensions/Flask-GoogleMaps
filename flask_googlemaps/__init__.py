# coding: utf-8

from flask import render_template, Blueprint, Markup, g
from flask_googlemaps.icons import dots
DEFAULT_ICON = dots.red


class Map(object):
    def __init__(self,
                 identifier,
                 lat,
                 lng,
                 zoom=13,
                 maptype="ROADMAP",
                 markers=None,
                 varname='map',
                 style="height:300px;width:300px;margin:0;",
                 cls="map",
                 rectangles=None,
                 drawing=False,
                 zoom_control=True,
                 maptype_control=True,
                 scale_control=True,
                 streetview_control=True,
                 rotate_control=True,
                 fullscreen_control=True,
                 **kwargs):
        """Builds the Map properties"""
        self.cls = cls
        self.style = style
        self.varname = varname
        self.center = (lat, lng)
        self.zoom = zoom
        self.maptype = maptype
        self.markers = []
        self.build_markers(markers)
        # Following the same pattern of building markers for rectangles objs
        self.rectangles = []
        self.build_rectangles(rectangles)

        self.identifier = identifier
        self.zoom_control = zoom_control
        self.maptype_control = maptype_control
        self.scale_control = scale_control
        self.streetview_control = streetview_control
        self.rotate_control = rotate_control
        self.fullscreen_control = fullscreen_control

    def build_markers(self, markers):
        if not markers:
            return
        if not isinstance(markers, (dict, list, tuple)):
            raise AttributeError('markers accepts only dict, list and tuple')

        if isinstance(markers, dict):
            for icon, marker_list in markers.items():
                for marker in marker_list:
                    marker_dict = self.build_marker_dict(marker, icon=icon)
                    self.add_marker(**marker_dict)
        else:
            for marker in markers:
                if isinstance(marker, dict):
                    self.add_marker(**marker)
                elif isinstance(marker, (tuple, list)):
                    marker_dict = self.build_marker_dict(marker)
                    self.add_marker(**marker_dict)

    def build_marker_dict(self, marker, icon=None):
        marker_dict = {
            'lat': marker[0],
            'lng': marker[1],
            'icon': icon or DEFAULT_ICON
        }
        if len(marker) > 2:
            marker_dict['infobox'] = marker[2]
        if len(marker) > 3:
            marker_dict['icon'] = marker[3]
        return marker_dict

    def add_marker(self, lat=None, lng=None, **kwargs):
        if lat:
            kwargs['lat'] = lat
        if lng:
            kwargs['lng'] = lng
        if 'lat' not in kwargs or 'lng' not in kwargs:
            raise AttributeError('lat and lng required')
        self.markers.append(kwargs)

    def build_rectangles(self, rectangles):
        """ Process data to construct rectangles

        This method is built from the assumption that the rectangles parameter
        is a list of:
            lists : a list with 4 elements indicating [north, west, south, east]
            tuples: a tuple with 4 elements indicating (north, west, south,east)
            tuple of tuples: a tuple of 2 tuple elements of length 2 indicating
            (north_west, south_east)
            dicts: a dictionary with rectangle attributes

        So, for instance, we have this general scenario as a input parameter:
            [[22.345,45.44,23.345, 45.55],
             (22.345,45.44,23.345,45.55),
             ((22.345,45.44),(23.345,45.55)),
             [(22.345,45.44),(23.345,45.55)],
             {
            'stroke_color': stroke_color,
            'stroke_opacity': stroke_opacity,
            'stroke_weight': stroke_weight,
            'fill_color': fill_color,
            'fill_opacity': fill_opacity,
            'bounds': {'north': north,
                       'east': east,
                       'south': south,
                       'west': west,
                       }
            }]
        """

        if not rectangles:
            return
        if not isinstance(rectangles, list):
            raise AttributeError('rectangles only accept lists as parameters')
        for rect in rectangles:

            # Check the instance of one rectangle in the list. Can be
            # list, tuple or dict
            if isinstance(rect, (list, tuple)):

                # If the rectangle bounds doesn't have size 4 or 2
                # an AttributeError is raised
                if len(rect) != 4:
                    if len(rect) != 2:
                        raise AttributeError('The bound must have length'
                                             ' 4 or 2')

                # If the tuple or list has size 4, the bounds order are
                # especified as north, west, south, east
                if len(rect) == 4:
                    rect_dict = self.build_rectangle_dict(*rect)
                    self.add_rectangle(**rect_dict)

                # Otherwise size 2, the tuple or list have the north_west and
                # south_east tuples. If the tuples doesn't have the correct
                # size, an AttributeError is raised.
                elif len(rect) == 2:
                    if len(rect[0]) != 2 or len(rect[1]) != 2:
                        raise AttributeError('Wrong size of rectangle bounds')
                    rect_dict = self.build_rectangle_dict(rect[0][0],
                                                          rect[0][1],
                                                          rect[1][0],
                                                          rect[1][1])
                    self.add_rectangle(**rect_dict)
                else:
                    raise AttributeError('Wrong bounds input size')
            elif isinstance(rect, dict):
                self.add_rectangle(**rect)

    def build_rectangle_dict(self,
                             north,
                             west,
                             south,
                             east,
                             stroke_color='#FF0000',
                             stroke_opacity=.8,
                             stroke_weight=2,
                             fill_color='#FF0000',
                             fill_opacity=.3,
                             ):
        """ Set a dictionary with the javascript class Rectangle parameters

        This function sets a default drawing configuration if the user just
        pass the rectangle bounds, but also allows to set each parameter
        individually if the user wish so.

        Args:
            north (float): The north latitude bound
            west (float): The west longitude bound
            south (float): The south latitude bound
            east (float): The east longitude bound
            stroke_color (str): Sets the color of the rectangle border using
                hexadecimal color notation
            stroke_opacity (float): Sets the opacity of the rectangle border
                in percentage. If stroke_opacity = 0, the border is transparent
            stroke_weight (int): Sets the stroke girth in pixels.
            fill_color (str): Sets the color of the rectangle fill using
                hexadecimal color notation
            fill_opacity (float): Sets the opacity of the rectangle fill


        """
        rectangle = {
            'stroke_color': stroke_color,
            'stroke_opacity': stroke_opacity,
            'stroke_weight': stroke_weight,
            'fill_color': fill_color,
            'fill_opacity': fill_opacity,
            'bounds': {'north': north,
                       'west': west,
                       'south': south,
                       'east': east,
                       }
        }

        return rectangle

    def add_rectangle(self,
                      north=None,
                      west=None,
                      south=None,
                      east=None,
                      **kwargs):
        """ Adds a rectangle dict to the Map.rectangles attribute

        The Google Maps API describes a rectangle using the LatLngBounds
        object, which defines the bounds to be drawn. The bounds use the
        concept of 2 delimiting points, a northwest and a southeast points,
        were each coordinate is defined by each parameter.

        It accepts a rectangle dict representation as well.

        Args:
            north (float): The north latitude
            west (float): The west longitude
            south (float): The south latitude
            east (float): The east longitude

        .. _LatLngBoundsLiteral:
            https://developers.google.com/maps/documentation/javascript/reference#LatLngBoundsLiteral

        .. _Rectangles:
            https://developers.google.com/maps/documentation/javascript/shapes#rectangles
        """

        if north:
            kwargs['bounds']['north'] = north
        if west:
            kwargs['bounds']['west'] = west
        if south:
            kwargs['bounds']['south'] = south
        if east:
            kwargs['bounds']['east'] = east

        if 'bounds' not in kwargs:
            raise AttributeError('bounds required to build rectangles')

        if 'bounds' in kwargs \
                and {'north', 'east', 'south', 'west'} \
                != kwargs['bounds'].keys():
            raise AttributeError('rectangle bounds required to rectangles')

        if 'stroke_color' not in kwargs:
            kwargs['stroke_color'] = '#FF0000'
        if 'stroke_opacity' not in kwargs:
            kwargs['stroke_opacity'] = .8
        if 'stroke_weight' not in kwargs:
            kwargs['stroke_weight'] = 2
        if 'fill_color' not in kwargs:
            kwargs['fill_color'] = '#FF0000'
        if 'fill_opacity' not in kwargs:
            kwargs['fill_opacity'] = .3

        self.rectangles.append(kwargs)

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def js(self):
        return Markup(
            self.render(
                'googlemaps/gmapjs.html',
                gmap=self,
                DEFAULT_ICON=DEFAULT_ICON
            )
        )

    @property
    def html(self):
        return Markup(self.render('googlemaps/gmap.html', gmap=self))


def googlemap_obj(*args, **kwargs):
    map = Map(*args, **kwargs)
    return map


def googlemap(*args, **kwargs):
    map = googlemap_obj(*args, **kwargs)
    return Markup("".join((map.js, map.html)))


def googlemap_html(*args, **kwargs):
    return googlemap_obj(*args, **kwargs).html


def googlemap_js(*args, **kwargs):
    return googlemap_obj(*args, **kwargs).js


def set_googlemaps_loaded():
    g.googlemaps_loaded = True
    return ''


def is_googlemaps_loaded():
    return getattr(g, 'googlemaps_loaded', False)


class GoogleMaps(object):
    def __init__(self, app=None, **kwargs):
        self.key = kwargs.get('key')
        if app:
            self.init_app(app)

    def init_app(self, app):
        if self.key:
            app.config['GOOGLEMAPS_KEY'] = self.key
        self.register_blueprint(app)
        app.add_template_filter(googlemap_html)
        app.add_template_filter(googlemap_js)
        app.add_template_global(googlemap_obj)
        app.add_template_filter(googlemap)
        app.add_template_global(googlemap)
        app.add_template_global(
            app.config.get('GOOGLEMAPS_KEY'), name='GOOGLEMAPS_KEY')
        app.add_template_global(set_googlemaps_loaded)
        app.add_template_global(is_googlemaps_loaded)

    def register_blueprint(self, app):
        module = Blueprint(
            "googlemaps", __name__, template_folder="templates"
        )
        app.register_blueprint(module)
        return module
