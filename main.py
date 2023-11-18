<<<<<<< HEAD
import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
=======
from flask import Flask, render_template
>>>>>>> 66398e9e7ba3b88b031730c883d6f9fc8ae6863d

<<<<<<< HEAD
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error): 
    return "Страница не найдена", 404

@app.route('/')
def index():
    return render_template("index.html", title = "Main page")


if __name__ == "__main__":
    app.run()
=======


app = Flask(__name__)
app.config["SECRET_KEY"] = 'oaoaooa'
app.config["JSON_AS_ASCII"] = False



@app.route("/")
def index():
    return "<h1>IN PROGRESS</h1>"


@app.route("/login")
def login():
    return render_template("login.html")
>>>>>>> 66398e9e7ba3b88b031730c883d6f9fc8ae6863d