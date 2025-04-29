"""
Конфигурационный файл ERP_VITTAVENTO
Содержит настройки для различных окружений
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Базовая директория проекта
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Базовый класс конфигурации"""
    # Секретный ключ для защиты сессий и токенов
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change-in-production')

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = 'postgresql://vittavento_user:vittavento_pass@localhost/erp_vittavento'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Настройки приложения
    APP_NAME = 'ERP_VITTAVENTO'

    # Настройки загрузки файлов
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Настройки логирования
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def init_app(app):
        """Инициализация приложения с конфигурацией"""
        # Создание директорий, если они не существуют
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)


class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True

    # Дополнительные настройки для разработки
    SQLALCHEMY_ECHO = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://localhost/erp_vittavento_test')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    TESTING = False

    # В продакшене секретный ключ должен быть обязательно переопределен
    SECRET_KEY = os.getenv('SECRET_KEY') or None
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Production environment")

    # Дополнительные настройки безопасности
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


# Словарь доступных конфигураций
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}