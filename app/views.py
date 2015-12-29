from app import app
from flask import Flask, render_template, jsonify
from tweet_counter import get_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
		return get_data()
# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"