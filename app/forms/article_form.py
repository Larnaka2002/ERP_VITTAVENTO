from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class ArticleForm(FlaskForm):
    code = StringField('Код артикула', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])