from app.extensions import db

class ArticleAttribute(db.Model):
    __tablename__ = 'article_attributes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)  # Название параметра (Цвет)
    code = db.Column(db.String(16), nullable=False)  # Код для артикула (например BLK)

    values = db.relationship("ArticleAttributeValue", backref="attribute", cascade="all, delete-orphan")


class ArticleAttributeValue(db.Model):
    __tablename__ = 'article_attribute_values'

    id = db.Column(db.Integer, primary_key=True)
    attribute_id = db.Column(db.Integer, db.ForeignKey('article_attributes.id'), nullable=False)
    value = db.Column(db.String(64), nullable=False)  # Конкретное значение (например Белый)
    code = db.Column(db.String(16), nullable=False)   # Код (например WHT)