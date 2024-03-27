from flask_login import UserMixin
from app.models import db
from pymysql.err import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import unicodedata
from operator import itemgetter
import re
import os
from pymysql.err import IntegrityError


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
    def register(form_data):
        print(form_data)
        password_hash = generate_password_hash(form_data['password'])

        new_user = User(
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            username=form_data['username'],
            password_hash=password_hash,
            email=form_data['email'],
            phone_number=form_data['phone_number'],
            birth_date=form_data['birth_date']
        )

        new_user.role = 'admin'

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


class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False, unique=True)
    is_validated = db.Column(db.Boolean, nullable=False, default=False)

    image = db.relationship('Image', backref='entry', uselist=False)
    questions = db.relationship('Question', backref='entry')
    definitions = db.relationship('Definition', backref='entry')
    terms = db.relationship('Term', backref='entry')

    @staticmethod
    def register(form_data):
        entry_content = form_data['entry_content'].casefold()

        entry = Entry(
            content=entry_content.replace('*', '').replace('.', '')
        )

        if not entry.has_integrity():
            raise IntegrityError('Esse verbete já foi inserido. Tente novamente com outro.')

        if ' ' in entry_content and entry_content.count('*') != 2:
            raise ValueError(
                'Você precisa definir o termo principal, e apenas um termo principal. Ponha-o entre asteriscos (\'*\').')
        elif ' ' not in entry_content and entry_content.count('*') != 2:
            entry_content = entry_content.replace('*', '')
            entry_content = '*' + entry_content + '*'

        db.session.add(entry)

        terms_contents = entry_content.split()
        for i, term_content in enumerate(terms_contents):
            term = Term(
                content=term_content.replace('.', '').replace('*', ''),
                order=i,
                entry=entry
            )

            if term_content[0] == '*' and term_content[-1] == '*':
                term.is_main_term = True
                term.gender = form_data['main_term_gender']
                term.grammatical_category = form_data['main_term_grammatical_category']

            db.session.add(term)

            syllables = term_content.split('.')
            for j, syllable in enumerate(syllables):
                syllable = Syllable(
                    content=syllable.replace('*', ''),
                    order=j,
                    term=term
                )

                db.session.add(syllable)

        image_file = form_data['image']
        if image_file.filename and image_file:
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join('app/static/img/entry_illustration/', filename))

            image = Image(
                path=filename,
                caption=form_data['image_caption'] if form_data['image_caption'] else None,
                entry=entry
            )

            image_file.close()

            db.session.add(image)

        n_attributes = {
            'definition': [],
            'question': []
        }

        for key, value in form_data.items():
            if 'definition' not in key and 'question' not in key:
                continue

            key_index = Entry.get_index_from_key(key)
            key_description = Entry.get_description_from_key(key)
            key_entity_name = Entry.get_entity_name_from_key(key)

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
                    order=definition_data['order'],
                    entry=entry,
                    knowledge_area=KnowledgeArea.query.filter_by(content=definition_data['knowledge_area']).first()
                )

                db.session.add(definition)

        for question in n_attributes['question']:
            if question['statement'] and question['answer']:
                question = Question(
                    statement=question['statement'],
                    answer=question['answer'],
                    order=question['order'],
                    entry=entry
                )

                db.session.add(question)

        db.session.commit()

        return entry

    def delete_entry(self):
        for term in self.terms:
            for syllable in term.syllables:
                db.session.delete(syllable)
            db.session.delete(term)

        for entities_list in [self.definitions, self.questions]:
            for entity in entities_list:
                db.session.delete(entity)

        if self.image:
            try:
                os.remove(self.image.path)
            except FileNotFoundError:
                pass
            db.session.delete(self.image)

        db.session.delete(self)
        db.session.commit()

    def has_integrity(self):
        entry_with_same_content = Entry.query.filter_by(content=self.content).first()
        return entry_with_same_content is None

    @staticmethod
    def get_index_from_key(key: str):
        return int(key.rsplit('_', 1)[1]) - 1

    @staticmethod
    def get_description_from_key(key: str):
        return key.rsplit('_', 1)[0].split('_', 1)[1]

    @staticmethod
    def get_entity_name_from_key(key: str):
        return key.split('_', 1)[0]

    @staticmethod
    def get_entry_by_content(content):
        return Entry.query.filter_by(content=content).first()

    @staticmethod
    def search_for_related_entries(search_sentence, gender=None, grammatical_category=None):
        related_entries = Entry.query.with_entities(Entry.id, Entry.content).all()

        entries_and_occurrences = []

        for entry in related_entries:
            entries_and_occurrences.append(
                {'entry_id': entry.id, 'content': entry.content, 'occurrences': 0}
            )

        normalized_search_sentence = normalize_string(search_sentence)

        for search_word in normalized_search_sentence.split():
            for i, entry_and_occurrences in enumerate(entries_and_occurrences):
                normalized_entry_content = normalize_string(entry_and_occurrences['content'])

                matched_strings = re.findall(rf'.*{search_word}.*', normalized_entry_content)

                if matched_strings and search_word == normalized_entry_content:
                    entries_and_occurrences[i]['occurrences'] += 3
                elif matched_strings:
                    entries_and_occurrences[i]['occurrences'] += 1

            #     print(f'{search_word} / {entry_content} => {matched_strings}')
            # print()

        entries_and_occurrences = sorted(entries_and_occurrences, key=itemgetter('content'))
        entries_and_occurrences = sorted(entries_and_occurrences, key=itemgetter('occurrences'), reverse=True)

        related_entries = []
        for entry_and_occurrences in entries_and_occurrences:
            if entry_and_occurrences['occurrences'] != 0:
                related_entries.append(
                    Entry.query.get(entry_and_occurrences['entry_id'])
                )

        return related_entries

    def get_definition_with_knowledge_area(self, knowledge_area):
        return Definition.query.filter_by(knowledge_area=knowledge_area, entry=self).first()

    def get_main_term(self):
        return Term.query.filter_by(entry=self, is_main_term=True).first()

    def turn_valid(self):
        self.is_validated = True
        db.session.commit()


class Term(db.Model):
    __tablename__ = 'term'

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False, unique=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    grammatical_category = db.Column(
        db.Enum('substantivo', 'verbo', 'adjetivo', 'numeral'), nullable=True
    )
    is_main_term = db.Column(db.Boolean, nullable=False, default=False)
    order = db.Column(db.Integer, nullable=False)

    syllables = db.relationship('Syllable', backref='term')
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))

    def get_gender_in_full(self):
        return Term.abbreviation_to_gender_in_full(self.gender)

    @staticmethod
    def abbreviation_to_gender_in_full(abbreviation):
        gender_in_full = {
            'M': 'masculino',
            'F': 'feminino',
        }

        return gender_in_full[abbreviation]


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.String(256), nullable=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statement = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    explanation = db.Column(db.String(256), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))


class Syllable(db.Model):
    __tablename__ = 'syllable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(12), nullable=False)
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

    @staticmethod
    def get_all():
        return KnowledgeArea.query.all()

    def get_related_entries(self):
        related_definitions = self.definitions
        related_entries = set()
        for definition in related_definitions:
            related_entries.add(definition.entry)
        return related_entries

    @staticmethod
    def register(content, subject):
        knowledge_area = KnowledgeArea(
            content=content,
            subject=subject
        )
        db.session.add(knowledge_area)
        db.session.commit()


class Definition(db.Model):
    __tablename__ = 'definition'

    MAX_LENGTH = {
        'content': 256
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    knowledge_area_id = db.Column(db.Integer, db.ForeignKey('knowledge_area.id'))

# if __name__ == '__main__':
#     from app import app
#
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
