  
import flask
from joblib import load
import os
import numpy as np
from flask import request, jsonify




model = load('models/mlmodel.joblib') 


app = flask.Flask(__name__, template_folder='templates')
app._static_folder = os.path.abspath("static/")
@app.route('/')
def main():
    return(flask.render_template('main.html'))
if __name__ == '__main__':
    app.run()

@app.route('/predict')
def predict():
    #For rendering results on HTML GUI
    a = float(request.args.get('speedval', 0))
    b = float(request.args.get('direction', 0))

    
    return jsonify({
        'prediction': '1200kW',

    })