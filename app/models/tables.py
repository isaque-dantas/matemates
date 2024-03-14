from flask_login import UserMixin
from app.models import db

from werkzeug.security import generate_password_hash, check_password_hash

import unicodedata
from operator import itemgetter
import re


def normalize_string(query_string: str) -> str:
    normalized = unicodedata.normalize('NFD', query_string)
    return ''.join(
        [char for char in normalized if not unicodedata.combining(char)]
    ).casefold()


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
    role = db.Column(db.Enum('admin', 'normal'), nullable=False)

    @staticmethod
    def register(form):
        password_hash = generate_password_hash(form.password.data)

        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password_hash=password_hash,
            email=form.email.data,
            phone_number=form.phone_number.data,
            birth_date=form.birth_date.data,
            role='normal'
        )

        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get_or_404(user_id)

    def is_password_valid(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'


class Term(db.Model):
    __tablename__ = 'term'

    MAX_CONTENT = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=False
    )

    questions = db.relationship('Question', backref='term')
    syllables = db.relationship('Syllable', backref='term')
    definitions = db.relationship('Definition', backref='term')

    @staticmethod
    def register(form):
        pass

    def get_gender_in_full(self):
        return Term.abbreviation_to_gender_in_full(self.gender)

    @staticmethod
    def abbreviation_to_gender_in_full(abbreviation):
        gender_in_full = {
            'M': 'masculino',
            'F': 'feminino',
        }

        return gender_in_full[abbreviation]

    @staticmethod
    def get_term_by_content(content):
        return Term.query.filter_by(content=content).first()

    @staticmethod
    def search_for_related_terms(search_sentence, gender=None, grammatical_category=None):
        # if gender is not None and grammatical_category is not None:
        #     terms_ids = Term.query.with_entities(Term.id).filter_by(gender=gender).filter_by(
        #         grammatical_category=grammatical_category).all()
        # elif gender is not None:
        #     terms_ids = Term.query.with_entities(Term.id).filter_by(gender=gender).all()
        # elif grammatical_category is not None:
        #     terms_ids = Term.query.with_entities(Term.id).filter_by(grammatical_category=grammatical_category).all()
        # else:
        #     terms_ids = Term.query.with_entities(Term.id).all()
        terms = Term.query.with_entities(Term.id, Term.content).all()

        terms_and_occurrences = []

        for term in terms:
            terms_and_occurrences.append(
                {'term_id': term.id, 'content': term.content, 'occurrences': 0}
            )

        normalized_search_sentence = normalize_string(search_sentence)

        for search_word in normalized_search_sentence.split():
            for i, term_and_occurrences in enumerate(terms_and_occurrences):
                normalized_term_content = normalize_string(term_and_occurrences['content'])

                matched_strings = re.findall(rf'.*{search_word}.*', normalized_term_content)

                if matched_strings and search_word == normalized_term_content:
                    terms_and_occurrences[i]['occurrences'] += 3
                elif matched_strings:
                    terms_and_occurrences[i]['occurrences'] += 1

            #     print(f'{search_word} / {term_content} => {matched_strings}')
            # print()

        terms_and_occurrences = sorted(terms_and_occurrences, key=itemgetter('content'))
        terms_and_occurrences = sorted(terms_and_occurrences, key=itemgetter('occurrences'), reverse=True)

        terms = []
        for term_and_occurrences in terms_and_occurrences:
            if term_and_occurrences['occurrences'] != 0:
                terms.append(
                    Term.query.get(term_and_occurrences['term_id'])
                )

        return terms

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


definition_knowledge_area = \
    db.Table('definition_knowledge_area',
             db.Column('definition_id', db.Integer, db.ForeignKey('definition.id')),
             db.Column('knowledge_id', db.Integer, db.ForeignKey('knowledge_area.id'))
             )


class Definition(db.Model):
    __tablename__ = 'definition'

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))


class KnowledgeArea(db.Model):
    __tablename__ = 'knowledge_area'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(128), nullable=False)
    knowledge_areas = db.relationship('Term', secondary=definition_knowledge_area, backref='knowledge_areas')


if __name__ == '__main__':
    from app import app
    from datetime import date

    with app.app_context():
        # db.drop_all()
        # db.create_all()

        isaque = User(
            first_name='Isaque',
            last_name='Dantas',
            username='isaque-dantas',
            password_hash=generate_password_hash('123456'),
            email='isaque@email.com',
            phone_number='912344321',
            birth_date=date(year=2007),
            role='normal'
        )

        db.session.add(isaque)

        cos = Term(
            content='cosseno',
            gender='M',
            grammatical_category='substantivo'
        )

        cos_definition = Definition(
            content='Razão entre o cateto adjacente e a hipotenusa de determinado ângulo em um triângulo retângulo.',
            order=0
        )

        cos_image = Image(path='alpha.png', term_id=cos.id)

        trigonometry = KnowledgeArea(content='trigonometria', subject='mathematics')
        cos_definition.knowledge_areas.append(cos_definition)

        db.session.add_all([
            Syllable(content='cos', order=0, term=cos),
            Syllable(content='se', order=1, term=cos),
            Syllable(content='no', order=2, term=cos),
            cos, cos_definition, trigonometry
        ])

        calculator = Term(
            content='calculadora',
            gender='F',
            grammatical_category='substantivo'
        )

        calculator_definition = Definition(
            content='Aparelho eletrônico usado para fazer cálculos matemáticos.',
            order=0
        )

        calculator_image = Image(path='alpha.png', term_id=calculator.id)

        db.session.add_all([
            Syllable(content='cal', order=0, term=calculator),
            Syllable(content='cu', order=1, term=calculator),
            Syllable(content='la', order=2, term=calculator),
            Syllable(content='do', order=3, term=calculator),
            Syllable(content='ra', order=4, term=calculator),
            calculator, calculator_definition
        ])

        db.session.commit()
