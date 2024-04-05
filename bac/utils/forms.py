from flask_wtf import FlaskForm
from wtforms import (
    EmailField, PasswordField, StringField,BooleanField,SelectField,IntegerField
)
from wtforms.validators import DataRequired,Email,EqualTo, Length

from bac.plugins.models import User

class LoginForm(FlaskForm):
    
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Mot de passe", validators=[DataRequired(), Length(min=3, max=25)]
    )
    remember = BooleanField("Se souvenir de moi")

JOB_CHOICES = [(1,'Etudiant.e'),(2,'Technicien.ne'),(3,'Biologiste'),(4,'Interne'),(5,'Admin'),(6,'Autre')]

class RegisterForm(FlaskForm):

    firstname = StringField(
        "Prénom",validators=[DataRequired()]
    )
    name = StringField(
        "Nom",validators=[DataRequired()]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    job = SelectField(
        "Métier",choices=JOB_CHOICES,
    )
    password = PasswordField(
        "Mot de passe", validators=[DataRequired(), Length(min=3, max=25)]
    )
    confirm = PasswordField(
        "Confirmez le mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password", message="Les mots de passe doivent être identiques."),
        ],
    )

    def validate(self,extra_validators=None):
        initial_validation = super(RegisterForm, self).validate(extra_validators)
        if not initial_validation:
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords must match")
            return False
        return True


class SettingsForm(FlaskForm):

    nquestions = IntegerField(
        'Nombre de questions',
    )

    clock = BooleanField('Chronomètre')

    clock_time = IntegerField()

    history = BooleanField('Revenir sur les erreurs passées')

    multiple_choice = BooleanField('Réponses multiples')

    dropdown_menu = BooleanField('Menus déroulants')

    open_question = BooleanField('Questions ouverte')

    antibiogram = BooleanField('Antibiogrammes')

    direct_exam = BooleanField('Examens directs')

    culture = BooleanField('Cultures')