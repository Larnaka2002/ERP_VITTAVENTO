from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired
from app.models.article import Article

class ArticleForm(FlaskForm):
    code = StringField('Код артикула', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    components = SelectMultipleField('Компоненты (принадлежит к сборке)', coerce=int)
    submit = SubmitField('Сохранить')

    def set_component_choices(self):
        self.components.choices = [(a.id, a.code) for a in Article.query.all()]