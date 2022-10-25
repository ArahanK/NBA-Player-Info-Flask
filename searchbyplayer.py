from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

class search(FlaskForm):
    name = StringField("Enter Name", validators=[DataRequired()])
    submit = SubmitField("Look Up!")
