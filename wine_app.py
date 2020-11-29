import flask
import numpy as np
from flask import Flask, render_template, request
from joblib import load


app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

user_input = None


@app.route("/")
def index():
    return flask.render_template("index.html")


def value_predictor(wine_type, to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 11)
    if wine_type == "white":
        loaded_model = load("white_wine_model.joblib")
    elif wine_type == "red":
        loaded_model = load("red_wine_model.joblib")
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route("/predict", methods=["POST"])
def result():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        wine_type = to_predict_list[0]
        to_predict_list = to_predict_list[1:]
        print(to_predict_list)
        to_predict_list = list(map(float, to_predict_list))
        result = value_predictor(wine_type, to_predict_list)
        prediction = str(result)
        if result == 0:
            prediction = "Poor quality"
        elif result == 1:
            prediction = "Normal quality"
        elif result == 2:
            prediction = "Excellent quality"
        return render_template("predict.html", prediction=prediction)


@app.route("/predict")
def predict():
    return render_template("predict.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()