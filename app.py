  
import flask
from joblib import load
import os
import numpy as np
from flask import request, jsonify




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

@app.route('/')
def main(): 
    return(flask.render_template('main.html'))
if __name__ == '__main__':
    app.run()




