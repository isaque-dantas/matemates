from flask_login import UserMixin
from app.models import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    MAX_LENGTH = {
        'first_name': 32,
        'last_name': 32,
        'email': 128,
        'username': 24,
        'password': 8,
        'password_hash': 256,
        'phone_number': 32
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(MAX_LENGTH['first_name']), nullable=False)
    last_name = db.Column(db.String(MAX_LENGTH['last_name']), nullable=False)
    email = db.Column(db.String(MAX_LENGTH['email']), nullable=False, unique=True)
    password_hash = db.Column(db.String(MAX_LENGTH['password_hash']), nullable=False)
    username = db.Column(db.String(MAX_LENGTH['username']), nullable=False, unique=True)
    phone_number = db.Column(db.String(MAX_LENGTH['phone_number']))
    birth_date = db.Column(db.Date, nullable=False)


class Entry(db.Model):
    __tablename__ = 'entry'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.String(256), nullable=False)


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statement = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    explanation = db.Column(db.String(256), nullable=False)
    order = db.Column(db.Integer, nullable=False)


class Term(db.Model):
    __tablename__ = 'term'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(256), nullable=False)

    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=False
    )

    explanation = db.Column(db.String(256), nullable=False)
    order = db.Column(db.Integer, nullable=False)


class Syllable(db.Model):
    __tablename__ = 'syllable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(6), nullable=False)
    order = db.Column(db.Integer, nullable=False)


class Definition(db.Model):
    __tablename__ = 'definition'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(6), nullable=False)
    related_math_area = db.Column(
        db.Enum('álgebra', 'cálculo', 'geometria', 'estatística e probabilidade',
                'trigonometria', 'teoria dos números', 'matemática discreta')
    )
    order = db.Column(db.Integer, nullable=False)
