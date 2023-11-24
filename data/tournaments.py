import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
import random
from math import log2
from .db_session import SqlAlchemyBase


class Tournament(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tournaments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             index=True, unique=True, nullable=True)
    place = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    organizer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    discipline = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    participants_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    teams_amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    deadlines = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    judges = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    grid = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    results = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def make_new(self, name, place, organizer, discipline, deadlines, participants_amount, teams_amount):
        self.name = name
        self.place = place
        self.organizer = organizer
        self.discipline = discipline
        self.deadlines = deadlines
        self.participants_amount = participants_amount
        self.teams_amount = teams_amount
        self.status = 0
        self.grid = json.dumps({"grid": []})

    def add_results(self, results):
        self.results = results

    def update_status(self):
        status = json.loads(self.deadlines)['deadlines']
        if datetime.datetime.today() > status["registration"]:
            self.status = 1
        if datetime.datetime.today() > status["start"]:
            self.status = 2
        if datetime.datetime.today() > status["end"]:
            self.status = 3
        if datetime.datetime.today() > status["close"]:
            self.status = 4

    def edit(self, name, place, organizer, discipline, deadlines, participants_amount, teams_amount):
        self.name = name
        self.place = place
        self.organizer = organizer
        self.discipline = discipline
        self.deadlines = deadlines
        self.participants_amount = participants_amount
        self.teams_amount = teams_amount
        self.status = 0

    def randomize_grid(self, team_ids):
        self.grid = json.dumps({"grid": random.shuffle(team_ids)})

    def update_grid(self, winner_teams):
        grid = json.loads(self.grid)["grid"]
        grid.extend(winner_teams)
        self.grid = json.dumps({"grid": grid})
