from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.palettes import Spectral4
import requests
import json
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    ticker = request.form['ticker'].upper()
    features = request.form.getlist('features')

    api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=5wY62Y1qbsMcJA9qVjBz' % ticker
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    raw_data = session.get(api_url)

    if len(raw_data.json()) <= 1:
	return render_template('error.html', ticker=ticker)

    else:
      cols = raw_data.json()[u'column_names']
      data = raw_data.json()[u'data']
      df = pd.DataFrame(data)
      df.columns = cols
      df['Date'] = pd.to_datetime(df['Date'])

      p = figure(title='Data from Quandl WIKI set',
 		x_axis_label='date', x_axis_type='datetime')
      for (f, c) in zip(features, Spectral4):
        p.line(df['Date'], df[f], line_color=c, legend=ticker + ": " + f)    

      script, div = components(p)
      return render_template('graph.html', script=script, div=div, ticker=ticker)

if __name__ == '__main__':
#  app.run(port=33507)
  app.run(host='0.0.0.0')
