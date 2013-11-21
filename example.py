# coding: utf-8

from flask import Flask, render_template
from flaskext.googlemaps import GoogleMaps
from flaskext.googlemaps import Map

app = Flask(__name__, template_folder=".")
GoogleMaps(app)

@app.route("/")
def mapview():
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    return render_template('example.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)
