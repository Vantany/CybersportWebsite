import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error): 
    return "Страница не найдена", 404


@app.route("/")
def index():
    return "<h1>IN PROGRESS</h1>"


@app.route("/login")
def login():
    return render_template("login.html")