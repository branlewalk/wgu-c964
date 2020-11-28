import os
import pandas as pd
import numpy as np
import flask
from joblib import load
from flask import Flask, render_template, request

STATIC_DIR = os.path.abspath('../static')

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def index():
    return flask.render_template("index.html")


def value_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 11)
    loaded_model = load("red_wine_model.joblib")
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route("/predict", methods = ["POST"])
def result():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        result = value_predictor(to_predict_list)
        prediction = str(result)
        return render_template("predict.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)