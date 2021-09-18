import flask
from joblib import load
import os




model = load('model/mlmodel.joblib') 

app = flask.Flask(__name__, template_folder='templates')
app._static_folder = os.path.abspath("static/")
@app.route('/')
def main():
    return(flask.render_template('main.html'))
if __name__ == '__main__':
    app.run()
