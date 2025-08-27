from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepinterest.models import User


class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit_button = SubmitField("Fazer login")


class FormRegister(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    password_confirmation = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo("password")])
    submit_button = SubmitField("Fazer o cadastro")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            return ValidationError("Email já cadastrado. Faça login para continuar")


class FormPost(FlaskForm):
    photo = FileField("Foto", validators=[DataRequired()])
    submit_button = SubmitField("Enviar")
    