"""FlaskGoogleMaps - Google Maps Extension for Flask"""

__version__ = "0.5.0"

from json import dumps
from typing import Optional, Dict, Any, List, Union, Tuple, Text  # noqa: F401

import requests
from flask import Blueprint, g, render_template
from markupsafe import Markup

from flask_googlemaps.marker import Marker

DEFAULT_CLUSTER_IMAGE_PATH = "static/images/m"


class Map(object):
    def __init__(
        self,
        identifier,  # type: str
        lat,  # type: float
        lng,  # type: float
        zoom=13,  # type: int
        maptype="ROADMAP",  # type: str
        markers=None,  # type: Optional[Union[Dict, List, Tuple]]
        varname="map",  # type: str
        style="height:300px;width:300px;margin:0;",  # type: str
        cls="map",  # type: str
        language="en",  # type: str
        region="US",  # type: str
        rectangles=None,
        # type: Optional[List[Union[List, Tuple, Tuple[Tuple], Dict]]]
        circles=None,  # type: Optional[List[Union[List, Tuple, Dict]]]
        polylines=None,  # type: Optional[List[Union[List, Tuple, Dict]]]
        polygons=None,  # type: Optional[List[Union[List, Tuple, Dict]]]
        zoom_control=True,  # type: bool
        maptype_control=True,  # type: bool
        scale_control=True,  # type: bool
        streetview_control=True,  # type: bool
        rotate_control=True,  # type: bool
        scroll_wheel=True,  # type: bool
        fullscreen_control=True,  # type: bool
        collapsible=False,  # type: bool
        mapdisplay=False,  # type: bool
        cluster=False,  # type: bool
        cluster_imagepath=DEFAULT_CLUSTER_IMAGE_PATH,  # type: str
        cluster_gridsize=60,  # type: int
        fit_markers_to_bounds=False,  # type: bool
        center_on_user_location=False,  # type: bool
        report_markerClickpos=False,  # type: bool
        report_clickpos=False,  # type: bool
        markerClickpos_uri="",  # type: str
        clickpos_uri="",  # type: str
        styles="",
        layer="",
        map_ids=None,
        bicycle_layer=False,
        heatmap_data=None,
        heatmap_layer=False,
        **kwargs
    ):
        # type: (...) -> None
        """Builds the Map properties"""
        self.cls = cls
        self.style = style
        self.language = language
        self.region = region
        self.varname = varname
        self.center = Marker.verify_latitude(lat), Marker.verify_longitude(lng)
        self.zoom = zoom
        self.maptype = maptype
        self.markers = Marker.from_list(markers)  # type: List[Marker]
        self.map_ids = map_ids
        self.rectangles = []  # type: List[Any]
        self.build_rectangles(rectangles)
        self.circles = []  # type: List[Any]
        self.build_circles(circles)
        self.polylines = []  # type: List[Any]
        self.build_polylines(polylines)
        self.polygons = []  # type: List[Any]
        self.build_polygons(polygons)
        self.identifier = identifier
        self.zoom_control = zoom_control
        self.maptype_control = maptype_control
        self.scale_control = scale_control
        self.streetview_control = streetview_control
        self.rotate_control = rotate_control
        self.scroll_wheel = scroll_wheel
        self.fullscreen_control = fullscreen_control
        self.collapsible = collapsible
        self.mapdisplay = mapdisplay
        self.center_on_user_location = center_on_user_location
        self.report_clickpos = report_clickpos
        self.clickpos_uri = clickpos_uri
        self.report_markerClickpos = report_markerClickpos
        self.markerClickpos_uri = markerClickpos_uri

        self.cluster = cluster
        self.cluster_imagepath = cluster_imagepath
        self.cluster_gridsize = cluster_gridsize

        self.fit_markers_to_bounds = fit_markers_to_bounds
        self.styles = styles
        self.layer = layer
        self.bicycle_layer = bicycle_layer
        self.heatmap_layer = heatmap_layer
        self.heatmap_data = []
        self.build_heatmap(heatmap_data, heatmap_layer)

    def build_rectangles(self, rectangles):
        # type: (Optional[List[Union[List, Tuple, Tuple[Tuple], Dict]]]) -> None
        """Process data to construct rectangles

        This method is built from the assumption that the rectangles parameter
        is a list of:
            lists :a list with 4 elements indicating [north, west, south, east]
            tuples:a tuple with 4 elements indicating (north, west, south,east)
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
            raise AttributeError("rectangles only accept lists as parameters")
        for rect in rectangles:

            # Check the instance of one rectangle in the list. Can be
            # list, tuple or dict
            if isinstance(rect, (list, tuple)):

                # If the rectangle bounds doesn't have size 4 or 2
                # an AttributeError is raised
                if len(rect) not in (2, 4):
                    raise AttributeError("The bound must have length" " 4 or 2")

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
                        raise AttributeError("Wrong size of rectangle bounds")
                    rect_dict = self.build_rectangle_dict(
                        rect[0][0], rect[0][1], rect[1][0], rect[1][1]
                    )
                    self.add_rectangle(**rect_dict)
                else:
                    raise AttributeError("Wrong bounds input size")
            elif isinstance(rect, dict):
                self.add_rectangle(**rect)

    def build_rectangle_dict(
        self,
        north,  # type: float
        west,  # type: float
        south,  # type: float
        east,  # type: float
        stroke_color="#FF0000",  # type: str
        stroke_opacity=0.8,  # type: float
        stroke_weight=2,  # type: int
        fill_color="#FF0000",  # type: str
        fill_opacity=0.3,  # type: float
    ):
        # type: (...) -> Dict
        """Set a dictionary with the javascript class Rectangle parameters

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
            "stroke_color": stroke_color,
            "stroke_opacity": stroke_opacity,
            "stroke_weight": stroke_weight,
            "fill_color": fill_color,
            "fill_opacity": fill_opacity,
            "bounds": {
                "north": north,
                "west": west,
                "south": south,
                "east": east,
            },
        }

        return rectangle

    def add_rectangle(
        self, north=None, west=None, south=None, east=None, **kwargs
    ):
        # type: (Optional[float], Optional[float], Optional[float], Optional[float], **Any) -> None  # noqa E501
        """Adds a rectangle dict to the Map.rectangles attribute

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
            https://developers.google.com/maps/documen
            tation/javascript/reference#LatLngBoundsLiteral

        .. _Rectangles:
            https://developers.google.com/maps/documen
            tation/javascript/shapes#rectangles
        """
        kwargs.setdefault("bounds", {})

        if north:
            kwargs["bounds"]["north"] = north
        if west:
            kwargs["bounds"]["west"] = west
        if south:
            kwargs["bounds"]["south"] = south
        if east:
            kwargs["bounds"]["east"] = east

        if set(("north", "east", "south", "west")) != set(
            kwargs["bounds"].keys()
        ):
            raise AttributeError("rectangle bounds required to rectangles")

        kwargs.setdefault("stroke_color", "#FF0000")
        kwargs.setdefault("stroke_opacity", 0.8)
        kwargs.setdefault("stroke_weight", 2)
        kwargs.setdefault("fill_color", "#FF0000")
        kwargs.setdefault("fill_opacity", 0.3)

        self.rectangles.append(kwargs)

    def build_circles(self, circles):
        # type: (Optional[List[Union[List, Tuple, Dict]]]) -> None
        """Process data to construct rectangles

        This method is built from the assumption that the circles parameter
        is a list of:
            lists : a list with 3 elements indicating
                [center_latitude, center_longitude, radius]
            tuples : a tuple with 3 elements indicating
                (center_latitude, center_longitude, radius)
            dicts: a dictionary with circle attributes

        So, for instance, we have this general scenario as a input parameter:
            [[22.345,45.44, 1000],
             (22.345,45.44,200),
             {
            'stroke_color': stroke_color,
            'stroke_opacity': stroke_opacity,
            'stroke_weight': stroke_weight,
            'fill_color': fill_color,
            'fill_opacity': fill_opacity,
            'center': {'lat': center_latitude,
                       'lng': center_longitude,
                       },
            'radius': radius
            }]
        """
        if not circles:
            return
        if not isinstance(circles, list):
            raise AttributeError("circles accepts only lists")

        for circle in circles:
            if isinstance(circle, dict):
                self.add_circle(**circle)
            elif isinstance(circle, (tuple, list)):
                if len(circle) != 3:
                    raise AttributeError("circle requires center and radius")
                circle_dict = self.build_circle_dict(
                    circle[0], circle[1], circle[2]
                )
                self.add_circle(**circle_dict)

    def build_circle_dict(
        self,
        center_lat,  # type: float
        center_lng,  # type: float
        radius,  # type: float
        stroke_color="#FF0000",  # type: str
        stroke_opacity=0.8,  # type: float
        stroke_weight=2,  # type: int
        fill_color="#FF0000",  # type: str
        fill_opacity=0.3,  # type: float
        clickable=True,  # type: bool
    ):
        # type: (...) -> Dict
        """Set a dictionary with the javascript class Circle parameters

        This function sets a default drawing configuration if the user just
        pass the rectangle bounds, but also allows to set each parameter
        individually if the user wish so.

        Args:
            center_lat (float): The circle center latitude
            center_lng (float): The circle center longitude
            radius  (float): The circle radius, in meters
            stroke_color (str): Sets the color of the rectangle border using
                hexadecimal color notation
            stroke_opacity (float): Sets the opacity of the rectangle border
                in percentage. If stroke_opacity = 0, the border is transparent
            stroke_weight (int): Sets the stroke girth in pixels.
            fill_color (str): Sets the color of the circle fill using
                hexadecimal color notation
            fill_opacity (float): Sets the opacity of the circle fill
        """

        circle = {
            "stroke_color": stroke_color,
            "stroke_opacity": stroke_opacity,
            "stroke_weight": stroke_weight,
            "fill_color": fill_color,
            "fill_opacity": fill_opacity,
            "center": {"lat": center_lat, "lng": center_lng},
            "radius": radius,
            "clickable": clickable,
        }

        return circle

    def add_circle(
        self, center_lat=None, center_lng=None, radius=None, **kwargs
    ):
        # type: (Optional[float], Optional[float], Optional[float], **Any) -> None
        """Adds a circle dict to the Map.circles attribute

        The circle in a sphere is called "spherical cap" and is defined in the
        Google Maps API by at least the center coordinates and its radius, in
        meters. A circle has color and opacity both for the border line and the
        inside area.

        It accepts a circle dict representation as well.

        Args:
            center_lat (float): The circle center latitude
            center_lng (float): The circle center longitude
            radius  (float): The circle radius, in meters

        .. _Circle:
            https://developers.google.com/maps/documen
            tation/javascript/reference#Circle
        """

        kwargs.setdefault("center", {})
        if center_lat:
            kwargs["center"]["lat"] = center_lat
        if center_lng:
            kwargs["center"]["lng"] = center_lng
        if radius:
            kwargs["radius"] = radius

        if set(("lat", "lng")) != set(kwargs["center"].keys()):
            raise AttributeError("circle center coordinates required")
        if "radius" not in kwargs:
            raise AttributeError("circle radius definition required")

        kwargs.setdefault("stroke_color", "#FF0000")
        kwargs.setdefault("stroke_opacity", 0.8)
        kwargs.setdefault("stroke_weight", 2)
        kwargs.setdefault("fill_color", "#FF0000")
        kwargs.setdefault("fill_opacity", 0.3)

        self.circles.append(kwargs)

    def build_polylines(self, polylines):
        # type: (Optional[List[Union[List, Tuple, Dict]]]) -> None
        """Process data to construct polylines

        This method is built from the assumption that the polylines parameter
        is a list of:
            list of lists or tuples : a list of path points, each one
            indicating the point coordinates --
            [lat,lng], [lat, lng], (lat, lng), ...

            tuple of lists or tuples : a tuple of path points, each one
                indicating the point coordinates -- (lat,lng), [lat, lng],
                (lat, lng), ...

            dicts: a dictionary with polylines attributes

        So, for instance, we have this general scenario as a input parameter:


            polyline = {
                'stroke_color': '#0AB0DE',
                'stroke_opacity': 1.0,
                'stroke_weight': 3,
                'path': [{'lat': 33.678, 'lng': -116.243},
                        {'lat': 33.679, 'lng': -116.244},
                        {'lat': 33.680, 'lng': -116.250},
                        {'lat': 33.681, 'lng': -116.239},
                        {'lat': 33.678, 'lng': -116.243}]
            }

            path1 = [(33.665, -116.235), (33.666, -116.256),
                    (33.667, -116.250), (33.668, -116.229)]

            path2 = ((33.659, -116.243), (33.660, -116.244),
                    (33.649, -116.250), (33.644, -116.239))

            path3 = ([33.688, -116.243], [33.680, -116.244],
                    [33.682, -116.250], [33.690, -116.239])

            path4 = [[33.690, -116.243], [33.691, -116.244],
                    [33.692, -116.250], [33.693, -116.239]]

            polylines = [polyline, path1, path2, path3, path4]

        """
        if not polylines:
            return
        if not isinstance(polylines, (list, tuple)):
            raise AttributeError("A list or tuple of polylines is required")

        for points in polylines:
            if isinstance(points, dict):
                self.add_polyline(**points)
            elif isinstance(points, (tuple, list)):
                path = []
                for coords in points:
                    if len(coords) != 2:
                        raise AttributeError("A point needs two coordinates")
                    path.append({"lat": coords[0], "lng": coords[1]})
                polyline_dict = self.build_polyline_dict(path)
                self.add_polyline(**polyline_dict)

    def build_polyline_dict(
        self, path, stroke_color="#FF0000", stroke_opacity=0.8, stroke_weight=2
    ):
        # type: (List[Dict], str, float, int) -> Dict
        """Set a dictionary with the javascript class Polyline parameters

        This function sets a default drawing configuration if the user just
        pass the polyline path, but also allows to set each parameter
        individually if the user wish so.

        Args:
            path (list): A list of latitude and longitude point for the
            polyline stroke_color (str): Sets the color of the rectangle
            border using hexadecimal color notation
            stroke_opacity (float): Sets the opacity of the rectangle border
                in percentage. If stroke_opacity = 0, the border is transparent
            stroke_weight (int): Sets the stroke girth in pixels.
        """

        if not isinstance(path, list):
            raise AttributeError(
                "To build a map path a list of dictionaries"
                " of latitude and logitudes is required"
            )

        polyline = {
            "path": path,
            "stroke_color": stroke_color,
            "stroke_opacity": stroke_opacity,
            "stroke_weight": stroke_weight,
        }

        return polyline

    def add_polyline(self, path=None, **kwargs):
        # type: (Optional[List[Dict]], **Any) -> None
        """Adds a polyline dict to the Map.polylines attribute

        The Google Maps API describes a polyline as a "linear overlay of
        connected line segments on the map". The linear paths are defined
        by a list of Latitude and Longitude coordinate pairs, like so:

            { 'lat': y, 'lng': x }

        with each one being a point of the polyline path.

        It accepts a polyline dict representation as well.

        Args:
            path (list(dict)): The set of points of the path

        .. _Polyline:
            https://developers.google.com/maps/documen
            tation/javascript/reference#Polyline
        """

        if path:
            if not isinstance(path, list):
                raise AttributeError(
                    "The path is a list of dictionary of"
                    "latitude and longitudes por path points"
                )
            for i, point in enumerate(path):
                if not isinstance(point, dict):
                    if isinstance(point, (list, tuple)) and len(point) == 2:
                        path[i] = {"lat": point[0], "lng": point[1]}
                    else:
                        raise AttributeError(
                            "All points in the path must be dicts"
                            " of latitudes and longitudes, list or tuple"
                        )
            kwargs["path"] = path

        kwargs.setdefault("stroke_color", "#FF0000")
        kwargs.setdefault("stroke_opacity", 0.8)
        kwargs.setdefault("stroke_weight", 2)

        self.polylines.append(kwargs)

    def build_polygons(self, polygons):
        # type: (Optional[List[Union[List, Tuple, Dict]]]) -> None
        """Process data to construct polygons

        This method is built from the assumption that the polygons parameter
        is a list of:
            list of lists or tuples : a list of path points, each one
            indicating the point coordinates --
            [lat,lng], [lat, lng], (lat, lng), ...

            tuple of lists or tuples : a tuple of path points, each one
                indicating the point coordinates -- (lat,lng), [lat, lng],
                (lat, lng), ...

            dicts: a dictionary with polylines attributes

        So, for instance, we have this general scenario as a input parameter:


            polygon = {
                'stroke_color': '#0AB0DE',
                'stroke_opacity': 1.0,
                'stroke_weight': 3,
                'fill_color': '#FFABCD',
                'fill_opacity': 0.5,
                'path': [{'lat': 33.678, 'lng': -116.243},
                        {'lat': 33.679, 'lng': -116.244},
                        {'lat': 33.680, 'lng': -116.250},
                        {'lat': 33.681, 'lng': -116.239},
                        {'lat': 33.678, 'lng': -116.243}]
            }

            path1 = [(33.665, -116.235), (33.666, -116.256),
                    (33.667, -116.250), (33.668, -116.229)]

            path2 = ((33.659, -116.243), (33.660, -116.244),
                    (33.649, -116.250), (33.644, -116.239))

            path3 = ([33.688, -116.243], [33.680, -116.244],
                    [33.682, -116.250], [33.690, -116.239])

            path4 = [[33.690, -116.243], [33.691, -116.244],
                    [33.692, -116.250], [33.693, -116.239]]

            polygons = [polygon, path1, path2, path3, path4]

        """
        if not polygons:
            return
        if not isinstance(polygons, (list, tuple)):
            raise AttributeError("A list or tuple of polylines is required")

        for points in polygons:
            if isinstance(points, dict):
                self.add_polygon(**points)
            elif isinstance(points, (tuple, list)):
                path = []
                for coords in points:
                    if len(coords) != 2:
                        raise AttributeError("A point needs two coordinates")
                    path.append({"lat": coords[0], "lng": coords[1]})
                polygon_dict = self.build_polygon_dict(path)
                self.add_polygon(**polygon_dict)

    def build_polygon_dict(
        self,
        path,  # type: List[Dict]
        stroke_color="#FF0000",  # type: str
        stroke_opacity=0.8,  # type: float
        stroke_weight=2,  # type: int
        fill_color="#FF0000",  # type: str
        fill_opacity=0.3,  # type: float
    ):
        # type: (...) -> Dict
        """Set a dictionary with the javascript class Polygon parameters

        This function sets a default drawing configuration if the user just
        pass the polygon path, but also allows to set each parameter
        individually if the user wish so.

        Args:
            path (list): A list of latitude and longitude point for the polygon
            stroke_color (str): Sets the color of the polygon border using
                hexadecimal color notation
            stroke_opacity (float): Sets the opacity of the polygon border
                in percentage. If stroke_opacity = 0, the border is transparent
            stroke_weight (int): Sets the stroke girth in pixels.

            fill_color (str): Sets the color of the polygon fill using
                hexadecimal color notation
            fill_opacity (float): Sets the opacity of the polygon fill
        """

        if not isinstance(path, list):
            raise AttributeError(
                "To build a map path a list of dictionaries"
                " of latitude and logitudes is required"
            )

        polygon = {
            "path": path,
            "stroke_color": stroke_color,
            "stroke_opacity": stroke_opacity,
            "stroke_weight": stroke_weight,
            "fill_color": fill_color,
            "fill_opacity": fill_opacity,
        }

        return polygon

    def add_polygon(self, path=None, **kwargs):
        # type: (Optional[List[Dict]], **Any) -> None
        """Adds a polygon dict to the Map.polygons attribute

        The Google Maps API describes a polyline as a "linear overlay of
        connected line segments on the map" and "form a closed loop and define
        a filled region.". The linear paths are defined by a list of Latitude
        and Longitude coordinate pairs, like so:

            { 'lat': y, 'lng': x }

        with each one being a point of the polyline path.

        It accepts a polygon dict representation as well.

        Args:
            path (list(dict)): The set of points of the path

        .. _Polygon:
            https://developers.google.com/maps/documen
            tation/javascript/reference#Polygon
        """

        if path:
            if not isinstance(path, list):
                raise AttributeError(
                    "The path is a list of dictionary of"
                    "latitude and longitudes por path points"
                )
            for i, point in enumerate(path):
                if not isinstance(point, dict):
                    if isinstance(point, (list, tuple)) and len(point) == 2:
                        path[i] = {"lat": point[0], "lng": point[1]}
                    else:
                        raise AttributeError(
                            "All points in the path must be dicts"
                            " of latitudes and longitudes, list or tuple"
                        )
            kwargs["path"] = path

        kwargs.setdefault("stroke_color", "#FF0000")
        kwargs.setdefault("stroke_opacity", 0.8)
        kwargs.setdefault("stroke_weight", 2)
        kwargs.setdefault("fill_color", "#FF0000")
        kwargs.setdefault("fill_opacity", 0.3)

        self.polygons.append(kwargs)

    def build_heatmap(self, heatmap_data, heatmap_layer):
        # type: (list, bool) -> dict
        if not heatmap_layer:
            return
        if heatmap_layer and not heatmap_data:
            raise AttributeError("heatmap_later requires 'heatmap_data'")
        if not isinstance(heatmap_data, (list)):
            raise AttributeError(
                "heatmap_data only accepts a list of dicts with keys "
                "'lat' 'lng' and their corresponding values"
            )
        for hm in heatmap_data:
            if isinstance(hm, dict):
                self.add_heatmap(**hm)
            else:
                raise AttributeError(
                    "elements of list 'heatmap_data' must be a dict of keys "
                    "'lat' and 'lng' with their corresponding values"
                )

    def add_heatmap(self, lat=None, lng=None, **kwargs):
        # type: (Optional[float], Optional[float], **Any) -> None
        if lat is not None:
            kwargs["lat"] = lat
        if lng is not None:
            kwargs["lng"] = lng
        if "lat" not in kwargs or "lng" not in kwargs:
            raise AttributeError("heatmap_data requires 'lat' and 'lng' values")
        if len(kwargs) > 2:
            raise AttributeError(
                "heatmap_data can only contain 'lat' and 'lng' values"
            )

        self.heatmap_data.append(kwargs)

    def render(self, *args, **kwargs):
        # type: (*Any, **Any) -> Text
        return render_template(*args, **kwargs)

    def as_json(self):
        # type: () -> Dict
        json_dict = {
            "identifier": self.identifier,
            "center": self.center,
            "zoom": self.zoom,
            "maptype": self.maptype,
            "markers": self.markers,
            "varname": self.varname,
            "style": self.style,
            "cls": self.cls,
            "rectangles": self.rectangles,
            "circles": self.circles,
            "polylines": self.polylines,
            "polygons": self.polygons,
            "zoom_control": self.zoom_control,
            "maptype_control": self.maptype_control,
            "scale_control": self.scale_control,
            "streetview_control": self.streetview_control,
            "rotate_control": self.rotate_control,
            "fullscreen_control": self.fullscreen_control,
            "cluster": self.cluster,
            "cluster_imagepath": self.cluster_imagepath,
            "cluster_gridsize": self.cluster_gridsize,
            "collapsible": self.collapsible,
            "center_on_user_location": self.center_on_user_location,
            "js": dumps(self.js),
            "html": dumps(self.html),
            "fit_markers_to_bounds": self.fit_markers_to_bounds,
        }

        return json_dict

    @property
    def js(self):
        # type: () -> Markup
        return Markup(
            self.render("googlemaps/gmapjs.html", gmap=self, DEFAULT_PIN="")
        )

    @property
    def html(self):
        # type: () -> Markup
        return Markup(self.render("googlemaps/gmap.html", gmap=self))


def googlemap_obj(*args, **kwargs):
    # type: (*Any, **Any) -> Map
    map = Map(*args, **kwargs)
    return map


def googlemap(*args, **kwargs):
    # type: (*Any, **Any) -> Markup
    map = googlemap_obj(*args, **kwargs)
    return Markup("".join((map.js, map.html)))


def googlemap_html(*args, **kwargs):
    # type: (*Any, **Any) -> Markup
    return googlemap_obj(*args, **kwargs).html


def googlemap_js(*args, **kwargs):
    # type: (*Any, **Any) -> Markup
    return googlemap_obj(*args, **kwargs).js


def set_googlemaps_loaded():
    # type: () -> str
    g.googlemaps_loaded = True
    return ""


def get_address(API_KEY, lat, lon):
    # type: (str, float, float) -> dict
    add_dict = dict()
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?latlng="
        + ",".join(map(str, [lat, lon]))
        + "&key="
        + API_KEY
    ).json()
    add_dict["zip"] = response["results"][0]["address_components"][-1][
        "long_name"
    ]
    add_dict["country"] = response["results"][0]["address_components"][-2][
        "long_name"
    ]
    add_dict["state"] = response["results"][0]["address_components"][-3][
        "long_name"
    ]
    add_dict["city"] = response["results"][0]["address_components"][-4][
        "long_name"
    ]
    add_dict["locality"] = response["results"][0]["address_components"][-5][
        "long_name"
    ]
    add_dict["road"] = response["results"][0]["address_components"][-6][
        "long_name"
    ]
    add_dict["formatted_address"] = response["results"][0]["formatted_address"]
    return add_dict


def get_coordinates(API_KEY, address_text):
    # type: (str, str) -> Dict
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + address_text
        + "&key="
        + API_KEY
    ).json()
    return response["results"][0]["geometry"]["location"]


def is_googlemaps_loaded():
    # type: () -> bool
    return getattr(g, "googlemaps_loaded", False)


class GoogleMaps(object):
    def __init__(self, app=None, **kwargs):
        # type: (Optional[Any], **str) -> None
        self.key = kwargs.get("key")
        if app:
            self.init_app(app)

    def init_app(self, app):
        # type: (Any) -> None
        if self.key:
            app.config["GOOGLEMAPS_KEY"] = self.key
        self.register_blueprint(app)
        app.add_template_filter(googlemap_html)
        app.add_template_filter(googlemap_js)
        app.add_template_global(googlemap_obj)
        app.add_template_filter(googlemap)
        app.add_template_global(googlemap)
        app.add_template_global(
            app.config.get("GOOGLEMAPS_KEY"), name="GOOGLEMAPS_KEY"
        )
        app.add_template_global(set_googlemaps_loaded)
        app.add_template_global(is_googlemaps_loaded)

    def register_blueprint(self, app):
        module = Blueprint("googlemaps", __name__, template_folder="templates")
        app.register_blueprint(module)
        return module
