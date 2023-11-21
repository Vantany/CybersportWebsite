from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, SelectField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    is_registration = True
    login_or_email = StringField('Логин или адрес электронной почты', validators=[DataRequired()])
    username = StringField('Введите имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    password_again = PasswordField('Повторите пароль',
                                   validators=[DataRequired(message="Поле 'пароль' не может быть пустым")])
    login = StringField('Придумайте логин', validators=[DataRequired(message="Поле 'логин' не может быть пустым")])
    email = StringField('Введите адрес электронной почты',
                        validators=[DataRequired(message="Поле 'почта' не может быть пустым")])
    position = SelectField(choices=[("user", "Я капитан"), ("judge", "Я судья")])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    @property
    def get_position(self):
        return "user" if self.position.data == 0 else "judge"
