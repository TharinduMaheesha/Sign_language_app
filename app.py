from flask import Flask, render_template, request, flash
import SER_prediction as SER
import video_to_audio as audio
import audio_to_text as text
import video_emotion as video
import text_emotion as text2
import main as main
from moviepy.editor import VideoFileClip, concatenate_videoclips

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