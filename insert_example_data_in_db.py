from app import app
from app.models.tables import Entry, KnowledgeArea, User
from app.models import db
from werkzeug.datastructures import FileMultiDict
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    dados_usuario_admin = {
        'username': 'isq_dantas',
        'first_name': 'Isaque',
        'last_name': 'Dantas',
        'password': '12345',
        'email': 'isaque@gmail.com',
        'phone_number': '1234567890',
        'birth_date': date(2007, 3, 14),
        'role': 'admin'
    }

    User.register(dados_usuario_admin)

    knowledge_areas = [
        {'content': 'álgebra', 'subject': 'matemática'},
        {'content': 'geometria', 'subject': 'matemática'},
        {'content': 'trigonometria', 'subject': 'matemática'},
        {'content': 'matemática discreta', 'subject': 'matemática'},
        {'content': 'estatística e probabilidade', 'subject': 'matemática'},
        {'content': 'cálculo', 'subject': 'matemática'},
    ]

    for knowledge_area in knowledge_areas:
        KnowledgeArea.register(knowledge_area['content'], knowledge_area['subject'])

    dados_angulo_reto = {
        'entry_content': '*Ân.gu.lo* re.to',
        'main_term_grammatical_category': 'substantivo',
        'main_term_gender': 'M',
        'definition_content_1': 'Ângulo com valor de 90°.',
        'definition_knowledge_area_1': 'geometria',
        'definition_content_2': 'Classificação dos ângulos de quadrados e retângulos.',
        'definition_knowledge_area_2': 'geometria',
        'question_statement_1': 'O que é um ângulo reto?',
        'question_answer_1': 'batata',
        'image_caption': ''
    }

    files = FileMultiDict()
    files.add_file('image', r'app/static/img/entry_illustration/alfa.png')

    dados_angulo_reto.update(dict(files))

    Entry.register(dados_angulo_reto)

    dados_calculadora = {
        'entry_content': '*cal.cu.la.do.ra*',
        'main_term_grammatical_category': 'substantivo',
        'main_term_gender': 'F',
        'definition_content_1': 'Dispositivo eletrônico usado para facilitar cálculos matemáticos.',
        'definition_knowledge_area_1': 'álgebra',
        'image_caption': ''
    }

    files = FileMultiDict()
    files.add_file('image', r'app/static/img/entry_illustration/calculadora.jpg')

    dados_calculadora.update(dict(files))

    Entry.register(dados_calculadora)
