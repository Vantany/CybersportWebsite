import os
from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data.users import User
from data.proposals import Proposal
from data.participants import Participant
from data.tournaments import Tournament
from data import db_session
from forms.loginform import LoginForm, RegistrationForm
from forms.addtournamentform import AddTournamentForm
from forms.edittournamentform import EditTournamentForm
from tables import deadlines

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
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
    return render_template("main page.html", title="Главная страница")


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


@app.route('/account', methods=["POST", "GET"])
@login_required
def account():
    if current_user.access_level == 0:
        db_sess = db_session.create_session()
        my_proposals_ids = current_user.proposals_list
        my_proposals = []
        for proposal_id in my_proposals_ids:
            current_proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
            tourtament = db_sess.query(Tournament).filter(Tournament.id == current_proposal.tourtament_id).first()
            participants = []
            for participant in current_proposal.participant_list():
                participants.append(participant.username)
            proposal = {
                "tornament_name": tourtament.name,
                "team": participants,
                "status": current_proposal.status
            }
            my_proposals.append(proposal)
        return render_template('index-leader.html',
                               proposals=my_proposals,
                               is_empty=len(my_proposals) == 0)
    else:
        db_sess = db_session.create_session()
        my_tournaments_ids = current_user.tournaments_list
        my_tournaments = []
        for tournament_id in my_tournaments_ids:
            current_tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
            current_tournament.update_status()
            proposal_amount = db_sess.query(Proposal).filter(Proposal.tournament_id == tournament_id).count()
            tournament = {
                "tournament_name": current_tournament.name,
                "proposals_amount": proposal_amount,
                "proposals_need": current_tournament.participants_amount,
                "tournament_status": deadlines[current_tournament.status]
            }
            my_tournaments.append(tournament)
        return render_template('index-judge.html',
                               tournaments=my_tournaments,
                               is_empty=len(my_tournaments) == 0)


@app.route('/add_tournament', methods=["POST", "GET"])
@login_required
def add_tournament():
    if current_user.access_level == 0:
        return "Недостаточно прав доступа для проведения турнира"
    else:
        form = AddTournamentForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            new_tournament = Tournament()

            new_tournament.make_new(name=form.name.data, place=form.place.data,
                                    organizer=form.organizer.data, discipline=form.discipline.data,
                                    deadlines=form.get_deadlines(),
                                    participants_amount=form.participants_amount.data)

            db_sess.add(new_tournament)
            db_sess.commit()
            current_user.add_tournament(new_tournament.id)
            db_sess.commit()

            return redirect("/account")

        return render_template("add_tourtament.html",
                               form=form)


@app.route('/edit_tournament/<int:tournament_id>', methods=["POST", "GET"])
@login_required
def edit_toutnament(tournament_id):
    db_sess = db_session.create_session()
    tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament:
        form = EditTournamentForm()
        if form.validate_on_submit():
            tournament.edit(name=form.name.data, place=form.place.data,
                            organizer=form.organizer.data, discipline=form.discipline.data,
                            deadlines=form.get_deadlines(),
                            participants_amount=form.participants_amount.data)
            db_sess.commit()
    else:
        abort(404)
    return redirect('/account')


@app.route('/delete_tournament/<int:tournament_id>', methods=["POST", "GET"])
@login_required
def delete_toutnament(tournament_id):
    db_sess = db_session.create_session()
    tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament:
        db_sess.delete(tournament)
        if tournament_id in current_user.tournament_list():
            current_user.delete_tournament(tournament_id)
        for proposal in db_sess.query(Proposal).filter(Proposal.tournament_id == tournament_id).all():
            db_sess.delete(proposal)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/account')


if __name__ == "__main__":
    db_session.global_init("main")
    app.run(debug=True)
