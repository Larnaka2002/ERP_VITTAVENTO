from datetime import datetime
from app.extensions import db
from sqlalchemy import Column, Integer, String, Text, DateTime, func

# Вспомогательная таблица для связи артикулов и их компонентов
article_components = db.Table(
    'article_components',
    db.Column('parent_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('component_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False)
)

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Новые поля
    characteristics = Column(Text, nullable=True)
    additional_properties = Column(Text, nullable=True)

    created_at = Column(DateTime, default=func.now())
    weight_real = db.Column(db.Float)
    weight_code = db.Column(db.Integer)

    # Иерархия — ссылка на родительский артикул
    parent_id = db.Column(db.Integer, db.ForeignKey('articles.id'), nullable=True)

    # Компоненты, входящие в сборку
    components = db.relationship(
        'Article',
        secondary=article_components,
        primaryjoin=id == article_components.c.parent_id,
        secondaryjoin=id == article_components.c.component_id,
        backref='used_in'
    )

    def __repr__(self):
        return f'<Article {self.code}>'