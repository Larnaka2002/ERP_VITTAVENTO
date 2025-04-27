"""
Инициализация приложения ERP_VITTAVENTO
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

from config import config

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()
csrf = CSRFProtect()

# Настройка login_manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    from app.models.users import User
    return User.query.get(int(user_id))


# Импорт для инициализации базы данных
from app.init_db import register_commands


def create_app(config_name=None):
    """
    Фабрика приложений - создает экземпляр приложения с указанной конфигурацией

    Args:
        config_name (str): Имя конфигурации из config.py

    Returns:
        Flask: Экземпляр Flask приложения
    """
    # Определение конфигурации
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    # Создание экземпляра приложения
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    csrf.init_app(app)

    # Настройка логирования
    setup_logging(app)

    # Регистрация схем (blueprints)
    register_blueprints(app)

    # Регистрация обработчиков ошибок
    register_error_handlers(app)

    # Регистрация команд оболочки
    register_shell_context(app)

    # Регистрация CLI команд
    register_commands(app)

    return app


def setup_logging(app):
    """
    Настройка логирования приложения

    Args:
        app (Flask): Экземпляр Flask приложения
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Настройка ротации файлов логов
    file_handler = RotatingFileHandler(
        'logs/erp_vittavento.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)

    # Установка уровня логирования
    log_level = app.config['LOG_LEVEL']
    file_handler.setLevel(getattr(logging, log_level))

    # Добавление хэндлера к логгеру приложения
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, log_level))

    app.logger.info('ERP_VITTAVENTO запущена')


def register_blueprints(app):
    """
    Регистрация blueprints (схем) приложения

    Args:
        app (Flask): Экземпляр Flask приложения
    """
    # Импорт схем
    from app.routes.main import main_bp

    # Регистрация основной схемы
    app.register_blueprint(main_bp)

    # Инициализация модуля артикулов
    try:
        from app.modules.articles import init_app as init_articles
        init_articles(app)
        app.logger.info("Модуль артикулов успешно инициализирован")
    except Exception as e:
        app.logger.error(f"Ошибка при инициализации модуля артикулов: {str(e)}")

    # Здесь будут регистрироваться другие схемы или модули по мере разработки
    # app.register_blueprint(inventory_bp, url_prefix='/inventory')
    # ...


def register_error_handlers(app):
    """
    Регистрация обработчиков ошибок

    Args:
        app (Flask): Экземпляр Flask приложения
    """

    @app.errorhandler(404)
    def not_found_error(error):
        """Обработчик ошибки 404 - Страница не найдена"""
        app.logger.warning(f"404 ошибка: {error}")
        return {'error': 'Ресурс не найден'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        """Обработчик ошибки 500 - Внутренняя ошибка сервера"""
        app.logger.error(f"500 ошибка: {error}")
        db.session.rollback()  # Откат транзакции в случае ошибки
        return {'error': 'Внутренняя ошибка сервера'}, 500


def register_shell_context(app):
    """
    Регистрация контекста оболочки для flask shell

    Args:
        app (Flask): Экземпляр Flask приложения
    """

    @app.shell_context_processor
    def make_shell_context():
        """Добавление объектов в контекст flask shell"""
        return {
            'db': db,
            'app': app,
            # Здесь будут добавляться модели по мере их создания
        }

    """
    Инициализация приложения ERP VITTAVENTO

    Этот модуль содержит фабрику приложения Flask и инициализацию всех компонентов.
    """
    import os
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from flask_login import LoginManager
    from config import config

    # Инициализация расширений
    db = SQLAlchemy()
    migrate = Migrate()
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите в систему для доступа к этой странице.'
    login_manager.login_message_category = 'info'

    def create_app(config_name=None):
        """
        Фабрика приложения Flask

        Args:
            config_name (str): Имя конфигурации (development, testing, production)

        Returns:
            Flask: Экземпляр приложения Flask
        """
        if config_name is None:
            config_name = os.environ.get('FLASK_CONFIG', 'development')

        app = Flask(__name__)
        app.config.from_object(config[config_name])
        config[config_name].init_app(app)

        # Инициализация расширений
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)

        # Регистрация blueprints
        register_blueprints(app)

        # Регистрация обработчиков ошибок
        register_error_handlers(app)

        return app

    def register_blueprints(app):
        """
        Регистрация blueprints (схем) приложения

        Args:
            app (Flask): Экземпляр Flask приложения
        """
        # Импорт схем
        from app.routes.main import main_bp

        # Регистрация основной схемы
        app.register_blueprint(main_bp)

        # Инициализация модулей
        try:
            from app.modules.articles import init_app as init_articles
            init_articles(app)
            app.logger.info("Модуль артикулов успешно инициализирован")
        except Exception as e:
            app.logger.error(f"Ошибка при инициализации модуля артикулов: {str(e)}")

        # Другие модули будут добавлены здесь

    def register_error_handlers(app):
        """
        Регистрация обработчиков ошибок

        Args:
            app (Flask): Экземпляр Flask приложения
        """

        @app.errorhandler(404)
        def not_found_error(error):
            return render_template('error/404.html'), 404

        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return render_template('error/500.html'), 500