from flask import Flask, render_template

from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)
GoogleMaps(app)

pin_content = {
    "border_color": "",
    "glyph_colors": "",
    "background": "",
    "glyph": "",
    "scale": 2.0,
}
image_content = {
    "icon_urls": "https://img.shields.io/badge/PayPal-Donante-red.svg"
}


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
                "label": "1",
                "content": pin_content,
            },
            {
                "latitude": 37.4519,
                "longitude": -122.1519,
                "content": image_content,
            },
        ],
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)


if __name__ == "__main__":
    app.run(port=5050, debug=True)
