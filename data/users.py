import datetime
import json
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Team_leader(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "leaders"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 index=True, unique=True, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    proposals = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def make_new(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return self.password == password or check_password_hash(self.password, password)


class Judge(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "judges"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String,
                                 index=True, unique=True, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tournaments = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def make_new(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return self.password == password or check_password_hash(self.password, password)