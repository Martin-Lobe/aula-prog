from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms import FileField, PasswordField, SelectField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError
from flask_wtf.file import FileRequired, FileAllowed

class InputIntegerSize(object):
    def __init__(self, min=-1, max=-1, message=None):
        assert min != -1 or max != -1, 'At least one of `min` or `max` must be specified.'
        assert max == -1 or min <= max, '`min` cannot be more than `max`.'
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        l = str(field.data) and len(str(field.data)) or 0
        if l < self.min or self.max != -1 and l > self.max:
            message = self.message
            if message is None:
                if self.max == -1:
                    message = field.ngettext('O campo deve ter no mínimo %(min)d números.',
                                             'O campo deve ter no mínimo %(min)d números.', self.min)
                elif self.min == -1:
                    message = field.ngettext('O campo deve ter no máximo %(max)d números.',
                                             'O campo deve ter no máximo %(max)d números.', self.max)
                else:
                    message = field.gettext('O campo deve ter entre %(min)d e %(max)d números.')

            raise ValidationError(message % dict(min=self.min, max=self.max, length=l))


class AnotacaoForm(FlaskForm):
    """Classe criada para representar o form de uma anotacão.
    Form pode ser traduzido como documentos com espaços em branco a serem
    preenchidos. Desta forma, classe AnotacaoForm gera um objeto que irá
    ajudar-nos a capitura os dados da anotações.
    """

    """
        Os campos da tela vão ser representados por Classes que terminam com
        Field, devem ser importandos de wtforms. São exemplos de campos da
        tela: RadioField, StringField, TextAreaField, SubmitField, FileField,
        IntegerField, DecimalField, FloatField, BooleanField, SubmitInput,
        FieldList, DateTimeField e etc. Ao criar os objetos do wtforms alguns
        parâmetros podem ser definidos:
            label – representa o texto que descreve o conteúdo do campo.
            validators – Lista de validadores que irão validar o campo.
            description – Descrição do campus, utilizado como ajuda.

        Os validators deve ser importados de wtforms.validators e podem ser:
            DataRequired
            InputRequired
            Email
            IPAddress
            Length
            NumberRange
            URL
        OBS: De acordo com a documentação do wtforms devemos utilizar
        InputRequired no lugar de DataRequired. DataRequired deve ser
        utlizado se você tiver certeza do que está fazendo.
    """

    titulo = StringField("Título", validators=[InputRequired(message="Campo obrigatório!")],
                         description="Deve ser único.")
    texto = TextAreaField("Texto", validators=[InputRequired()])
    data = DateField("Data", validators=[InputRequired()])
    submit = SubmitField("Salvar")


class UsuarioLogarForm(FlaskForm):
    """Classe criada para representar o form de login de um usuário."""
    #Os campos da tela podem ter um parâmetro Length para determiar tamanho
    nome = StringField("Nome do usuário", validators=[
                                            InputRequired(message="Não esqueça de preencher esse campo!"),
                                            Length(min=4, max=10,
                                                   message="Todo nome deve ter no mínimo 4 e máximo 10 caracteres")])
    senha = PasswordField("Senha", validators=[InputRequired(message="Não esqueça de preencher esse campo!")])
    submit = SubmitField("Logar")

class CadastroUsuarioForm(FlaskForm):
    """Classe criada para representar o form de cadastro de um usuário."""
    cpf = IntegerField("CPF", validators=[InputRequired(message="Não esqueça de preencher esse campo!"), InputIntegerSize(min=11, max=11)])
    email = StringField("E-mail", validators=[Email(message="E-mail inválido!"), InputRequired(message="Não esqueça de preencher esse campo!")])
    nome = StringField("Nome do usuário", validators=[InputRequired(message="Não esqueça de preencher esse campo!")])
    senha = PasswordField("Senha", validators=[InputRequired(message="Não esqueça de preencher esse campo!")])
    senha2 = PasswordField("Senha",
                           validators=[InputRequired(),
                                       EqualTo("senha",
                                       message="As senhas devem ser iguais.")])
    foto = FileField('Imagem', validators=[FileRequired(message="Arquivo requerido!"),
                                           FileAllowed(['jpg', 'png'],
                                           message='Somente imagens!')])
    submit = SubmitField("Cadastrar")

class ListaAnotacoes(FlaskForm):
    lista = SelectField("Anotações")
    submit = SubmitField("Carregar")

class AtualizarAnotacaoForm(FlaskForm):
    id = HiddenField("id")
    titulo = StringField("Título", validators=[InputRequired(message="Campo obrigatório!")],
                         description="Deve ser único.")
    texto = TextAreaField("Texto", validators=[InputRequired(message="Campo obrigatório!")])
    data = DateField("Data", validators=[InputRequired(message="Campo obrigatório!")])
    submit = SubmitField("Atualizar")
