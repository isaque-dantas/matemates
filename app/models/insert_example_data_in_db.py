from app import app
from app.models.tables import User, Term, Definition, Image, KnowledgeArea, Syllable
from app.models import db
from werkzeug.security import generate_password_hash
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    isaque = User(
        first_name='Isaque',
        last_name='Dantas',
        username='isaque-dantas',
        password_hash=generate_password_hash('123456'),
        email='isaque@email.com',
        phone_number='912344321',
        birth_date=date(year=2007, month=3, day=14),
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

    cos_image = Image(path='alfa.png', term=cos)

    trigonometry = KnowledgeArea(content='trigonometria', subject='mathematics')
    geometry = KnowledgeArea(content='geometria', subject='mathematics')

    cos_definition.knowledge_areas.append(trigonometry)
    cos_definition.knowledge_areas.append(geometry)
    cos.definitions.append(cos_definition)

    db.session.add_all([
        Syllable(content='cos', order=0, term=cos),
        Syllable(content='se', order=1, term=cos),
        Syllable(content='no', order=2, term=cos),
        cos, cos_definition, cos_image, geometry, trigonometry
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

    calculator_image = Image(path='alfa.png', term=calculator)
    calculator.definitions.append(calculator_definition)

    db.session.add_all([
        Syllable(content='cal', order=0, term=calculator),
        Syllable(content='cu', order=1, term=calculator),
        Syllable(content='la', order=2, term=calculator),
        Syllable(content='do', order=3, term=calculator),
        Syllable(content='ra', order=4, term=calculator),
        calculator, calculator_definition, calculator_image
    ])

    db.session.commit()
