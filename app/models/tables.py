# from app.secret_keys import EMAIL_PASSWORD

import base64
import os
import re
import unicodedata
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from operator import itemgetter
import datetime

from flask_login import UserMixin
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from jinja2 import Environment, PackageLoader, select_autoescape
from pymysql.err import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db


def normalize_string(query_string: str) -> str:
    normalized = unicodedata.normalize('NFD', query_string)
    return ''.join([
        char for char in normalized if not unicodedata.combining(char)
    ]).casefold()


def get_extension_from_filename(filename):
    return filename.split('.')[-1]


def get_credentials():
    creds = None
    scopes = [
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send"
    ]

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", scopes)
            creds = flow.run_local_server(port=5014)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def gmail_send_message(subject, template_filename, email):
    creds = get_credentials()

    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEMultipart()

        message["To"] = email
        message["From"] = "matemates.nao.responda@gmail.com"
        message["Subject"] = subject

        env = Environment(loader=PackageLoader("app"),
                          autoescape=select_autoescape())

        template = env.get_template(template_filename)
        html = template.render(email=email)

        html_part = MIMEText(html, "html")
        message.attach(html_part)
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        service.users().messages().send(userId="me",
                                        body=create_message).execute()

    except HttpError as error:
        raise HttpError(f'Um erro ocorreu: {error}')


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    MAX_LENGTH = {
        'name': 128,
        'first_name': 64,
        'last_name': 64,
        'email': 128,
        'username': 24,
        'password': 8,
        'password_hash': 256,
        'phone_number': 32,
        'profile_image_path': 128
    }

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(MAX_LENGTH['first_name']), nullable=False)
    last_name = db.Column(db.String(MAX_LENGTH['last_name']), nullable=False)
    email = db.Column(db.String(MAX_LENGTH['email']),
                      nullable=False,
                      unique=True)
    password_hash = db.Column(db.String(MAX_LENGTH['password_hash']),
                              nullable=False)
    username = db.Column(db.String(MAX_LENGTH['username']),
                         nullable=False,
                         unique=True)
    phone_number = db.Column(db.String(MAX_LENGTH['phone_number']))
    birth_date = db.Column(db.Date, nullable=False)
    role = db.Column(db.Enum('admin', 'normal'),
                     nullable=False,
                     default='normal')
    profile_image_path = db.Column(db.String(MAX_LENGTH['profile_image_path']),
                                   nullable=True)
    invitation_is_pending = db.Column(db.Boolean,
                                      nullable=False,
                                      default=False)

    invited_emails = db.relationship('InvitedEmail', backref='user')

    @staticmethod
    def register(form_data):
        password_hash = generate_password_hash(form_data['password'])

        first_and_last_name = User.get_first_and_last_name_from_name(
            form_data['name'])
        first_name = first_and_last_name['first_name']
        last_name = first_and_last_name['last_name']

        user = User(first_name=first_name,
                    last_name=last_name,
                    username=form_data['username'],
                    password_hash=password_hash,
                    email=form_data['email'])

        user.raise_if_form_data_is_invalid(form_data)

        if user.username == 'isq_dantas':
            user.role = 'admin'

        if form_data['phone_number']:
            user.phone_number = form_data['phone_number']

        if form_data['birth_date']:
            year, month, day = [int(x) for x in form_data['birth_date'].split('-')]
            user.birth_date = datetime.date(year, month, day)

        if user.was_invited():
            user.accept_invite_to_be_admin()

        user.register_image(form_data)

        db.session.add(user)
        db.session.commit()

    def update_user(self, form_data):
        print('started update')
        self.raise_if_form_data_is_invalid(form_data)
        print('raise success')
        first_and_last_name = User.get_first_and_last_name_from_name(
            form_data['name'])
        self.first_name = first_and_last_name['first_name']
        self.last_name = first_and_last_name['last_name']

        self.username = form_data['username']
        self.email = form_data['email']

        if form_data['phone_number']:
            self.phone_number = form_data['phone_number']
        if form_data['birth_date']:
            year, month, day = [int(x) for x in form_data['birth_date'].split('-')]
            self.birth_date = datetime.date(year, month, day)

        if form_data['image']:
            self.register_image(form_data)

        db.session.commit()

    def raise_if_form_data_is_invalid(self, form_data):
        if re.match(r'^[\w ]+$', form_data['name']) is None:
            raise ValueError('Seu nome deve conter apenas letras.')

        if len(form_data['name'].split()) != 2:
            raise ValueError(
                'Insira seu primeiro e último nome, nem mais e nem menos.')

        if re.match(r'^[\w\-_]+$', form_data['username']) is None:
            raise ValueError(
                'O nome de usuário deve conter apenas letras, números, hífens (-) ou underlines (_).'
            )

        if re.match(r'^[\w\-.]+@([\w\-]+.)+[\w\-]{2,}$',
                    form_data['email']) is None:
            raise ValueError('O e-mail informado não é válido.')

        if not self.email_has_integrity(
                form_data) and not self.username_has_integrity(form_data):
            raise IntegrityError(
                'O email e o nome de usuário já foram cadastrados.')
        elif not self.email_has_integrity(form_data):
            raise IntegrityError('Esse email já foi cadastrado.')
        elif not self.username_has_integrity(form_data):
            raise IntegrityError('Esse nome de usuário já foi cadastrado.')

    def email_has_integrity(self, form_data):
        user_with_same_email = User.query.filter_by(
            email=form_data['email']).first()
        return user_with_same_email is None or user_with_same_email == self

    def username_has_integrity(self, form_data):
        user_with_same_username = User.query.filter_by(
            username=form_data['username']).first()
        return user_with_same_username is None or user_with_same_username == self

    def register_image(self, form_data):
        image_file = form_data['image']
        if image_file.filename and image_file:
            filename = f'{self.username}.{get_extension_from_filename(image_file.filename)}'
            image_file.save(
                os.path.join('app/static/img/user_profile_picture/', filename))
            image_file.close()
            self.profile_image_path = filename
        else:
            self.profile_image_path = '$default.png'

    @staticmethod
    def get_first_and_last_name_from_name(name):
        return {'first_name': name.split()[0], 'last_name': name.split()[1]}

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get_or_404(user_id)

    def is_password_valid(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def get_dict_of_properties(self):
        return {
            'name': self.get_parsed_name(),
            'email': self.email,
            'username': self.username,
            'phone_number': self.phone_number,
            'password': 'senha errada',
            'birth_date': self.get_parsed_birth_date()
        }

    def get_parsed_name(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_parsed_birth_date(self):
        return self.birth_date.strftime('%Y-%m-%d')

    def delete_user(self):
        if self.profile_image_path:
            os.remove(
                os.path.join('app/static/img/user_profile_picture/',
                             self.profile_image_path))

        db.session.delete(self)
        db.session.commit()

    def invite(self, email):
        user_to_invite = User.get_by_email(email)

        if InvitedEmail.email_was_already_invited(email):
            raise ValueError('Esse e-mail já foi convidado.')
        if user_to_invite:
            if user_to_invite.role == 'admin':
                raise ValueError(
                    'O usuário com esse e-mail já é administrador.')
            user_to_invite.invitation_is_pending = True
        gmail_send_message('Convite para ser administrador(a) do Matematês',
                           'invite-to-be-admin.html', email)
        invited_email = InvitedEmail(email=email)
        self.invited_emails.append(invited_email)
        db.session.commit()

    def accept_invite_to_be_admin(self):
        self.invitation_is_pending = False
        self.role = 'admin'
        db.session.commit()

    def was_invited(self):
        invited_email = InvitedEmail.query.filter_by(email=self.email).first()
        return invited_email is not None or self.invitation_is_pending

    def edit_password(self, form_data):
        if self.is_password_valid(form_data['current-password']):
            print(form_data['new-password'])
            self.password_hash = generate_password_hash(
                form_data['new-password'])
            db.session.commit()
        else:
            raise ValueError('Senha incorreta.')


class InvitedEmail(db.Model):
    __tablename__ = 'invited_email'
    id = db.Column(db.Integer,
                   primary_key=True,
                   nullable=False,
                   autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    user_who_invited_id = db.Column(db.Integer,
                                    db.ForeignKey('user.id'),
                                    nullable=False)

    @staticmethod
    def email_was_already_invited(email):
        invited_email = InvitedEmail.query.filter_by(email=email).first()
        print(invited_email)
        return invited_email is not None


class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False, unique=True)
    is_validated = db.Column(db.Boolean, nullable=False, default=False)

    images = db.relationship('Image', backref='entry')
    questions = db.relationship('Question', backref='entry')
    definitions = db.relationship('Definition', backref='entry')
    terms = db.relationship('Term', backref='entry')

    @staticmethod
    def register(form_data):
        entry_content = form_data['entry_content'].casefold()

        entry = Entry(content=entry_content.replace('*', '').replace('.', ''))

        entry.raise_if_form_data_is_invalid(form_data)
        entry_content_with_dots_and_asterisks = Entry.normalize_entry_content_asterisks(
            entry_content)

        db.session.add(entry)

        entry.register_terms_and_syllables(
            entry_content_with_dots_and_asterisks, form_data)
        # entry.register_images(form_data)
        entry.register_n_attributes(form_data)

        db.session.commit()

        return entry

    def update(self, form_data: dict):
        self.raise_if_form_data_is_invalid(form_data)

        entry_content_with_dots_and_asterisks = form_data[
            'entry_content'].casefold()
        entry_content_with_dots_and_asterisks = Entry.normalize_entry_content_asterisks(
            entry_content_with_dots_and_asterisks)

        self.content = entry_content_with_dots_and_asterisks.replace(
            '*', '').replace('.', '')

        self.delete_n_properties()
        self.delete_image()

        self.register_terms_and_syllables(
            entry_content_with_dots_and_asterisks, form_data)
        self.register_images(form_data)
        self.register_n_attributes(form_data)

    def raise_if_form_data_is_invalid(self, form_data):
        entry_content = form_data['entry_content']
        if not self.has_integrity(
                entry_content.replace('*', '').replace('.', '')):
            raise IntegrityError(
                'Esse verbete já foi inserido. Tente novamente com outro.')

        if ' ' in entry_content and entry_content.count('*') != 2:
            raise ValueError(
                'Você precisa definir o termo principal, e apenas um termo principal. Ponha-o entre asteriscos (\'*\').'
            )

    @staticmethod
    def normalize_entry_content_asterisks(entry_content):
        if ' ' not in entry_content and entry_content.count('*') != 2:
            entry_content = entry_content.replace('*', '')
            entry_content = '*' + entry_content + '*'
        return entry_content

    def register_terms_and_syllables(self,
                                     entry_content_with_dots_and_asterisks,
                                     form_data):
        terms_contents = entry_content_with_dots_and_asterisks.split()
        for i, term_content in enumerate(terms_contents):
            term = Term(content=term_content.replace('.', '').replace('*', ''),
                        order=i,
                        entry=self)

            if Term.is_term_content_of_main_term(term_content):
                term.is_main_term = True
                term.gender = form_data['main_term_gender']
                term.grammatical_category = form_data[
                    'main_term_grammatical_category']

            db.session.add(term)

            syllables = term_content.split('.')
            for j, syllable in enumerate(syllables):
                syllable = Syllable(content=syllable.replace('*', ''),
                                    order=j,
                                    term=term)

                db.session.add(syllable)

    def register_images(self, form_data):
        image_file = form_data['image']
        if image_file.filename and image_file:
            filename = f'{self.get_normalized_content()}.{get_extension_from_filename(image_file.filename)}'
            image_file.save(
                os.path.join('app/static/img/entry_illustration/', filename))

            image = Image(path=filename,
                          caption=form_data['image_caption']
                          if form_data['image_caption'] else None,
                          entry=self)

            image_file.close()

            db.session.add(image)

    def register_n_attributes(self, form_data):
        n_attributes = {'definition': [], 'question': [], 'image': []}

        for key, value in form_data.items():
            if 'definition' not in key and 'question' not in key and 'image' not in key:
                continue

            key_index = Entry.get_index_from_form_data_key(key)
            key_description = Entry.get_description_from_form_data_key(key)
            key_entity_name = Entry.get_entity_name_from_form_data_key(key)

            try:
                n_attributes[key_entity_name][key_index].update(
                    {key_description: value})
            except IndexError:
                n_attributes[key_entity_name].append({
                    key_description: value,
                    'order': key_index
                })

        for definition_data in n_attributes['definition']:
            if definition_data['content'] and definition_data['knowledge_area']:
                definition = Definition(
                    content=definition_data['content'],
                    order=definition_data['order'],
                    entry=self,
                    knowledge_area=KnowledgeArea.query.filter_by(
                        content=definition_data['knowledge_area']).first())

                db.session.add(definition)
            else:
                raise ValueError('Insira as definições corretamente.')

        for question in n_attributes['question']:
            if question['statement'] and question['answer']:
                question = Question(statement=question['statement'],
                                    answer=question['answer'],
                                    order=question['order'],
                                    entry=self)

                db.session.add(question)
            elif (question['statement'] is not None) ^ (question['answer']
                                                        is not None):
                raise ValueError('Insira as questões corretamente.')

        for image in n_attributes['image']:
            image_content = image['content']
            if image_content:
                filename = f'{self.get_normalized_content()}--{image["order"]}.{get_extension_from_filename(image_content.filename)}'
                image_content.save(
                    os.path.join('app/static/img/entry_illustration/',
                                 filename))
                image_content.close()

                try:
                    image_caption = image['caption']
                except KeyError:
                    image_caption = None

                image = Image(path=filename,
                              caption=image_caption if image_caption else None,
                              order=image['order'],
                              entry=self)

                db.session.add(image)
            else:
                raise ValueError('Insira as ilustrações corretamente.')

        db.session.commit()

    def delete_entry(self):
        self.delete_n_properties()
        self.delete_image()
        db.session.delete(self)
        db.session.commit()

    def delete_n_properties(self):
        self.delete_terms()

        for entities_list in [self.definitions, self.questions]:
            for entity in entities_list:
                db.session.delete(entity)

    def delete_terms(self):
        for term in self.terms:
            for syllable in term.syllables:
                db.session.delete(syllable)
            db.session.delete(term)

    def delete_image(self):
        if self.images:
            try:
                os.remove(self.images.path)
            except FileNotFoundError:
                pass
            db.session.delete(self.images)

    def get_normalized_content(self):
        return self.content.replace(' ', '_')

    def has_integrity(self, entry_content):
        entry_with_same_content = Entry.query.filter_by(
            content=entry_content).first()
        return entry_with_same_content is None or entry_with_same_content == self

    @staticmethod
    def get_index_from_form_data_key(key: str):
        return int(key.rsplit('_', 1)[1]) - 1

    @staticmethod
    def get_description_from_form_data_key(key: str):
        return key.rsplit('_', 1)[0].split('_', 1)[1]

    @staticmethod
    def get_entity_name_from_form_data_key(key: str):
        return key.split('_', 1)[0]

    @staticmethod
    def get_by_content(content):
        content = content.replace("_", " ")
        return Entry.query.filter_by(content=content).first()

    @staticmethod
    def get_by_id(entry_id):
        return Entry.query.get(entry_id)

    @staticmethod
    def search_for_related_entries(search_sentence,
                                   gender=None,
                                   grammatical_category=None):
        related_entries = Entry.query.with_entities(Entry.id,
                                                    Entry.content).all()

        entries_and_occurrences = []

        for entry in related_entries:
            entries_and_occurrences.append({
                'entry_id': entry.id,
                'content': entry.content,
                'occurrences': 0
            })

        normalized_search_sentence = normalize_string(search_sentence)

        for search_word in normalized_search_sentence.split():
            for i, entry_and_occurrences in enumerate(entries_and_occurrences):
                normalized_entry_content = normalize_string(
                    entry_and_occurrences['content'])

                matched_strings = re.findall(rf'.*{search_word}.*',
                                             normalized_entry_content)

                if matched_strings and search_word == normalized_entry_content:
                    entries_and_occurrences[i]['occurrences'] += 3
                elif matched_strings:
                    entries_and_occurrences[i]['occurrences'] += 1

            #     print(f'{search_word} / {entry_content} => {matched_strings}')
            # print()

        entries_and_occurrences = sorted(entries_and_occurrences,
                                         key=itemgetter('content'))
        entries_and_occurrences = sorted(entries_and_occurrences,
                                         key=itemgetter('occurrences'),
                                         reverse=True)

        related_entries = []
        for entry_and_occurrences in entries_and_occurrences:
            if entry_and_occurrences['occurrences'] != 0:
                related_entries.append(
                    Entry.query.get(entry_and_occurrences['entry_id']))

        return related_entries

    def get_definition_with_knowledge_area(self, knowledge_area):
        return Definition.query.filter_by(knowledge_area=knowledge_area,
                                          entry=self).first()

    def get_main_term(self):
        return Term.query.filter_by(entry=self, is_main_term=True).first()

    def get_dict_of_properties(self):
        n_properties = {}

        for i, question in enumerate(self.questions):
            n_properties.update({
                f'question_statement_{i + 1}': question.statement,
                f'question_answer_{i + 1}': question.answer
            })

        for i, definition in enumerate(self.definitions):
            n_properties.update({
                f'definition_content_{i + 1}':
                definition.content,
                f'definition_knowledge_area_{i + 1}':
                definition.knowledge_area.content
            })

        entry_content_with_dots_and_asterisks = ''
        for i, term in enumerate(self.terms):
            if i != 0:
                entry_content_with_dots_and_asterisks += ' '
            if term.is_main_term:
                entry_content_with_dots_and_asterisks += '*'
            for j, syllable in enumerate(term.syllables):
                if j != 0:
                    entry_content_with_dots_and_asterisks += '.'
                entry_content_with_dots_and_asterisks += syllable.content
            if term.is_main_term:
                entry_content_with_dots_and_asterisks += '*'

        fixed_properties = {
            'entry_content': entry_content_with_dots_and_asterisks,
            'main_term_grammatical_category':
            self.get_main_term().grammatical_category,
            'main_term_gender': self.get_main_term().gender
        }

        return {
            'n_properties': n_properties,
            'fixed_properties': fixed_properties
        }

    def turn_valid(self):
        self.is_validated = True
        db.session.commit()

    def get_term_by_content(self, term_content):
        return Term.query.filter_by(entry=self, content=term_content).first()


class Term(db.Model):
    __tablename__ = 'term'

    MAX_LENGTH = {'content': 256}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False, unique=True)
    gender = db.Column(db.Enum('M', 'F'), nullable=True)
    grammatical_category = db.Column(db.Enum('substantivo', 'verbo',
                                             'adjetivo', 'numeral'),
                                     nullable=True)
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

    @staticmethod
    def is_term_content_of_main_term(term_content):
        return term_content[0] == '*' and term_content[-1] == '*'

    def get_parsed_syllables(self):
        syllables_contents = [syllable.content for syllable in self.syllables]
        return '.'.join(syllables_contents)


class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(256), nullable=False)
    caption = db.Column(db.String(256), nullable=True)
    order = db.Column(db.Integer, nullable=False)
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
        contents = KnowledgeArea.query.with_entities(
            KnowledgeArea.content).order_by(KnowledgeArea.content).all()

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
        return list(related_entries)

    def get_related_and_validated_entries(self):
        related_definitions = self.definitions
        related_entries = set()
        for definition in related_definitions:
            if definition.entry.is_validated:
                related_entries.add(definition.entry)
        return list(related_entries)

    @staticmethod
    def register(content, subject):
        knowledge_area = KnowledgeArea(content=content, subject=subject)
        db.session.add(knowledge_area)
        db.session.commit()


class Definition(db.Model):
    __tablename__ = 'definition'

    MAX_LENGTH = {'content': 256}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(MAX_LENGTH['content']), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'))
    knowledge_area_id = db.Column(db.Integer,
                                  db.ForeignKey('knowledge_area.id'))


# if __name__ == '__main__':
#     from app import app
#
#     with app.app_context():
#         db.drop_all()
#         db.create_all()
