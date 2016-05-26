from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
from bokeh.embed import components
import requests

app = Flask(__name__)
app.vars = {}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['POST'])
def index():
  app.vars['ticker'] = request.form['ticker']
  app.vars['features'] = request.form['features']

  api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % app.vars['ticker']
  session = requests.Session()
  session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
  raw_data = session.get(api.url)

  plot = figure(tools=TOOLS, title='Data from Quandl WIKI set',
 		x_axis_label='date', x_axis_type='datetime')

  script, div = components(plot)

  return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)

