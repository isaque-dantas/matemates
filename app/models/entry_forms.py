from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length

from app.models.tables import Term, Definition, KnowledgeArea
from app import app


class EntryCreationForm(FlaskForm):
    entry_content = StringField('Conteúdo',
                               validators=[
                                   DataRequired(),
                                   Length(max=Term.MAX_LENGTH['content'])
                               ])

    main_term_grammatical_category = SelectField('Classe gramatical',
                                                 choices=[
                                                     ('', 'Classe'),
                                                     ('substantivo', 'Substantivo'),
                                                     ('verbo', 'Verbo'),
                                                     ('adjetivo', 'Adjetivo'),
                                                     ('numeral', 'Numeral'),
                                                 ],
                                                 validators=[DataRequired()])

    main_term_gender = SelectField('Classe gramatical',
                                   choices=[
                                       ('', 'Gênero'),
                                       ('M', Term.abbreviation_to_gender_in_full('M').capitalize()),
                                       ('F', Term.abbreviation_to_gender_in_full('F').capitalize())
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
                *KnowledgeArea.get_term_creation_form_definitions_choices()
            ])

    question_statement_1 = StringField('Enunciado')

    question_answer_1 = StringField('Resposta')

    image = FileField('Imagem', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos \'jpg\', \'png\' ou \'jpeg\' são permitidos.'),
    ])

    image_caption = StringField()

    submit = SubmitField('Confirmar')
