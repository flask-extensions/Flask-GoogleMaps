# coding: utf-8

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from dynaconf import FlaskDynaconf

app = Flask(__name__, template_folder="templates")
FlaskDynaconf(app)  # will read GOOGLEMAPS_KEY from .secrets.toml


# you can set key as config
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyDP0GX-Wsui9TSDxtFNj2XuKrh7JBTPCnU"

# you can also pass key here
GoogleMaps(
    app,
    # key="AIzaSyDP0GX-Wsui9TSDxtFNj2XuKrh7JBTPCnU"
)

# NOTE: this example is using a form to get the apikey


@app.route("/")
def mapview():
    mymap = Map(
        identifier="view-side",  # for DOM element
        varname="mymap",  # for JS object name
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
    )
    sndmap = Map(
        identifier="sndmap",
        varname="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
    )

    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                "icon": icons.alpha.B,
                "lat": 37.4419,
                "lng": -122.1419,
                "infobox": "Hello I am <b style='color:green;'>GREEN</b>!",
            },
            {
                "icon": icons.dots.blue,
                "lat": 37.4300,
                "lng": -122.1400,
                "infobox": "Hello I am <b style='color:blue;'>BLUE</b>!",
            },
            {
                "icon": "//maps.google.com/mapfiles/ms/icons/yellow-dot.png",
                "lat": 37.4500,
                "lng": -122.1350,
                "infobox": (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                ),
            },
        ],
    )

    clustermap = Map(
        identifier="clustermap",
        varname="clustermap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {"lat": 37.4500, "lng": -122.1350},
            {"lat": 37.4400, "lng": -122.1350},
            {"lat": 37.4300, "lng": -122.1350},
            {"lat": 36.4200, "lng": -122.1350},
            {"lat": 36.4100, "lng": -121.1350},
        ],
        zoom=12,
        cluster=True,
    )

    movingmap = Map(
        identifier="movingmap",
        varname="movingmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[{"lat": 37.4500, "lng": -122.1350}],
        zoom=12,
    )

    movingmarkers = [
        {"lat": 37.4400, "lng": -122.1350},
        {"lat": 37.4430, "lng": -122.1350},
        {"lat": 37.4450, "lng": -122.1350},
        {"lat": 37.4490, "lng": -122.1350},
    ]

    rectangle = {
        "stroke_color": "#0000FF",
        "stroke_opacity": 0.8,
        "stroke_weight": 5,
        "fill_color": "#FFFFFF",
        "fill_opacity": 0.1,
        "bounds": {
            "north": 33.685,
            "south": 33.671,
            "east": -116.234,
            "west": -116.251,
        },
    }

    rectmap = Map(
        identifier="rectmap",
        varname="rectmap",
        lat=33.678,
        lng=-116.243,
        rectangles=[
            rectangle,
            [33.678, -116.243, 33.671, -116.234],
            (33.685, -116.251, 33.678, -116.243),
            [(33.679, -116.254), (33.678, -116.243)],
            ([33.689, -116.260], [33.685, -116.250]),
        ],
    )

    circle = {
        "stroke_color": "#FF00FF",
        "stroke_opacity": 1.0,
        "stroke_weight": 7,
        "fill_color": "#FFFFFF",
        "fill_opacity": 0.8,
        "center": {"lat": 33.685, "lng": -116.251},
        "radius": 2000,
    }

    circlemap = Map(
        identifier="circlemap",
        varname="circlemap",
        lat=33.678,
        lng=-116.243,
        circles=[circle, [33.685, -116.251, 1000], (33.685, -116.251, 1500),],
    )

    polyline = {
        "stroke_color": "#0AB0DE",
        "stroke_opacity": 1.0,
        "stroke_weight": 3,
        "path": [
            {"lat": 33.678, "lng": -116.243},
            {"lat": 33.679, "lng": -116.244},
            {"lat": 33.680, "lng": -116.250},
            {"lat": 33.681, "lng": -116.239},
            {"lat": 33.678, "lng": -116.243},
        ],
    }

    path1 = [
        (33.665, -116.235),
        (33.666, -116.256),
        (33.667, -116.250),
        (33.668, -116.229),
    ]

    path2 = (
        (33.659, -116.243),
        (33.660, -116.244),
        (33.649, -116.250),
        (33.644, -116.239),
    )

    path3 = (
        [33.688, -116.243],
        [33.680, -116.244],
        [33.682, -116.250],
        [33.690, -116.239],
    )

    path4 = [
        [33.690, -116.243],
        [33.691, -116.244],
        [33.692, -116.250],
        [33.693, -116.239],
    ]

    plinemap = Map(
        identifier="plinemap",
        varname="plinemap",
        lat=33.678,
        lng=-116.243,
        polylines=[polyline, path1, path2, path3, path4],
    )

    polygon = {
        "stroke_color": "#0AB0DE",
        "stroke_opacity": 1.0,
        "stroke_weight": 3,
        "fill_color": "#ABC321",
        "fill_opacity": 0.5,
        "path": [
            {"lat": 33.678, "lng": -116.243},
            {"lat": 33.679, "lng": -116.244},
            {"lat": 33.680, "lng": -116.250},
            {"lat": 33.681, "lng": -116.239},
            {"lat": 33.678, "lng": -116.243},
        ],
    }

    pgonmap = Map(
        identifier="pgonmap",
        varname="pgonmap",
        lat=33.678,
        lng=-116.243,
        polygons=[polygon, path1, path2, path3, path4],
    )

    collapsible = Map(
        identifier="collapsible",
        varname="collapsible",
        lat=60.000025,
        lng=30.288809,
        zoom=13,
        collapsible=True,
    )

    infoboxmap = Map(
        identifier="infoboxmap",
        zoom=12,
        lat=59.939012,
        lng=30.315707,
        markers=[{"lat": 59.939, "lng": 30.315, "infobox": "This is a marker"}],
        circles=[
            {
                "stroke_color": "#FF00FF",
                "stroke_opacity": 1.0,
                "stroke_weight": 7,
                "fill_color": "#FF00FF",
                "fill_opacity": 0.2,
                "center": {"lat": 59.939, "lng": 30.3},
                "radius": 200,
                "infobox": "This is a circle",
            }
        ],
        rectangles=[
            {
                "stroke_color": "#0000FF",
                "stroke_opacity": 0.8,
                "stroke_weight": 5,
                "fill_color": "#FFFFFF",
                "fill_opacity": 0.1,
                "bounds": {
                    "north": 59.935,
                    "south": 59.93,
                    "east": 30.325,
                    "west": 30.3,
                },
                "infobox": "This is a rectangle",
            }
        ],
        polygons=[
            {
                "stroke_color": "#0AB0DE",
                "stroke_opacity": 1.0,
                "stroke_weight": 3,
                "path": [
                    [59.94, 30.318],
                    [59.946, 30.325],
                    [59.946, 30.34],
                    [59.941, 30.35],
                    [59.938, 30.33],
                ],
                "infobox": "This is a polygon",
            }
        ],
        polylines=[
            {
                "stroke_color": "#0AB0DE",
                "stroke_opacity": 1.0,
                "stroke_weight": 10,
                "path": [
                    (59.941, 30.285),
                    (59.951, 30.31),
                    (59.95, 30.36),
                    (59.938, 30.358),
                ],
                "infobox": "This is a polyline",
            }
        ],
    )

    clickmap = Map(
        identifier="clickmap",
        varname="clickmap",
        lat=37.4419,
        lng=-122.1419,
        report_clickpos=True,
        clickpos_uri="/clickpost/",
    )

    return render_template(
        "example.html",
        mymap=mymap,
        sndmap=sndmap,
        trdmap=trdmap,
        rectmap=rectmap,
        circlemap=circlemap,
        plinemap=plinemap,
        pgonmap=pgonmap,
        clustermap=clustermap,
        movingmap=movingmap,
        movingmarkers=movingmarkers,
        collapsible=collapsible,
        infoboxmap=infoboxmap,
        clickmap=clickmap,
        GOOGLEMAPS_KEY=request.args.get("apikey"),
    )


@app.route("/fullmap")
def fullmap():
    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:200;"
        ),
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                "icon": "//maps.google.com/mapfiles/ms/icons/green-dot.png",
                "lat": 37.4419,
                "lng": -122.1419,
                "infobox": "Hello I am <b style='color:green;'>GREEN</b>!",
            },
            {
                "icon": "//maps.google.com/mapfiles/ms/icons/blue-dot.png",
                "lat": 37.4300,
                "lng": -122.1400,
                "infobox": "Hello I am <b style='color:blue;'>BLUE</b>!",
            },
            {
                "icon": icons.dots.yellow,
                "title": "Click Here",
                "lat": 37.4500,
                "lng": -122.1350,
                "infobox": (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                ),
            },
        ],
        # maptype = "TERRAIN",
        # zoom="5"
    )
    return render_template(
        "example_fullmap.html",
        fullmap=fullmap,
        GOOGLEMAPS_KEY=request.args.get("apikey"),
    )


@app.route("/clickpost/", methods=["POST"])
def clickpost():
    # Now lat and lon can be accessed as:
    lat = request.form["lat"]
    lng = request.form["lng"]
    print(lat)
    print(lng)
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
