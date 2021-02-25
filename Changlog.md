Changelog
=========


0.4.1 (2020-02-21)
------------
- Added support for marker labels [jackcarter]
- Added KML layer: User can add hyperlink of KML file to apply on the map [bhuveshsharma09]
- Added Bicycle lane layer: User can turn on/off bicycle lane using the new attribute [bhuveshsharma09]
- Added Custom Styles: User can add custom style JSON file for the map style [bhuveshsharma09]
- Validated the lat lng coordinates when initialize the Map object [JacobGeoGeek]
- Added map id support [markmelnic]
- Updated some dependencies [Vicente Marçal]


0.4.0 (2020-02-21)
------------
- Added Trafficlayer support [wimpruijsers]
- Fixed wrong map object when calling setCenter() which make function
  working properly. [SmallSea]
- Create a Changelog.md file [Vicente Marçal]  
- Updated README. [Vicente Marçal]


0.3.0 (2020-02-21)
------------------
- Merge pull request #94 from flask-extensions/poetry. [Vicente Marçal]

  Moving to Poetry
- Add poetry files. [Bruno Rocha]
- Removed old setup files. [Bruno Rocha]
- Add Issues Templates. [Vicente Marçal]
- Fix missing , in alpha options. [Josh Mint VM]
- Fix typos in paddle options. [Josh Mint VM]
- Add paddle icons from http://kml4earth.appspot.com/icons.html#paddle.
  [Josh Mint VM]
- Update icon base_url values for shapes and pushpin, from
  http://kml4earth.appspot.com/icons.html#mapfiles. [Josh Mint VM]
- Merge pull request #79 from kjellreell/minor-doc-fix. [Bruno Rocha]

  updated README.md description on how to run the example
- Updated README.md description on how to run the example. [martin
  kjellin]
- Merge branch 'kjellreell-issue60-latlon-from-click' [Bruno Rocha]
- Add a form to get APIkey. [Bruno Rocha]
- Issue #60: add support for getting clicked latitude and longitude to
  flask. [martin kjellin]
- Merge pull request #75 from johnclary/update-docs. [Bruno Rocha]

  Update Docs with center_on_user_location
- Update Docs with center_on_user_location. [John Clary]

  The variable name center_on_user_location wasn't properly formatted in the docs. Fixed. You're very welcome!
- Merge pull request #70 from david81brs/iconsets. [Bruno Rocha]

  New sets #shapes & #pushpin
- New sets #shapes & #pushpin. [David Silva]
- Pinned Flask version for compatibility reasons try to resolve #69.
  [Bruno Rocha]
- Merge pull request #64 from n0d/master. [Bruno Rocha]

  Add option to center map based on user's location (Issue #52).
- Add option to center map based on user's location (Issue #52).
  [Beandob]
- Merge pull request #61 from edawine/fix-license. [Bruno Rocha]

  Create LICENSE
- Create LICENSE. [edawine]

  Adds MIT license because the package is tagged with MIT license (from 2013).


0.2.5 (2017-08-31)
------------------
- New release 0.2.5. [Bruno Rocha]
- Merge pull request #58 from mattdavis1121/master. [Bruno Rocha]

  Add fitbounds feature to README
- Update README.md. [Matt Davis]
- Merge pull request #1 from mattdavis1121/add-toggle-for-mapfitbounds.
  [Matt Davis]

  Add toggle for map.fitBounds() - closes issue #55
- Merge pull request #56 from mattdavis1121/add-toggle-for-mapfitbounds.
  [Bruno Rocha]

  Add toggle for map.fitBounds() - closes issue #55
- Add toggle for map.fitBounds() - closes issue #55. [Matt Davis]
- Merge pull request #49 from alfredopironti/master. [Bruno Rocha]

  Fix typo in object dict
- Update documentation for language and region. [Alfredo Pironti]
- Add support for Google Maps language and region. [Alfredo Pironti]
- Fix typo in object dict. [Alfredo Pironti]
- Fix bug that returns attribute error when lat or long is exactly 0
  (#44) [Bruno Rocha]

  * Fix bug that returns attribute error when lat or long is exactly 0

  * replace  '!= None' with  'is not None'
- Replace  '!= None' with  'is not None' [mebroadbent]
- Fix bug that returns attribute error when lat or long is exactly 0.
  [mebroadbent]
- HOTFIX: Make it compatible with Python 2.6 again. [Bruno Rocha]


0.2.4 (2016-10-07)
------------------
- Bump 0.2.3. [Bruno Rocha]


0.2.3 (2016-08-08)
------------------
- Serialize maps as json when passed to jsonify to allow API based
  frontend (#30) [Francisco Fernandes]

  * #30 Early decode from class to JSON dict

  * Fixed some map names and set the dict return instead of json dump

  * Added collapsible attr to as_json func

  * Removed live loading of Google Maps example code through Jquery

  * JSON dumped the Markup file for more encoding/decoding freedom for user

  * Moved import to file top
- Pep8 fixes. [Bruno Rocha]
- Collapsible option + Marker infobox improvements (#38) [Mikhail
  Ksenofontov]

  * Unicode support for marker infoboxes

  * Marker infobox closes when another one opens

  * Added collapsible option

  * Fix for multiple onload functions

  * Infoboxes for rectangles, circles, polygons and polylines

  * Comments deleted

  * Enumerate
- Added scroll wheel option (#36) [Ruan Aragão]

  * Add scroll wheel option

  * Update README.md for add 'scroll_wheel'
- Update README.md. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Changed screenshot example. [Bruno Rocha]
- Add h2 titles to example. [Bruno Rocha]
- Defined varnames and added a dynamic moving map to example.py. [Bruno
  Rocha]
- Fix #27 makes map variable global using map.varname. [Bruno Rocha]
- Added Polylines and Polygons drawing support (#26) [Francisco
  Fernandes]

  * Implemented polyline path drawing

  * Added rendering of polylines at js file

  * Added more polyline path formatting and fixed function to add polylines

  * Wrote some docstrings for polylines and circles functions

  * Added polygons support in maps
- Better way of handling markers, so we dont have tons of JS vars. (#25)
  [Ruben Rocha]
- Add MarkerClusterer support (#24) [Ruben Rocha]

  * Add MarkerClusterer support

  * Fix repetition, oops

  * Cluster now goes into the Map() object, not GoogleMaps(). Added examples folder with static,templates
- Merge pull request #23 from chicao/ISSUE-19-draw-lines-polygons.
  [Bruno Rocha]

  ISSUE #19 Add functionality for drawing Rectangles, Lines, Polygons, Circles and Drawings
- Added support for drawing circles. [Francisco Fernandes]
- Improved code with suggestions and set comparison of dict keys with
  sets. [Francisco Fernandes]
- Implemented the rectangle drawing functionality without classes.
  [Francisco Fernandes]
- Created function to add dict based rectangles to Map.rectangles list.
  [Francisco Fernandes]
- Added support for alpha icons. [Bruno Rocha]
- Add support for marker hover title. [Bruno Rocha]
- Better screenshot iamge. [Bruno Rocha]
- Add notes to add more icons to icons.py module HELP NEEDED. [Bruno
  Rocha]
- Add a control to check if maps script already loaded. [Bruno Rocha]
- Updated screenshot example. [Bruno Rocha]
- Added icons generator. [Bruno Rocha]
- Preparing for 0.2.0. [Bruno Rocha]
- Protocol is relative - using // instead of http: [Bruno Rocha]
- Merge pull request #15 from tvgdb/master. [Bruno Rocha]

  Load Google Maps script over HTTPS
- Load Google Maps script over HTTPS. [Thibault van Geluwe de Berlaere]
- Update README.md. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Update setup.py. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Merge pull request #13 from jclark754/master. [Bruno Rocha]

  Added support for infobox creation
- Added flag to check for list. [Joshua Clark]

  Needed to add a flag to check if infobox was a list or str because
  jinja2 does not have a builtin for type(). This allows a user to
  specify either a list of infobox values or one infobox value for
  multiple markers.
- Added functionality for infoboxes. [Joshua Clark]

  This commit adds support for infobox generation. `infobox` is a new
  optional parameter the user may specify. If passed to the `Map` class,
  info boxes for each marker on the map are created and users may assign
  a list of text/html strings for info box creation. If `infobox` is not
  found in kwargs, the map just shows markers normally. I’ll provide an
  example in the PR.

  Also fixes some very minor PEP8 issues :)
- Update README.md. [Bruno Rocha]
- Protocol bases URL in icon, related to #22. [Bruno Rocha]
- Trying to Fix #12. [Bruno Rocha]
- Upgrades to 1.0.6 and updated pipy fix: #11. [Bruno Rocha]
- Change .ext to _ in import fix #8. [Bruno Rocha]
- Merge pull request #6 from nklever/master. [Bruno Rocha]

  Extending "markers" parameter with additional icons for markers
- Extending "markers" parameter with additional icons for markers.
  [nklever]
- Merge pull request #5 from mjhea0/doc-updates. [Bruno Rocha]

  added parameter info
- Added parametere info. [Michael Herman]
- Merge pull request #1 from bitdeli-chef/master. [Bruno Rocha]

  Add a Bitdeli Badge to README
- Add a Bitdeli badge to README. [Bitdeli Chef]
- Fix example.py. [Bruno Rocha]
- Pep8 fixes. [Bruno Rocha]
- Removed .pyc. [Bruno Rocha]
- Moved to new package. [Bruno Rocha]
- Fix install namespace for flask.ext. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Update README.md. [Bruno Rocha]
- Fix MANIFEST.in and released to PyPI. [Bruno Rocha]
- Install and use instructions. [Bruno Rocha]
- Added screenshot. [Bruno Rocha]
- Initial commit. [Bruno Rocha]


