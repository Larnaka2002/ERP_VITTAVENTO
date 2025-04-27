"""
Формы для модуля артикулов
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, FloatField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.modules.articles.models import ArticleCategory


class ArticleCategoryForm(FlaskForm):
    """Форма для создания и редактирования категорий артикулов."""

    name = StringField('Наименование', validators=[
        DataRequired(message='Наименование категории обязательно'),
        Length(max=255, message='Наименование не должно превышать 255 символов')
    ])

    code = StringField('Код', validators=[
        DataRequired(message='Код категории обязателен'),
        Length(max=50, message='Код не должен превышать 50 символов')
    ])

    parent_id = SelectField('Родительская категория', coerce=int, validators=[Optional()])

    article_prefix = StringField('Префикс артикулов', validators=[
        DataRequired(message='Префикс артикулов обязателен'),
        Length(max=10, message='Префикс не должен превышать 10 символов')
    ])

    sequence_start = StringField('Начальный номер последовательности', validators=[
        DataRequired(message='Начальный номер обязателен')
    ])

    def __init__(self, *args, **kwargs):
        super(ArticleCategoryForm, self).__init__(*args, **kwargs)
        # Загрузка списка категорий
        self.parent_id.choices = [(0, 'Нет (корневая категория)')] + [
            (cat.id, cat.name) for cat in ArticleCategory.query.order_by(ArticleCategory.name).all()
        ]


class ArticleForm(FlaskForm):
    """Форма для создания и редактирования артикулов."""

    name = StringField('Наименование', validators=[
        DataRequired(message='Наименование артикула обязательно'),
        Length(max=255, message='Наименование не должно превышать 255 символов')
    ])

    description = TextAreaField('Описание', validators=[Optional()])

    category_id = SelectField('Категория', coerce=int, validators=[
        DataRequired(message='Категория обязательна')
    ])

    weight = FloatField('Вес (кг)', validators=[Optional()])

    length = FloatField('Длина (мм)', validators=[Optional()])

    width = FloatField('Ширина (мм)', validators=[Optional()])

    height = FloatField('Высота (мм)', validators=[Optional()])

    is_active = BooleanField('Активен', default=True)

    is_purchasable = BooleanField('Доступен для закупки', default=True)

    is_sellable = BooleanField('Доступен для продажи', default=True)

    is_manufacturable = BooleanField('Производимый', default=False)

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # Загрузка списка категорий
        self.category_id.choices = [
            (cat.id, cat.name) for cat in ArticleCategory.query.order_by(ArticleCategory.name).all()
        ]


class ArticleAttributeForm(FlaskForm):
    """Форма для создания и редактирования атрибутов артикулов."""

    name = StringField('Наименование', validators=[
        DataRequired(message='Наименование атрибута обязательно'),
        Length(max=255, message='Наименование не должно превышать 255 символов')
    ])

    field_type = SelectField('Тип поля', choices=[
        ('string', 'Строка'),
        ('integer', 'Целое число'),
        ('float', 'Число с плавающей точкой'),
        ('boolean', 'Логическое значение'),
        ('enum', 'Перечисление')
    ], validators=[DataRequired(message='Тип поля обязателен')])

    required = BooleanField('Обязательное поле', default=False)

    default_value = StringField('Значение по умолчанию', validators=[Optional()])

    enum_values = TextAreaField('Значения перечисления (по одному в строке)', validators=[Optional()])

    category_id = SelectField('Категория', coerce=int, validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(ArticleAttributeForm, self).__init__(*args, **kwargs)
        # Загрузка списка категорий
        self.category_id.choices = [(0, 'Все категории')] + [
            (cat.id, cat.name) for cat in ArticleCategory.query.order_by(ArticleCategory.name).all()
        ]


class ArticleMediaForm(FlaskForm):
    """Форма для загрузки медиафайлов артикулов."""

    media_type = SelectField('Тип медиафайла', choices=[
        ('photo', 'Фотография'),
        ('drawing', 'Чертеж'),
        ('scheme', 'Схема'),
        ('document', 'Документ')
    ], validators=[DataRequired(message='Тип медиафайла обязателен')])

    file = FileField('Файл', validators=[
        FileRequired(message='Файл обязателен'),
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'dwg', 'svg', 'docx'],
                    'Разрешены только изображения и документы')
    ])