from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField, FileField
from wtforms.validators import DataRequired, Length

from app.models.tables import User


class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário',
                           validators=[
                               DataRequired(),
                               Length(2, User.MAX_LENGTH['username'])
                           ])
    first_name = StringField('Primeiro nome',
                             validators=[
                                 DataRequired(),
                                 Length(2, User.MAX_LENGTH['first_name'])
                             ])

    last_name = StringField('Sobrenome',
                            validators=[
                                DataRequired(),
                                Length(2, User.MAX_LENGTH['last_name'])
                            ])

    password = PasswordField('Senha',
                             validators=[
                                 DataRequired(),
                                 Length(4, User.MAX_LENGTH['password'])
                             ])

    email = EmailField('E-mail',
                       validators=[
                           DataRequired(),
                           Length(max=User.MAX_LENGTH['email']),
                       ])

    phone_number = FileField('Telefone')
    birth_date = DateField('Data de nascimento')

    submit = SubmitField('Confirmar')


class LoginForm(FlaskForm):
    email = EmailField('E-mail',
                       validators=[
                           DataRequired(),
                           Length(max=User.MAX_LENGTH['email'])
                       ])

    password = PasswordField('Senha',
                             validators=[
                                 DataRequired(),
                                 Length(max=User.MAX_LENGTH['password'])
                             ])

    submit = SubmitField('Confirmar')