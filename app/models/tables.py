from flask_login import UserMixin
from app.models import db
from app import app


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


class Term(db.Model):
    __tablename__ = 'term'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=False
    )

    def get_gender_in_full(self):
        gender_in_full = {
            'M': 'masculino',
            'F': 'feminino',
        }

        return gender_in_full[self.gender]

    @staticmethod
    def get_term_by_content(content):
        return Term.query.filter_by(content=content).first()

    def get_one(self, entity):
        return entity.query.filter_by(term_id=self.id).first()

    def get_many(self, entity):
        return entity.query.filter_by(term_id=self.id).order_by(entity.order.asc()).all()

    def get_image(self):
        return self.get_one(Image)

    def get_questions(self):
        return self.get_many(Question)

    def get_definitions(self):
        return self.get_many(Definition)

    def get_syllables(self):
        return self.get_many(Syllable)


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.String(256), nullable=True)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statement = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    explanation = db.Column(db.String(256), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))


class Syllable(db.Model):
    __tablename__ = 'syllable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(6), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))


class Definition(db.Model):
    __tablename__ = 'definition'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False)
    related_math_area = db.Column(
        db.Enum('álgebra', 'cálculo', 'geometria', 'estatística e probabilidade',
                'trigonometria', 'teoria dos números', 'matemática discreta')
    )
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         db.drop_all()
