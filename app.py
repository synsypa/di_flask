from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show
from bokeh.embed import components
import requests
import json
import numpy as np
import pandas as pd

app = Flask(__name__)
features = []
ticker = ''

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    ticker = request.form['ticker'].upper()
    features = request.form['features']

    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % ticker
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api.url)

    cols = raw_data.json()[u'column_names']
    data = raw_data.json()[u'data']
    df = pd.DataFrame(data)
    df.columns = cols
    df['Date'] = pd.to_datetime(df['Date'])

    p = figure(tools=TOOLS, title='Data from Quandl WIKI set',
 		x_axis_label='date', x_axis_type='datetime')

    p.line(df['Date'], df['Open'], color='#A6CEE3', legend=ticker + ": " + feature)

    script, div = components(plot)
    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)

