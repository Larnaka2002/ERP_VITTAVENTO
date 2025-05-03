from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class GeneratorForm(FlaskForm):
    prefix = StringField('Префикс', validators=[DataRequired(), Length(max=3)])
    hierarchy_code = StringField('Иерархический код', validators=[DataRequired(), Length(max=6)])
    material_code = StringField('Материал', validators=[DataRequired(), Length(max=4)])
    name = StringField('Название детали', validators=[DataRequired()])
    color = StringField('Цвет', validators=[Length(max=10)])
    material_type = StringField('Тип материала', validators=[Length(max=20)])
    manufacturer = StringField('Завод-производитель', validators=[Length(max=30)])
    country = StringField('Страна', validators=[Length(max=30)])

    submit = SubmitField('Сгенерировать артикул')