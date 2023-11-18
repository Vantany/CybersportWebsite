from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired



class RegisterForm(FlaskForm):
    login = StringField('Придумайте логин', validators=[DataRequired(message="Поле 'логин' не может быть пустым")])
    email = StringField('Введите адрес электронной почты', validators=[DataRequired(message="Поле 'почта' не может быть пустым")])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    is_captain = BooleanField('Я - капитан команды')
    is_judge = BooleanField("Я - судья")
    submit = SubmitField('Зарегистрироваться')