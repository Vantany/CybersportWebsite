import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
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
    deadlines = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    judges = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    grid = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    results = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def make_new(self, name, place, organizer, discipline, deadlines, participants_amount):
        self.name = name
        self.place = place
        self.organizer = organizer
        self.discipline = discipline
        self.deadlines = deadlines
        self.participants_amount = participants_amount

    def add_results(self, results):
        self.results = results