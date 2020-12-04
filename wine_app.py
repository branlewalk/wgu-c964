import flask
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, flash
from joblib import load
from functools import wraps


app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
user_input = None


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'WineCo' or request.form['password'] != 'Red&White':
            error = 'Wrong username or password. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route("/")
@login_required
def index():
    return flask.render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return flask.render_template("dashboard.html")


def value_predictor(wine_type, to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 11)
    if wine_type == "white":
        loaded_model = load("white_wine_model.joblib")
    elif wine_type == "red":
        loaded_model = load("red_wine_model.joblib")
    result = loaded_model.predict(to_predict)
    return result[0]


@app.route("/predict", methods=["POST"])
@login_required
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
@login_required
def predict():
    return render_template("predict.html")


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)