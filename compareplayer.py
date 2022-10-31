from logging import PlaceHolder
from wsgiref import validate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

class compare(FlaskForm):
    name1 = StringField("Enter Name of 1st Player", validators=[DataRequired()], render_kw={"placeholder": "Enter player name"})
    name2 = StringField(render_kw={"placeholder" : "Enter name of 2nd Player"}, validators=[DataRequired()])
    fgmfan = StringField("Enter points per FGM", validators=[DataRequired()], render_kw={"placeholder": "Enter Points per FGM"})
    fgafan = StringField("Enter points deducted per FGA", validators=[DataRequired()], render_kw={"placeholder": "Enter Points Deducted per FGA"})
    tovfan = StringField("Enter points deducted per TOV", render_kw={"placeholder": "Enter points deducted per TOV"})
    rebfan = StringField("Enter points per Rebound", render_kw={"placeholder": "Enter Points per Rebound"})
    astfan = StringField("Enter points per assist", render_kw={"placeholder": "Enter Points per Assist"})
    pointsfan = StringField("Enter Points per point scored", validators=[DataRequired()], render_kw={"placeholder": "Enter points per point scored"})
    stlsfan = StringField(render_kw={"placeholder": "Enter points per steal"}, validators=[DataRequired()])
    blkfan = StringField(render_kw={"placeholder": "Enter points per block"}, validators=[DataRequired()])
    submit = SubmitField("Look Up!")
