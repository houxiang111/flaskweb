# -*- coding: utf-8 -*-
from flask.ext.wtf import FlaskForm     
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class nameform(FlaskForm):
    name = StringField('name',validators=[Required()])
    submit = SubmitField('submit')
