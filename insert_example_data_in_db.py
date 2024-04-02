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

    files = FileMultiDict()
    files.add_file('image', r'isq_dantas.png')

    dados_usuario_admin.update(dict(files))

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
    files.add_file('image', r'angulo_reto.jpeg')

    dados_angulo_reto.update(dict(files))

    Entry.register(dados_angulo_reto)

    dados_calculadora = {
        'entry_content': 'cal.cu.la.do.ra',
        'main_term_grammatical_category': 'substantivo',
        'main_term_gender': 'F',
        'definition_content_1': 'Dispositivo eletrônico usado para facilitar cálculos matemáticos.',
        'definition_knowledge_area_1': 'álgebra',
        'image_caption': ''
    }

    files = FileMultiDict()
    files.add_file('image', r'calculadora.jpg')

    dados_calculadora.update(dict(files))

    Entry.register(dados_calculadora)

    dados_rafael = {
        'entry_content': 'ra.fa.el',
        'main_term_grammatical_category': 'substantivo',
        'main_term_gender': 'M',
        'definition_content_1': 'Mega rafa',
        'definition_knowledge_area_1': 'álgebra',
        'definition_content_2': 'The teacher',
        'definition_knowledge_area_2': 'estatística e probabilidade',
        'definition_content_3': 'The teacher',
        'definition_knowledge_area_3': 'estatística e probabilidade',
        'definition_content_4': 'The teacher',
        'definition_knowledge_area_4': 'estatística e probabilidade',
        'definition_content_5': 'The teacher',
        'definition_knowledge_area_5': 'estatística e probabilidade',
        'image_caption': ''
    }

    files = FileMultiDict()
    files.add_file('image', r'calculadora.jpg')

    dados_rafael.update(dict(files))

    Entry.register(dados_rafael)
