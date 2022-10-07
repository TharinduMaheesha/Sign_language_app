from flask import Flask, render_template, request, flash
from prompt_toolkit import application
import main as main

app = Flask(__name__, static_folder='static')
app.secret_key = "manbearpig_MUDMAN888"

@app.route("/")
def index():
	flash("what's your name?")
	return render_template("index.html")

@app.route("/greet", methods=['POST', 'GET'])
def greeter():
	link = str(request.form['name_input'])
	test = 	main.mainFunction(link)
	flash(test+".mp4" , "test")
	return render_template("video.html")