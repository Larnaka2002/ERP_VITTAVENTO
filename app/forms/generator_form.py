
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms import TextAreaField
from wtforms import IntegerField

# Вспомогательная форма для компонента
class ComponentForm(FlaskForm):
    component_id = SelectField('Компонент', coerce=int, choices=[])
    quantity = IntegerField(label='Количество', validators=[NumberRange(min=0)])

# Основная форма генератора
class GeneratorForm(FlaskForm):
    prefix = StringField(label='Префикс', validators=[DataRequired(), Length(max=3)])
    hierarchy_code = StringField(label='Иерархия', validators=[DataRequired()])
    material_code = StringField(label='Модель', validators=[DataRequired()])
    name = StringField(label='Название детали', validators=[DataRequired()])
    color = StringField(label='Цвет', validators=[Length(max=10)])
    material_type = StringField(label='Вес (код)', validators=[Length(max=20)])
    weight_real = FloatField(label='Фактический вес (lb)', validators=[DataRequired()])
    manufacturer = StringField(label='Завод-производитель', validators=[Length(max=30)])
    country = StringField(label='Страна', validators=[Length(max=30)])
    components = FieldList(FormField(ComponentForm), min_entries=1)
    characteristics = TextAreaField('Характеристики')
    additional_properties = TextAreaField('Дополнительные свойства')
    submit = SubmitField('Сгенерировать артикул')

    # другие поля
    weight_code = IntegerField('Округлённый вес')