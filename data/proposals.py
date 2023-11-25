import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
import json
from .db_session import SqlAlchemyBase


class Proposal(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'proposals'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    team_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    participants = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    tournament_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def make_new(self, team_id, tournament_id, team_name):
        self.team_id = team_id
        self.tournament_id = tournament_id
        self.team_name = team_name
        self.participants = json.dumps({'participants': []})
        self.status = False

    def approve_proposal(self):
        self.status = True if (self.status == False) else False

    @property
    def participants_list(self):
        return json.loads(self.participants)['participants']

    def add_participant(self, participant_id):
        participant_list = self.participants_list
        participant_list.append(participant_id)
        self.participants = json.dumps({'participants': participant_list})

    def delete_participant(self, participant_id):
        partipant_list = self.participant_list
        if participant_id in partipant_list:
            partipant_list.remove(participant_id)
        self.participants = json.dumps({'participants': partipant_list})
