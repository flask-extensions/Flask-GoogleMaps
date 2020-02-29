from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map, icons
from dynaconf import FlaskDynaconf

app = Flask(__name__)
GoogleMaps(app)
FlaskDynaconf(app)


@app.route("/")
def map_created_in_view():

    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=37.4419,
        lng=-122.1419,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;",
    )

    return render_template("simple.html", gmap=gmap)


if __name__ == "__main__":
    app.run(port=5050)
