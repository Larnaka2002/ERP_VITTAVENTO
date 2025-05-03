"""
Базовые модели и миксины для всех моделей приложения
"""
from datetime import datetime
from app.extensions import db


class TimestampMixin(object):
    """
    Миксин для добавления полей created_at и updated_at
    """
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin(object):
    """
    Миксин для программного удаления объектов
    (мягкое удаление - объект остается в базе, но помечается как удаленный)
    """
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def soft_delete(self):
        """Пометить объект как удаленный"""
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True
        return self

    def restore(self):
        """Восстановить объект"""
        self.deleted_at = None
        self.is_deleted = False
        return self


class BaseModel(db.Model, TimestampMixin):
    """
    Базовая модель с общими методами и полями
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """
        Получить запись по ID

        Args:
            record_id (int): ID записи

        Returns:
            object: Объект модели или None
        """
        return cls.query.filter_by(id=record_id).first()

    @classmethod
    def create(cls, **kwargs):
        """
        Создать новую запись

        Args:
            **kwargs: Аргументы для создания записи

        Returns:
            object: Созданный объект
        """
        instance = cls(**kwargs)
        return instance.save()

    def update(self, **kwargs):
        """
        Обновить запись

        Args:
            **kwargs: Аргументы для обновления

        Returns:
            object: Обновленный объект
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def save(self):
        """
        Сохранить запись в базе данных

        Returns:
            object: Сохраненный объект
        """
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """
        Удалить запись из базы данных

        Returns:
            bool: True в случае успеха
        """
        db.session.delete(self)
        db.session.commit()
        return True

    def to_dict(self):
        """
        Преобразовать объект в словарь

        Returns:
            dict: Словарь с атрибутами объекта
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}