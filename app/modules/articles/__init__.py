"""
Инициализация модуля артикулов

Этот модуль отвечает за управление артикулами в системе ERP VITTAVENTO.
Включает в себя функциональность для создания, просмотра, редактирования и удаления артикулов.
"""
from flask import Blueprint

# Создание blueprint для модуля артикулов
articles_bp = Blueprint(
    'articles',  # Имя blueprint
    __name__,  # Имя пакета где находится blueprint
    url_prefix='/articles',  # Префикс URL для всех маршрутов модуля
    template_folder='templates',  # Директория с шаблонами
    static_folder='static'  # Директория со статическими файлами
)

# Импорт маршрутов модуля
from app.modules.articles import routes


# Функция для инициализации модуля в приложении
def init_app(app):
    """
    Инициализация модуля артикулов в приложении Flask

    Args:
        app: Экземпляр приложения Flask
    """
    # Регистрация blueprint
    app.register_blueprint(articles_bp)

    # Дополнительная инициализация модуля (если требуется)
    app.logger.info("Модуль артикулов успешно инициализирован")

    return app