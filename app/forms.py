from flask_wtf import Form
from wtforms import TextAreaField, TextField
from wtforms.validators import Required


class CommentForm(Form):
    nimi = TextField('post', validators=[Required()])
    comment = TextAreaField('post', validators=[Required()])
    nickname = TextField('post')

