from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models.base import BaseModel, TimestampMixin


class User(BaseModel, UserMixin, TimestampMixin):
    """Модель пользователя системы"""
    __tablename__ = 'users'

    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

    # Внешний ключ для роли
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Установка пароля пользователя"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверка пароля пользователя"""
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        """Проверка наличия разрешения у пользователя"""
        # TODO: Реализовать проверку разрешений
        return True


class Role(BaseModel):
    """Модель роли пользователя"""
    __tablename__ = 'roles'

    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(256))

    def __repr__(self):
        return f'<Role {self.name}>'