import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired


class AddProposalForm(FlaskForm):
    team_name = StringField('Введите название команды',
                            validators=[DataRequired(message="Поле 'никнейм' не может быть пустым")])
    username = [StringField('Введите никнейм этого игрока',
                            validators=[DataRequired(message="Поле 'никнейм' не может быть пустым")])]
    fullname = [StringField('Введите ФИО этого игрока',
                            validators=[DataRequired(message="Поле 'ФИО' не может быть пустым")])]
    gender = [SelectField("Выберите пол данного игрока: ", choices=[("m", "Мужской"), ("w", "Женский")])]
    birth_date = [DateField('Введите дату рождения данного игрока', format='%d-%m-%Y',
                            validators=[DataRequired(message="Данное поле не может быть пустым")])]
    gto = [StringField('Введите номер ГТО этого игрока',
                       validators=[DataRequired(message="Поле 'ГТО' не может быть пустым")])]
    contact = [StringField('Введите почту этого игрока',
                           validators=[DataRequired(message="Поле 'почта' не может быть пустым")])]

    submit = SubmitField('Добавить заявку')

    def data_expansion(self, amount):
        for i in range(amount):
            self.username.append(StringField('Введите никнейм этого игрока',
                                             validators=[DataRequired(message="Поле 'никнейм' не может быть пустым")]))
            self.fullname.append(StringField('Введите ФИО этого игрока',
                                             validators=[DataRequired(message="Поле 'ФИО' не может быть пустым")]))
            self.gender.append(
                SelectField("Выберите пол данного игрока: ", choices=[("m", "Мужской"), ("w", "Женский")]))
            self.birth_date.append(DateField('Введите дату рождения данного игрока', format='%d-%m-%Y',
                                             validators=[DataRequired(message="Данное поле не может быть пустым")]))
            self.gto.append(StringField('Введите номер ГТО этого игрока',
                                        validators=[DataRequired(message="Поле 'ГТО' не может быть пустым")]))
            self.contact.append(StringField('Введите почту этого игрока',
                                            validators=[DataRequired(message="Поле 'почта' не может быть пустым")]))