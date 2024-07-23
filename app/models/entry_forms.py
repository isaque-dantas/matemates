from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length

from app.models.tables import TermRepository, Definition, KnowledgeArea
from app import app


class EntryCreationForm(FlaskForm):
    entry_content = StringField('Conteúdo',
                                validators=[
                                    DataRequired(),
                                    Length(max=TermRepository.MAX_LENGTH['content'])
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
                                       ('M', TermRepository.abbreviation_to_gender_in_full('M').capitalize()),
                                       ('F', TermRepository.abbreviation_to_gender_in_full('F').capitalize())
                                   ])

    definition_content_1 = TextAreaField('Definição #1',
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

    image_content_1 = FileField('Imagem', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos \'jpg\', \'png\' ou \'jpeg\' são permitidos.'),
    ])

    image_caption_1 = TextAreaField('Legenda da imagem')

    submit = SubmitField('Confirmar')
