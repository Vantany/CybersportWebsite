import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data.users import User, Team_leader, Judge
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(404)
def not_found(error):
    return "Страница не найдена", 404


@app.route("/")
def index():
    return "<h1>IN PROGRESS</h1>"


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html", title = "Авторизация")


if __name__ == "__main__":
    db_session.global_init("main")
    app.run()
