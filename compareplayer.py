from logging import PlaceHolder
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

class compare(FlaskForm):
    name1 = StringField("Enter Name of 1st Player", validators=[DataRequired()], render_kw={"placeholder": "Enter player name"})
    name2 = StringField(render_kw={"placeholder" : "Enter name of 2nd Player"}, validators=[DataRequired()])
    submit = SubmitField("Look Up!")
