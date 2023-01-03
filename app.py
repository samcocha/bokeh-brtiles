from flask import Flask, render_template

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import WMTSTileSource

app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello, Sam!'

@app.route('/bokeh')
def bokeh():
  tile_provider = WMTSTileSource(
      url='http://tiles.buienradar.nl/tiles-eu-v2/{Z}/{X}/{Y}.png',
      attribution='Test by Sam with Buienradar Tiles'
  )

  # range bounds supplied in web mercator coordinates
  fig = figure(x_range=(230000, 880000), y_range=(6750000, 6900000),
            x_axis_type="mercator", y_axis_type="mercator")
  fig.add_tile(tile_provider)

  # grab the static resources
  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()

  # render template
  script, div = components(fig)
  html = render_template(
      'index.html',
      plot_script=script,
      plot_div=div,
      js_resources=js_resources,
      css_resources=css_resources,
  )

  return html