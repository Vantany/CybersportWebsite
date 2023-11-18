from flask import Flask, render_template



app = Flask(__name__)
app.config["SECRET_KEY"] = 'oaoaooa'
app.config["JSON_AS_ASCII"] = False



@app.route("/")
def index():
    return "<h1>IN PROGRESS</h1>"


@app.route("/login")
def login():
    return render_template("login.html")