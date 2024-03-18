from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length

from app.models.tables import Term, Definition, KnowledgeArea
from app import app


class TermCreationForm(FlaskForm):
    content = StringField('Conteúdo',
                          validators=[
                              DataRequired(),
                              Length(max=Term.MAX_LENGTH['content'])
                          ])

    definition_content_1 = StringField('Definição #1',
                                       validators=[
                                           DataRequired(),
                                           Length(max=Definition.MAX_LENGTH['content'])
                                       ])
    with app.app_context():
        definition_knowledge_area_1 = SelectField(
            'Área do conhecimento',
            choices=[
                ('', 'Selecione uma opção'),
                ('álgebra', 'Álgebra'),
                ('cálculo', 'Cálculo'),
                ('estatística e probabilidade', 'Estatística e probabilidade'),
                ('trigonometria', 'Trigonometria'),
                ('matemática discreta', 'Matemática discreta'),
                *KnowledgeArea.get_term_creation_form_definitions_choices()
            ])

    question_statement_1 = StringField('Enunciado')

    question_answer_1 = StringField('Resposta')

    grammatical_category = SelectField('Classe gramatical',
                                       choices=[
                                           ('', 'Classe'),
                                           ('substantivo', 'Substantivo'),
                                           ('verbo', 'Verbo'),
                                           ('adjetivo', 'Adjetivo'),
                                           ('numeral', 'Numeral'),
                                       ],
                                       validators=[DataRequired()])

    gender = SelectField('Classe gramatical',
                         choices=[
                             ('', 'Gênero'),
                             ('M', Term.abbreviation_to_gender_in_full('M').capitalize()),
                             ('F', Term.abbreviation_to_gender_in_full('F').capitalize())
                         ])

    image_path = FileField('Imagem', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos \'jpg\' \'png\' \'jpeg\' são permitidos'),
        DataRequired()
    ])

    image_caption = StringField()

    submit = SubmitField('Confirmar')
