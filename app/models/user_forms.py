from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, DateField
from wtforms.validators import DataRequired, Length

from app.models.tables import User


class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário',
                           validators=[
                               DataRequired(),
                               Length(2, User.MAX_LENGTH['username'])
                           ])

    name = StringField('Nome e sobrenome',
                       validators=[
                           DataRequired(),
                           Length(2, User.MAX_LENGTH['name'])
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

    phone_number = StringField('Telefone')
    birth_date = DateField('Data de nascimento')

    image = FileField('Foto de perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos \'jpg\', \'png\' ou \'jpeg\' são permitidos.'),
    ])

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
