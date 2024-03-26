from flask import Flask, render_template

from flask_googlemaps import GoogleMaps, Map
from flask_googlemaps.pin import Pin

app = Flask(__name__)
GoogleMaps(app)

red = Pin(border_color="", glyph_color="",
          background="",
          glyph="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png")
blue = Pin(border_color="blue", glyph_color="",
           background="black",
           glyph="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png")


@app.route("/")
def map_created_in_view():
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            red: [(37.4419, -122.1419),],
            blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)


if __name__ == "__main__":
    app.run(port=5050, debug=True)
