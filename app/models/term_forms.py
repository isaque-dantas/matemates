from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length

from app.models.tables import Term, Definition


class TermCreationForm(FlaskForm):
    title = StringField('Título',
                        validators=[
                            DataRequired(),
                            Length(max=Term.MAX_LENGTH['title'])
                        ])

    content = StringField('Conteúdo',
                          validators=[
                              DataRequired(),
                              Length(max=Term.MAX_LENGTH['content'])
                          ])

    definition_content = StringField('Definição #1',
                                     validators=[
                                         DataRequired(),
                                         Length(max=Definition.MAX_LENGTH['content'])
                                     ])

    definition_math_related_area = SelectField('Área da matemática',
                                               choices=[
                                                   ('álgebra', 'Álgebra'),
                                                   ('cálculo', 'Cálculo'),
                                                   ('estatística e probabilidade', 'Estatística e probabilidade'),
                                                   ('trigonometria', 'Trigonometria'),
                                                   ('teoria dos números', 'Estatística e probabilidade'),
                                                   ('estatística e probabilidade', 'matemática discreta')
                                               ])

    grammatical_category = SelectField('Classe gramatical',
                                       choices=[
                                           ('substantivo', 'Substantivo'),
                                           ('verbo', 'Verbo'),
                                           ('adjetivo', 'Adjetivo'),
                                           ('numeral', 'Numeral'),
                                       ],
                                       validators=[DataRequired()])

    gender = SelectField('Classe gramatical',
                         choices=[
                             ('M', Term.abbreviation_to_gender_in_full('M')),
                             ('F', Term.abbreviation_to_gender_in_full('F'))
                         ])

    image = FileField('Imagem', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas arquivos \'jpg\' \'png\' \'jpeg\' são permitidos')
    ])

    submit = SubmitField('Confirmar')
