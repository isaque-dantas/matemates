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

    # isaque = User(
    #     first_name='Isaque',
    #     last_name='Dantas',
    #     username='isaque-dantas',
    #     password_hash=generate_password_hash('123456'),
    #     email='isaque@email.com',
    #     phone_number='912344321',
    #     birth_date=date(year=2007, month=3, day=14),
    #     role='normal'
    # )
    #
    # db.session.add(isaque)
    #
    # cos = Term(
    #     content='cosseno',
    #     gender='M',
    #     grammatical_category='substantivo'
    # )
    #
    # cos_definition = Definition(
    #     content='Razão entre o cateto adjacente e a hipotenusa de determinado ângulo em um triângulo retângulo.',
    #     order=0
    # )
    #
    # cos_image = Image(path='alfa.png', term=cos)
    #
    # trigonometry = KnowledgeArea(content='trigonometria', subject='matemática')
    # geometry = KnowledgeArea(content='geometria', subject='matemática')
    #
    # cos_definition.knowledge_area = trigonometry
    # cos.definitions.append(cos_definition)
    #
    # db.session.add_all([
    #     Syllable(content='cos', order=0, term=cos),
    #     Syllable(content='se', order=1, term=cos),
    #     Syllable(content='no', order=2, term=cos),
    #     cos, cos_definition, cos_image, geometry, trigonometry,
    #     KnowledgeArea(content='álgebra', subject='matemática'),
    #     KnowledgeArea(content='cálculo', subject='matemática'),
    #     KnowledgeArea(content='estatística e probabilidade', subject='matemática'),
    #     KnowledgeArea(content='matemática discreta', subject='matemática')
    # ])
    #
    # calculator = Term(
    #     content='calculadora',
    #     gender='F',
    #     grammatical_category='substantivo'
    # )
    #
    # calculator_definition = Definition(
    #     content='Aparelho eletrônico usado para fazer cálculos matemáticos.',
    #     order=0
    # )
    #
    # calculator_image = Image(path='alfa.png', term=calculator)
    # calculator.definitions.append(calculator_definition)
    #
    # db.session.add_all([
    #     Syllable(content='cal', order=0, term=calculator),
    #     Syllable(content='cu', order=1, term=calculator),
    #     Syllable(content='la', order=2, term=calculator),
    #     Syllable(content='do', order=3, term=calculator),
    #     Syllable(content='ra', order=4, term=calculator),
    #     calculator, calculator_definition, calculator_image
    # ])
    #
    # db.session.commit()
