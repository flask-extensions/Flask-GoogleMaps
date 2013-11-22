# Flask Google Maps

Easy to use Google Maps in your Flask application

### requires
- Jinja
- Flask
- A google api key (optional I guess)


### Installation

```pip install flask-googlemaps```

or

```bash
git clone https://github.com/rochacbruno/Flask-GoogleMaps
cd Flask-GoogleMaps
python setup.py install
```

### Usage

You can create the map in the view and then send to the template context or you can use the template functions and filters directly


#### View

```python
from flask import Flask, render_template
from flaskext.googlemaps import GoogleMaps
from flaskext.googlemaps import Map

app = Flask(__name__, template_folder=".")
GoogleMaps(app)

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    return render_template('example.html', mymap=mymap)

if __name__ == "__main__":
    app.run(debug=True)
```

#### Template

```html
<!DOCTYPE html>
    <html>
    <head>
            {{"decoupled-map"|googlemap_js(37.4419, -122.1419, markers=[(37.4419, -122.1419)])}}
            {{mymap.js}}
    </head>
    <body>
        <h1>Flask Google Maps Example</h1>

        <h2> Template function centered, no marker </h2>
        {{googlemap("simple-map", 37.4419, -122.1419)}}

        <h2> Template filter decoupled with single marker </h2>
        {{"decoupled-map"|googlemap_html(37.4419, -122.1419)}}


        <h2> Template function with multiple markers </h2>
        {% with map=googlemap_obj("another-map", 37.4419, -122.1419, markers=[(37.4419, -122.1419), (37.4300, -122.1400)]) %}
            {{map.html}}
            {{map.js}}
        {% endwith %}

        <h2> Generated in view</h2>
        {{mymap.html}}
    </body>
</html>

```

### Screenshot

<img src="screenshot.png" />


### TODO:

Implement other methods from the api, add layers etc...
