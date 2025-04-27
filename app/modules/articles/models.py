"""
Модели данных для модуля артикулов

Этот модуль содержит определения моделей данных для артикулов и связанных сущностей.
"""
from app import db
from datetime import datetime
import sqlalchemy as sa


class ArticleCategory(db.Model):
    """
    Модель категории артикулов.

    Категории артикулов представляют собой иерархическую структуру для классификации артикулов.
    Например: Двери, Фурнитура, Станки ЧПУ и т.д.

    Атрибуты:
        id (int): Первичный ключ
        name (str): Наименование категории
        code (str): Уникальный код категории
        parent_id (int, optional): ID родительской категории (для иерархии)
        article_prefix (str): Префикс для генерации кодов артикулов
        sequence_start (int): Начальное значение для нумерации артикулов в этой категории
    """
    __tablename__ = 'article_category'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    code = sa.Column(sa.String(20), nullable=False, unique=True)
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('article_category.id'), nullable=True)
    article_prefix = sa.Column(sa.String(10), nullable=False)
    sequence_start = sa.Column(sa.Integer, default=1000)

    # Отношение для построения иерархии
    parent = db.relationship('ArticleCategory', remote_side=[id], backref='subcategories')

    def __repr__(self):
        return f'<ArticleCategory {self.code}: {self.name}>'


class Article(db.Model):
    """
    Модель артикула.

    Представляет единицу номенклатуры в системе. Артикулы могут быть различных типов:
    материалы, комплектующие, готовая продукция и т.д.

    Атрибуты:
        id (int): Первичный ключ
        article_code (str): Уникальный код артикула в формате XXNNNNNNN
        name (str): Наименование артикула
        description (str, optional): Описание артикула
        category_id (int): Внешний ключ к категории артикула
        is_active (bool): Флаг активности артикула
        created_at (datetime): Дата создания записи
        updated_at (datetime): Дата последнего обновления записи
    """
    __tablename__ = 'article'

    id = sa.Column(sa.Integer, primary_key=True)
    article_code = sa.Column(sa.String(20), nullable=False, unique=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.Text, nullable=True)

    # Связь с категорией
    category_id = sa.Column(sa.Integer, sa.ForeignKey('article_category.id'), nullable=False)
    category = db.relationship('ArticleCategory', backref='articles')

    # Флаги и статусы
    is_active = sa.Column(sa.Boolean, default=True)

    # Метаданные
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.article_code}: {self.name}>'

    def to_dict(self):
        """Преобразование объекта в словарь для сериализации"""
        return {
            'id': self.id,
            'article_code': self.article_code,
            'name': self.name,
            'description': self.description,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }