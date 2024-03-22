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

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False, unique=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=False
    )

    image = db.relationship('Image', backref='term', uselist=False)
    questions = db.relationship('Question', backref='term')
    syllables = db.relationship('Syllable', backref='term')
    definitions = db.relationship('Definition', backref='term')

    @staticmethod
    def register(form_data):
        print(form_data)
        term_content = form_data['content'].replace('.', '').casefold()

        term = Term(
            content=term_content,
            gender=form_data['gender'],
            grammatical_category=form_data['grammatical_category']
        )

        syllables = form_data['content'].split('.')
        for i, syllable in enumerate(syllables):
            syllable = Syllable(
                content=syllable,
                order=i,
                term=term
            )

            term.syllables.append(syllable)
            db.session.add(syllable)

        if form_data['image_path']:
            image = Image(
                path=form_data['image_path'],
                caption=form_data['image_caption'] if form_data['image_caption'] else None,
                term=term
            )

            db.session.add(image)

        n_attributes = {
            'definition': [],
            'question': []
        }

        print(form_data)

        for key, value in form_data.items():
            if 'definition' not in key and 'question' not in key:
                continue

            key_index = Term.get_index_from_key(key)
            key_description = Term.get_description_from_key(key)
            key_entity_name = Term.get_entity_name_from_key(key)

            try:
                n_attributes[key_entity_name][key_index].update(
                    {key_description: value}
                )
            except IndexError:
                n_attributes[key_entity_name].append(
                    {key_description: value, 'order': key_index}
                )

        for definition_data in n_attributes['definition']:
            if definition_data['content'] and definition_data['knowledge_area']:
                definition = Definition(
                    content=definition_data['content'],
                    order=definition_data['order']
                )

                definition.knowledge_area = KnowledgeArea.query.filter_by(content=definition_data['knowledge_area']).first()

                term.definitions.append(definition)
                db.session.add(definition)

        for question in n_attributes['question']:
            if question['statement'] and question['answer']:
                question = Question(
                    statement=question['statement'],
                    answer=question['answer'],
                    order=question['order']
                )

                term.questions.append(question)
                db.session.add(question)

        db.session.commit()

    def delete_term(self):
        entities_lists = [self.definitions, self.syllables, self.questions]

        for entities_list in entities_lists:
            for entity in entities_list:
                db.session.delete(entity)

        db.session.delete(self.image)
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_index_from_key(key: str):
        return int(key.rsplit('_', 1)[1]) - 1

    @staticmethod
    def get_description_from_key(key: str):
        return key.rsplit('_', 1)[0].split('_', 1)[1]

    @staticmethod
    def get_entity_name_from_key(key: str):
        return key.split('_', 1)[0]

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


class KnowledgeArea(db.Model):
    __tablename__ = 'knowledge_area'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(128), nullable=False, unique=True)
    subject = db.Column(db.String(128), nullable=False)
    definitions = db.relationship('Definition', backref='knowledge_area')

    @staticmethod
    def get_term_creation_form_definitions_choices():
        contents = KnowledgeArea.query.with_entities(KnowledgeArea.content).order_by(KnowledgeArea.content).all()

        for i, content in enumerate(contents):
            content_capitalized = content[0][0].upper() + content[0][1:]
            contents[i] = (content[0], content_capitalized)

        return contents


class Definition(db.Model):
    __tablename__ = 'definition'

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey('term.id'))
    knowledge_area_id = db.Column(db.Integer, db.ForeignKey('knowledge_area.id'))

# if __name__ == '__main__':
#     from app import app
#
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
