# coding: utf-8

from flask import render_template, Blueprint, Markup

DEFAULT_ICON = '//maps.google.com/mapfiles/ms/icons/red-dot.png'


class Map(object):
    def __init__(self, identifier, lat, lng,
                 zoom=13, maptype="ROADMAP", markers=None,
                 varname='map',
                 style="height:300px;width:300px;margin:0;",
                 cls="map", **kwargs):
        self.cls = cls
        self.style = style
        self.varname = varname
        self.center = (lat, lng)
        self.zoom = zoom
        self.maptype = maptype
        self.markers = markers or []
        if isinstance(markers, list):
            self.markers = {DEFAULT_ICON: markers}
        self.identifier = identifier
        if 'infobox' in kwargs:
            self.infobox = kwargs['infobox']
            # jinja2 has no builtin for type so a flag is set to check if infobox is
            # string or list for the template iteration
            if type(kwargs['infobox']) is list:
                self.typeflag = True
        else:
            self.infobox = None

    def add_marker(self, lat, lng):
        self.markers.append((lat, lng))

    def render(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    @property
    def js(self):
        return Markup(self.render('googlemaps/gmapjs.html', gmap=self))

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


class GoogleMaps(object):
    def __init__(self, app=None, **kwargs):
        self.key = kwargs.get('key')
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.config['GOOGLEMAPS_KEY'] = self.key
        self.register_blueprint(app)
        app.add_template_filter(googlemap_html)
        app.add_template_filter(googlemap_js)
        app.add_template_global(googlemap_obj)
        app.add_template_filter(googlemap)
        app.add_template_global(googlemap)

    def register_blueprint(self, app):
        module = Blueprint("googlemaps", __name__,
            template_folder="templates")
        app.register_blueprint(module)
        return module
