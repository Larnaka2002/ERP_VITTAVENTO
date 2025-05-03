"""
Инициализация приложения ERP_VITTAVENTO
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import config

# Импорт всех расширений из extensions
from app.extensions import db, migrate, login_manager, jwt, csrf, babel

# Настройка LoginManager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from app.models.users import User
    return User.query.get(int(user_id))

# Импорт CLI-команд
from app.init_db import register_commands

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Настройка языка
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    babel.init_app(app)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)

    # Логирование
    setup_logging(app)

    # Регистрация компонентов
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    # Flask-Admin
    from app.models.users import User, Role
    from app.models.article import Article
    from app.models.article_attributes import ArticleAttribute, ArticleAttributeValue  # ← ДОБАВЛЕНО

    admin_panel = Admin(app, name='Админка ERP', template_mode='bootstrap4')
    admin_panel.add_view(ModelView(User, db.session))
    admin_panel.add_view(ModelView(Role, db.session))
    admin_panel.add_view(ModelView(Article, db.session))
    admin_panel.add_view(ModelView(ArticleAttribute, db.session))  # ← ДОБАВЛЕНО
    admin_panel.add_view(ModelView(ArticleAttributeValue, db.session))  # ← ДОБАВЛЕНО

    # Импорт моделей для миграций
    from app.models import article, article_attributes  # ← ОБНОВЛЕНО

    return app

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/erp_vittavento.log', maxBytes=10 * 1024 * 1024, backupCount=10)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info('ERP_VITTAVENTO запущена')

def register_blueprints(app):
    from app.routes.main import main_bp
    from app.modules.articles.views import articles_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(articles_bp, url_prefix='/articles')

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.warning(f"404 ошибка: {error}")
        return {'error': 'Ресурс не найден'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 ошибка: {error}")
        db.session.rollback()
        return {'error': 'Внутренняя ошибка сервера'}, 500

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}