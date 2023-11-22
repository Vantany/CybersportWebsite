import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data.users import User
from data.proposals import Proposal
from data.participants import Participant
from data.tournaments import Tournament
from data import db_session
from forms.loginform import LoginForm, RegistrationForm, ToLoginForm

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
    curr_tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
    return curr_tournament


def get_participant(participant_id):
    db_sess = db_session.create_session()
    curr_participant = db_sess.query(Participant).filter(Participant.id == participant_id).first()
    return curr_participant


@app.errorhandler(404)
def not_found(error):
    return "Страница не найдена", 404


@app.errorhandler(401)
def unauthorized_access(error):
    return redirect('/login')


@app.route("/")
def index():
    form = ToLoginForm()

    if form.validate_on_submit():
        return redirect("/login")

    return render_template("main page.html", title="Главная страница", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        if register_form.password.data != register_form.password_again.data:
            # return render_template('login.html', title='Авторизация',
            #                        register_form=register_form,
            #                        login_form = login_form,
            #                        message="Пароли не совпадают")
            return "Пароли не совпадают"
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == register_form.email.data).first() or db_sess.query(User).filter(
                User.username == register_form.login.data).first():
            # return render_template('login.html', title='Авторизация',
            #                        register_form=register_form,
            #                        login_form = login_form,
            #                        message='Такой пользователь уже существует')
            return "Такой пользователь уже существует"

        user = User()
        user.make_new(username=register_form.login.data, email=register_form.email.data,
                      password=register_form.password.data, position=register_form.position.data)

        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    if login_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            (User.email == login_form.login_or_email.data) or (User.username == login_form.login_or_email.data)).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect("/")
        # return render_template('login.html', title='Авторизация',
        #                            message="Неправильный логин или пароль",
        #                            login_form=login_form,
        #                            register_form=register_form)
        return "Неправильный логин или пароль"

    return render_template('login.html', title='Авторизация', login_form=login_form, register_form=register_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("main")
    app.run(debug=True)
