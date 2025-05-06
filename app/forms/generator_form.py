from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, FormField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


# Вспомогательная форма для компонента
class ComponentForm(FlaskForm):
    component_id = SelectField('Компонент', coerce=int, choices=[])
    quantity = IntegerField(label='Количество', validators=[NumberRange(min=0)])


# Основная форма генератора
class GeneratorForm(FlaskForm):
    prefix = StringField(label='Префикс', validators=[DataRequired(), Length(max=3)])
    hierarchy_code = StringField(label='Иерархический код', validators=[DataRequired()])
    material_code = StringField(label='Материал', validators=[DataRequired()])
    name = StringField(label='Название детали', validators=[DataRequired()])
    color = StringField(label='Цвет', validators=[Length(max=10)])
    material_type = StringField(label='Конфигурация', validators=[Length(max=20)])  # переименовано
    manufacturer = StringField(label='Завод-производитель', validators=[Length(max=30)])
    country = StringField(label='Страна', validators=[Length(max=30)])
    characteristics = TextAreaField('Характеристики')
    additional_properties = TextAreaField('Дополнительные свойства')

    components = FieldList(FormField(ComponentForm), min_entries=1)
    submit = SubmitField('Сгенерировать артикул')