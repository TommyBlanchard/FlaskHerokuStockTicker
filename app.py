import requests
import pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

app_ticker = Flask(__name__)

app_ticker.vars={}


@app_ticker.route('/')
def main():
  return redirect('/index')

@app_ticker.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app_ticker.route('/graph', methods=['POST'])
def graph():
#    if request.method == 'POST':
        app_ticker.vars['ticker'] = request.form['ticker']

        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=gVz7XbzeecyxHdkCn8yB' % app_ticker.vars['ticker']
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)

        a = raw_data.json()
        df = pandas.DataFrame(a['data'], columns=a['column_names'])

        df['Date'] = pandas.to_datetime(df['Date'])

        p = figure(title='Data from Quandle WIKI set',
            x_axis_label='date',
            x_axis_type='datetime')

        p.line(x=df['Date'].values, 
            y=df['Close'].values,
            line_width=2)
      
        script, div = components(p)
        return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app_ticker.run(port=33507, debug=True)