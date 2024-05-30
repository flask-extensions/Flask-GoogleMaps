from flask import Flask, render_template

from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
GoogleMaps(app)


@app.route("/")
def map_created_in_view():
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
            {
                "latitude": 37.4419,
                "longitude": -122.1419,
                "infobox": "<b>Hello world!</b>",
                "content": {
                    "border_color": "rgb(218, 247, 166)",
                    "glyph_color": "white",
                    "background": "#F88379",
                    "scale": 1.0,
                },
            },
            {
                "latitude": 37.4519,
                "longitude": -122.1519,
                "content": {
                    "icon_url": "https://img.shields.io/badge/PayPal-Donante-red.svg"
                },
            },
            (37.4500, -122.1350),
            (37.4800, -122.1550),
        ],
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)


if __name__ == "__main__":
    app.run(port=5050, debug=True)
