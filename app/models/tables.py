from flask_login import UserMixin
from app.models import db

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
    role = db.Column(db.Enum('admin', 'normal'))


class Term(db.Model):
    __tablename__ = 'term'

    MAX_CONTENT = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=False
    )

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


class Definition(db.Model):
    __tablename__ = 'definition'

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    related_knowledge_area = db.Column(
        db.Enum('álgebra', 'cálculo', 'geometria', 'estatística e probabilidade',
                'trigonometria', 'teoria dos números', 'matemática discreta', 'física')
    )
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#         db.drop_all()
