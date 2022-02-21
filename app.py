import os
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

URL = "http://localhost:1323"

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated_function



@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

@app.route("/login", methods=["GET", "POST"])
def login():
	session.clear()
	if request.method == "POST":
		name=request.form.get("username")
		password=request.form.get("password")
		res=requests.post(URL+"/login",data={"name":name,"password":password})
		
		if res.json()["name"]=="":
			return render_template("login.html")
		return redirect("/")
	else:
		return render_template("login.html")


@app.route("/")
def index():
	res = requests.get(URL+"/user")
	print(res)
	print(res.json())
	jsondata=res.json()
	print("fas:")
	print(jsondata[0]["id"])
	return render_template("index.html")



if __name__ == '__main__':
   app.run(debug=True)
