from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from progetto.models import User
from progetto import db

class InsuranceForm(FlaskForm):
    eta = IntegerField('Età', validators=[DataRequired(), NumberRange(min=18, max=100)])
    cilindrata = IntegerField('Cilindrata', validators=[DataRequired(), NumberRange(min=1000, max=5000)])
    sinistri = IntegerField('Sinistri', validators=[NumberRange(min=0, max=18, message="I sinistri devono essere tra 0 e 10.")])
    chilometri = IntegerField('Chilometri percorsi', validators=[DataRequired(), NumberRange(min=0, max=200000)])
    classe_merito = IntegerField('Classe merito', validators=[DataRequired(), NumberRange(min=1, max=18, message="La classe merito deve essere tra 1 e 18.")])
    submit = SubmitField('Calcola')

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrati')

    def validate_email(self, email):
        user = db.users.find_one({"email": email.data})
        if user:
            raise ValidationError('Questa email è già utilizzata. Scegliere una diversa.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Ricordami')
    submit = SubmitField('Login')

# Modifica account
class UpdateAccountForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=20)])
    cognome = StringField('Cognome', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Modifica')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = db.users.find_one({"email": email.data})
            if user:
                raise ValidationError('Email già esistente, sceglierne una diversa')

   
          