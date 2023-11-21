import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data.users import User
from data.proposals import Proposal
from data.participants import Participant
from data.tournaments import Tournament
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):  # find user in database
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def get_proposal(proposal_id):
    db_sess = db_session.create_session()
    curr_proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    return curr_proposal


def get_tournament(tournament_id):
    db_sess = db_session.create_session()
    curr_tournament = db_sess.query(Proposal).filter(Proposal.id == tournament_id).first()
    return curr_tournament


def get_participant(participant_id):
    db_sess = db_session.create_session()
    curr_participant = db_sess.query(Proposal).filter(Proposal.id == participant_id).first()
    return curr_participant


@app.errorhandler(404)
def not_found(error):
    return "Страница не найдена", 404


@app.errorhandler(401)
def unauthorized_access(error):
    return redirect('/login')


@app.route("/")
def index():
    return "<h1>IN PROGRESS</h1>"


@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html", title="Авторизация")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("main")
    app.run()
