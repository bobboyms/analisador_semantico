from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class FormularioPrincipal(FlaskForm): 
    palavra_chave = StringField("palavra_chave", validators=[DataRequired()])
