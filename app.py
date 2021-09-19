  
import flask
from joblib import load
import os
import numpy as np
from flask import request, jsonify
import urllib
import json
import pandas as pd
import plotly.express as px




model = load('models/mlmodel.joblib') 


app = flask.Flask(__name__, template_folder='templates')
app._static_folder = os.path.abspath("static/")


def predict():
    a = float(request.args.get('speedval', 0))
    b = float(request.args.get('direction', 0))
    a = a/19.5
    b = b/360
    result = model.predict([[a,b]])
    r = result[0]
    return jsonify(
       
        { 'prediction' : r
        })


app.add_url_rule('/predict','predict', predict)

def forecast():
    city = request.args.get('city',0)
    api = 'http://api.openweathermap.org/data/2.5/onecall?lat=20.95&lon=85.10&exclude=daily&appid=18e247e0f23aeb979d363b605126f7e9'
    print(api)
    source = urllib.request.urlopen(api).read()
    list_of_data = dict(json.loads(source))
    hourly = list_of_data['hourly']
    speed =dict()
    windspeed = []
    winddirection = []
    for i in range(len(hourly)):
        speed[i] = hourly[i]
    for j in range(len(speed)):
        
        windspeed.append(speed[j]['wind_speed'])
        winddirection.append(speed[j]['wind_deg'])
    
    data = pd.DataFrame()
    data['WindSpeed'] = windspeed
    data['WindDir'] = winddirection
    
    data['WindSpeed'] = data['WindSpeed']/19.45
    data['WindDir']= data['WindDir']/360
    

    result = model.predict(data)
    result = result*3600
    output = pd.DataFrame(result,columns=['Power generated(kWh)'])
    
    k = float(output.max())
    m = float(output.idxmax(axis = 0))
    

    fig = px.line(output, y='Power generated(kWh)',labels={'index':'No of hrs'})
    fig.write_html("./templates/graph.html")
    fig.write_html("./static/graph.html")
    return jsonify(
        {
            'max_output' : k,
            'hour': m

        }
    )

   

    
app.add_url_rule('/forecast','forecast', forecast)

@app.route('/graph')    
def graph():
    return(flask.render_template('graph.html'))



@app.route('/')
def main(): 
    return(flask.render_template('main.html'))
if __name__ == '__main__':
    app.run()




