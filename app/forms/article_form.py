from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Optional
from app.models.article import Article


class ArticleForm(FlaskForm):
    code = StringField('Код артикула', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    characteristics = TextAreaField('Характеристики', validators=[Optional()])
    additional_properties = TextAreaField('Дополнительные свойства', validators=[Optional()])
    weight_real = FloatField('Вес точный, lb', validators=[Optional()])
    weight_code = IntegerField('Вес код', validators=[Optional()])
    components = SelectMultipleField('Компоненты (принадлежит к сборке)', coerce=int)
    submit = SubmitField('Сохранить')

    def set_component_choices(self):
        self.components.choices = [(a.id, a.code) for a in Article.query.all()]