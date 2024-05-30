from flask import Flask, jsonify, render_template

from flask_googlemaps import Map, GoogleMaps

app = Flask(__name__, template_folder="templates")
GoogleMaps(app)


@app.route("/")
def tst_jsonify():
    mymap = Map(
        identifier="view-side",  # for DOM element
        varname="mymap",  # for JS object name
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
    )
    return jsonify(mymap.as_json())


@app.route("/simplemap")
def simple_view_one():
    mymap = Map(
        identifier="view-side",  # for DOM element
        varname="mymap",  # for JS object name
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)],
    )
    return jsonify(mymap.as_json())


@app.route("/simplemap2")
def simple_view_two():
    sndmap = Map(
        identifier="sndmap",
        varname="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419), (37.4500, -122.1350)],
    )
    return jsonify(sndmap.as_json())


@app.route("/simplemap3")
def simple_view_three():
    trdmap = Map(
        identifier="trdmap",
        varname="trdmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                "content": {"background": "green"},
                "latitude": 37.4419,
                "longitude": -122.1419,
                "infobox": "Hello I am <b style='color:green;'>GREEN</b>!",
            },
            {
                "content": {"background": "blue"},
                "latitude": 37.4300,
                "longitude": -122.1400,
                "infobox": "Hello I am <b style='color:blue;'>BLUE</b>!",
            },
            {
                "content": {"background": "yellow"},
                "latitude": 37.4500,
                "longitude": -122.1350,
                "infobox": (
                    "Hello I am <b style='color:#ffcc00;'>YELLOW</b>!"
                    "<h2>It is HTML title</h2>"
                    "<img src='//placehold.it/50'>"
                    "<br>Images allowed!"
                ),
            },
        ],
    )

    return jsonify(trdmap.as_json())


@app.route("/clustered")
def cluster_view():
    clustermap = Map(
        identifier="clustermap",
        varname="clustermap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {"latitude": 37.4500, "longitude": -122.1350},
            {"latitude": 37.4400, "longitude": -122.1350},
            {"latitude": 37.4300, "longitude": -122.1350},
            {"latitude": 36.4200, "longitude": -122.1350},
            {"latitude": 36.4100, "longitude": -121.1350},
        ],
        zoom=12,
        cluster=True,
    )

    return jsonify(clustermap.as_json())


@app.route("/rectangle")
def rectangle_view():
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

    return jsonify(rectmap.as_json())


@app.route("/circle")
def circle_view():
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
        circles=[
            circle,
            [33.685, -116.251, 1000],
            (33.685, -116.251, 1500),
        ],
    )

    return jsonify(circlemap.as_json())


@app.route("/polyline")
def polyline_view():
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

    return jsonify(plinemap.as_json())


@app.route("/polygon")
def polygon_view():
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

    pgonmap = Map(
        identifier="pgonmap",
        varname="pgonmap",
        lat=33.678,
        lng=-116.243,
        polygons=[polygon, path1, path2, path3, path4],
    )

    return jsonify(pgonmap.as_json())


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
