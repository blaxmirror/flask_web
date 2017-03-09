#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    # DataRequired()验证器用来确保提交的字段不为空
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
