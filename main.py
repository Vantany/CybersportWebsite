import os
from flask import Flask, render_template, redirect, abort, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template
from data.users import User
from data.proposals import Proposal
from data.participants import Participant
from data.tournaments import Tournament
from data import db_session
from forms.loginform import LoginForm, RegistrationForm
from forms.addtournamentform import AddTournamentForm
from forms.addproposalform import AddProposalForm
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
            flash("Пароли не совпадают, повторите попытку регистрации", "error")
            # return "Пароли не совпадают"
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == register_form.email.data).first() or db_sess.query(User).filter(
                User.username == register_form.login.data).first():
            flash("Такой пользователь уже существует", "error")

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
        flash("Неправильный логин или пароль", "error")

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
        my_proposals = []
        not_confirmed_proposals = []
        for tournament_id in my_tournaments_ids:
            current_tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
            current_tournament.update_status()
            proposal_amount = db_sess.query(Proposal).filter(
                Proposal.tournament_id == tournament_id and Proposal.status).count()
            for proposal in db_sess.query(Proposal).filter(Proposal.tournament_id == tournament_id).all():
                if not proposal.status:
                    not_confirmed_proposals.append(proposal.id)
            tournament = {
                "tournament_name": current_tournament.name,
                "proposals_amount": proposal_amount,
                "proposals_need": current_tournament.teams_amount,
                "tournament_status": deadlines[current_tournament.status]
            }
            my_tournaments.append(tournament)

        for proposal_id in not_confirmed_proposals:
            current_proposal = get_proposal(proposal_id)
            current_tournament = get_tournament(current_proposal.tourtament_id)
            proposal = {
                "proposal_id": current_proposal.id,
                "team_name": current_proposal.team_name,
                "tournament_name": current_tournament.name
            }
            my_proposals.append(proposal)
        return render_template('index-judge.html',
                               tournaments=my_tournaments,
                               proposals=my_proposals,
                               is_empty_tournamnets=len(my_tournaments) == 0,
                               is_empty_proposals=len(my_proposals) == 0)


@app.route("/approve_proposal/<int:proposal_id>", methods=["POST", "GET"])
@login_required
def approve_proposal(proposal_id):
    if current_user.access_level == 0:
        return "Вы не имеете таких прав доступа"
    else:
        proposal = get_proposal(proposal_id)
        proposal.approve_proposal()
        return redirect("/account")


@app.route('/add_proposal/<int:tournament_id>', methods=["POST", "GET"])
@login_required
def add_proposal(tournament_id):
    if current_user.access_level == 1:
        return "Вы не можете подавать заявки на турниры"
    else:
        form = AddProposalForm()
        tournament = get_tournament(tournament_id)
        form.data_expansion(tournament.participants_amount)
        proposal = Proposal()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            for i in range(tournament.participants_amount):
                participant = Participant()
                participant.make_new(username=form.username[i].data,
                                     fullname=form.fullname[i].data, gender=form.gender[i].data,
                                     birth_date=form.birth_date[i].data, gto=form.gto[i].data,
                                     contact=form.contact[i].data)
                db_sess.add(participant)
                proposal.add_participant(participant.id)
            proposal.make_new(team_id=current_user.id,
                              team_name=form.team_name.data, tournament_id=tournament_id)
            db_sess.add(proposal)
            db_sess.commit()
            return redirect('/account')

    return render_template('add_proposal.html', form=form)


@app.route('/edit_proposal/<int:proposal_id>', methods=["POST", "GET"])
@login_required
def edit_proposal(proposal_id):
    db_sess = db_session.create_session()
    proposal = db_sess.query(Proposal).filter(Proposal.id == proposal_id).first()
    data = {
        "id": [],
        "username": [],
        "fullname": [],
        "gender": [],
        "birth_date": [],
        "gto": [],
        "contact": []
    }
    for participant_id in proposal.participant_list:
        participant = get_participant(participant_id)
        data["id"].append(participant_id)
        data["username"].append(participant.username)
        data["fullname"].append(participant.fullname)
        data["gender"].append(participant.gender)
        data["birth_date"].append(participant.birth_date)
        data["gto"].append(participant.gto)
        data["contact"].append(participant.contact)

    if proposal:
        form = AddProposalForm()
        tournament = get_tournament(proposal.tournament_id)
        form.data_expansion(tournament.participants_amount)
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            for i in range(tournament.participants_amount):
                participant = get_participant(data["id"][i])
                participant.update(username=form.username[i].data,
                                   fullname=form.fullname[i].data, gender=form.gender[i].data,
                                   birth_date=form.birth_date[i].data, gto=form.gto[i].data,
                                   contact=form.contact[i].data)
            db_sess.commit()
    else:
        abort(404)

    return render_template('edit_proposal.html', form=form, data=data)


@app.route('/delete_proposal/<int:proposal_id>', methods=["POST", "GET"])
@login_required
def delete_proposal(proposal_id):
    db_sess = db_session.create_session()
    proposal = get_proposal(proposal_id)
    if proposal:
        for participant_id in proposal.participant_list:
            participant = get_participant(participant_id)
            db_sess.delete(participant)
        user = db_sess.query(User).filter(User.id == proposal.team_id).first()
        user.delete_proposal(proposal_id)
        db_sess.delete(proposal)
        db_sess.commit()
    else:
        abort(404)

    return redirect('/account')


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
def edit_tournament(tournament_id):
    db_sess = db_session.create_session()
    tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament:
        form = AddTournamentForm()
        if form.validate_on_submit():
            tournament.edit(name=form.name.data, place=form.place.data,
                            organizer=form.organizer.data, discipline=form.discipline.data,
                            deadlines=form.get_deadlines(),
                            participants_amount=form.participants_amount.data)
            db_sess.commit()
    else:
        abort(404)
    return render_template("edit_tournament.html", form=form, tournament=tournament)


@app.route('/delete_tournament/<int:tournament_id>', methods=["POST", "GET"])
@login_required
def delete_tournament(tournament_id):
    db_sess = db_session.create_session()
    tournament = db_sess.query(Tournament).filter(Tournament.id == tournament_id).first()
    if tournament:
        db_sess.delete(tournament)
        if tournament_id in current_user.tournament_list():
            current_user.delete_tournament(tournament_id)
        for proposal in db_sess.query(Proposal).filter(Proposal.tournament_id == tournament_id).all():
            for participant_id in proposal.participant_list:
                participant = get_participant(participant_id)
                db_sess.delete(participant)
            user = db_sess.query(User).filter(User.id == proposal.team_id).first()
            user.delete_proposal(proposal.id)
            db_sess.delete(proposal)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/account')


@app.route('/tournament/<int:tournament_id>', methods=["POST", "GET"])
def tournament(tournament_id):
    pass


if __name__ == "__main__":
    db_session.global_init("main")
    app.run(debug=True)
