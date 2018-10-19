from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired

class FormularioTexto(FlaskForm): 
    texto = StringField("texto")
