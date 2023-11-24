import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired


class AddTournamentForm(FlaskForm):
    name = StringField('Введите название соревнования',
                       validators=[DataRequired(message="Поле 'название' не может быть пустым")])
    place = StringField('Введите место проведения соревнования',
                        validators=[DataRequired(message="Поле 'место' не может быть пустым")])
    organizer = StringField('Введите организатора соревнования',
                            validators=[DataRequired(message="Поле 'организатор' не может быть пустым")])
    discipline = StringField('Введите игру, по которой будет проводиться соревнование',
                             validators=[DataRequired(message="Поле 'дисциплина' не может быть пустым")])
    participants_amount = StringField('Введите колличество участников в одной команде',
                                      validators=[DataRequired(message="Данное поле не может быть пустым")])
    teams_amount = StringField('Введите колличество команд',
                               validators=[DataRequired(message="Данное поле не может быть пустым")])
    registration_time = DateField('Введите дату начала регистрации', format='%d-%m-%Y',
                                  validators=[DataRequired(message="Данное поле не может быть пустым")])
    start_time = DateField('Введите дату открытия соревнования', format='%d-%m-%Y',
                           validators=[DataRequired(message="Данное поле не может быть пустым")])
    end_time = DateField('Введите дату окончания соревнования', format='%d-%m-%Y',
                         validators=[DataRequired(message="Данное поле не может быть пустым")])
    closure_time = DateField('Введите дату закрытия соревнования', format='%d-%m-%Y',
                             validators=[DataRequired(message="Данное поле не может быть пустым")])
    submit = SubmitField('Добавить турнир')

    @property
    def get_deadlines(self):
        deadlines = {
            "registration": datetime.datetime.strptime(self.registration_time, "%d-%m-%Y"),
            "start": datetime.datetime.strptime(self.start_time, "%d-%m-%Y"),
            "end": datetime.datetime.strptime(self.end_time, "%d-%m-%Y"),
            "close": datetime.datetime.strptime(self.closure_time, "%d-%m-%Y")
        }
        return deadlines
