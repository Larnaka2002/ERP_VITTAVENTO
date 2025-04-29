"""Инициализация пакета маршрутов (routes)

Этот файл отвечает за доступность, он нужен для обозначения директории как пакета Python
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Логирование
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s in %(module)s: %(message)s'
)

def register_shell_context(app):
    """Регистрация дополнительных объектов в контексте shell"""
    def shell_context():
        return {'db': db, 'app': app}
    app.shell_context_processor(shell_context)

def register_blueprints(app):
    """Регистрация схем"""
    # Импорт схем
    from app.routes.main import main_bp
    from app.routes.auth import auth

    # Регистрация основных схем
    app.register_blueprint(main_bp)
    app.register_blueprint(auth)

# Инициализация модулей
try:
    from app.modules.articles import init_app as init_articles
    init_articles(app)
except ImportError as e:
    logging.error(f'Не удалось импортировать модуль articles: {e}')

logging.info('ERP_VITTAVENTO запущена')