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

    def add_rectangle(self, north_east=None, south_west=None, **kwargs):
        """ Adds a rectangle dict to the Map.rectangles attribute

        The Google Maps API describes a rectangle using the LatLngBounds
        object, which defines the bounds to be drawn. The bounds use the
        concept of 2 delimiting points, a northeast and a southwest points,
        described as the parameters north_east and south_west of this function.

        Args:
            north_east (tuple): The north and east bounds of the rectangle
            south_west (tuple): The south and west bounds of the rectangle

        .. _LatLngBounds class:
                https://developers.google.com/maps/documentation/javascript/reference#LatLngBounds

        """

        if north_east:
            kwargs['bounds'] = {}
            kwargs['bounds']['north'] = north_east[0]
            kwargs['bounds']['east'] = north_east[1]

        if south_west:
            kwargs['bounds']['south'] = south_west[0]
            kwargs['bounds']['west'] = south_west[1]

        if 'bounds' not in kwargs:
            raise AttributeError('bounds required to build rectangles')

        if 'bounds' in kwargs \
                and {'north', 'east', 'south', 'west'} \
                != kwargs['bounds'].keys():
            raise AttributeError('bounds directions required to rectangles')

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
