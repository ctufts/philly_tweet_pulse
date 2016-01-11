from app import app
from flask import Flask, render_template, jsonify
from mysql_python import philly_tweet_tools 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
		return philly_tweet_tools.get_data()
		
@app.route("/genderData")
def genderData():
		return philly_tweet_tools.get_gender_data()

@app.route("/ageData")
def ageData():
		return philly_tweet_tools.get_age_data()

# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"