from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map, icons
from dynaconf import FlaskDynaconf
#enter the api key below
api = ''
app = Flask(__name__)
GoogleMaps(app, key = api)
FlaskDynaconf(app)

import json


@app.route("/")
def map_created_in_view():

    with open('dark_mode.json') as d:
        dark_data = json.load(d)

    wmap = Map(
        identifier="wmap",
        varname="wmap",
        lat=41.881832,
        lng=-87.623177,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;color:#242f3e;",
        bicycle_layer = True,
    )


    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=1.351616,
        lng=103.808053,
        markers={
            icons.alpha.A: [(1.351616, 103.808053), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;color:#242f3e;",
        layer = "https://geo.data.gov.sg/dengue-cluster/2020/09/02/kml/dengue-cluster.kml"
    )

    dmap = Map(
        identifier="dmap",
        varname="dmap",
        lat=1.351616,
        lng=103.808053,
        markers={
            icons.dots.green: [(37.4419, -122.1419), (37.4500, -122.1350)],
            icons.dots.blue: [(37.4300, -122.1400, "Hello World")],
        },
        style="height:400px;width:600px;margin:0;color:#242f3e;",
        styles=dark_data,

    )

  #  print(get_address(api, 22.4761596, 88.4149326))
    return render_template("example_2.html", dmap=dmap ,gmap = gmap, wmap = wmap,key = api)





if __name__ == "__main__":
    app.run(port=5050, debug=True)
