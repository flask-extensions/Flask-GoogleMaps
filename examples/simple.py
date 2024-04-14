from flask import Flask, render_template

from flask_googlemaps import GoogleMaps, Map
from flask_googlemaps.image import Image
from flask_googlemaps.pin import Pin

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
                "label": "1",
                # 'content': Pin(border_color="blue", background="blue")
                "content": Pin(border_color="blue", background="blue"),
            },
            {
                "latitude": 37.4519,
                "longitude": -122.1519,
                "content": Pin(border_color="blue", background="blue"),
            },
        ],
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)


if __name__ == "__main__":
    app.run(port=5050, debug=True)
