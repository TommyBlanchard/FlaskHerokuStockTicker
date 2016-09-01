import requests
import pandas
import simplejson as json
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

app.vars={}


@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/graph', methods=['POST'])
def graph():
#    if request.method == 'POST':
        app.vars['ticker'] = request.form['ticker']
        
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json?api_key=gVz7XbzeecyxHdkCn8yB' % app.vars['ticker']
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)

        a = raw_data.json()
        df = pandas.DataFrame(a['data'], columns=a['column_names'])

        df['Date'] = pandas.to_datetime(df['Date'])

        p = figure(title='Stock prices for %s' % app.vars['ticker'],
            x_axis_label='date',
            x_axis_type='datetime')
        
        if request.form.get('Close'):
            p.line(x=df['Date'].values, y=df['Close'].values,line_width=2, legend='Close')
        if request.form.get('Adj. Close'):
            p.line(x=df['Date'].values, y=df['Adj. Close'].values,line_width=2, line_color="green", legend='Adj. Close')
        if request.form.get('Open'):
            p.line(x=df['Date'].values, y=df['Open'].values,line_width=2, line_color="red", legend='Open')
        if request.form.get('Adj. Open'):
            p.line(x=df['Date'].values, y=df['Adj. Open'].values,line_width=2, line_color="purple", legend='Adj. Open')
        script, div = components(p)
        return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
    app.run(port=33507)