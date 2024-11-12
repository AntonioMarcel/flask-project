from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired,
    Length,
    Regexp,
    ValidationError,
)

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = db.session.scalar(select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")


class RegistrarNotasFiscaisForm(FlaskForm):
    processo_sei = StringField("Processo SEI", validators=[DataRequired()])
    doc_sei_nf = StringField("Doc. SEI NF", validators=[DataRequired()])
    doc_sei_ateste = StringField("Doc. SEI Ateste", validators=[DataRequired()])
    doc_sei_conformidade = StringField("Doc. SEI Conformidade", validators=[DataRequired()])
    numero_nf = StringField("Número da Nota Fiscal", validators=[DataRequired()])
    data_emissao = DateField("Data de emissão", validators=[DataRequired()])
    data_entrada = DateField("Data de entrada", validators=[DataRequired()])
    data_vencimento = DateField("Data de vencimento", validators=[DataRequired()])
    data_inicio_competencia = DateField("Início competência", validators=[DataRequired()])
    data_fim_competencia = DateField("Fim competência", validators=[DataRequired()])
    masp = StringField("MASP Ordenador", validators=[DataRequired()])
    nome_ordenador = StringField("Nome do Ordenador", render_kw={"readonly": True})
    observacoes = TextAreaField("Observações")
    municipio = StringField("Município", validators=[DataRequired()])
    valor_nf = StringField("Valor da Nota Fiscal", validators=[DataRequired()])
    ue = StringField("Unidade Executora", validators=[DataRequired()])
    ano = StringField("Ano", validators=[DataRequired()])
    empenho = StringField("No. Empenho", validators=[DataRequired()])
    gmi_fp = StringField("GMI FP", render_kw={"readonly": True})
    nome_credor = StringField("Nome Credor", render_kw={"readonly": True})
    cnpj_cpf_credor = StringField("CNPJ/CPF Credor", render_kw={"readonly": True})

    conformidade = StringField("Conformidade", validators=[DataRequired()])
    status = SelectField(
        "Status",
        choices=[
            ("", "Selecione o status"),
            ("ok", "OK"),
            ("devolvido", "DEVOLVIDO"),
        ],
        validators=[DataRequired()]
    )

    banco = StringField("Banco", validators=[DataRequired()])
    agencia = StringField("Agencia", validators=[DataRequired()])
    conta = StringField("Conta", validators=[DataRequired()])

    submit = SubmitField("Enviar")


# validate as soon as user is typing > processo sei, campos de valor monetário: javascript?
# campo municipio: lista suspensa com municipios

# possible validations:
# formato processo sei
# Regexp(
#     r"^\d{4}\.\d{2}\.\d{7}/\d{4}-\d{2}$",
#     message="O campo deve seguir o formato: 1500.01.0023123/2024-08.",
# ),
# field length: Length(min=8, max=8, message="O campo deve ter exatamente 8 números."),
# only numbers
