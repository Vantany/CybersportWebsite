import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
from .db_session import SqlAlchemyBase


class Proposal(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "proposals"

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    tournament_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def make_new(self, id, tournament_id):
        self.id = id
        self.tournament_id = tournament_id
        self.status = False

