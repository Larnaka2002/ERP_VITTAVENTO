"""
Точка входа для запуска приложения ERP_VITTAVENTO
"""
import os
from app import create_app, db
from flask_migrate import Migrate, upgrade

# Создание экземпляра приложения
app = create_app(os.getenv('FLASK_ENV', 'default'))
migrate = Migrate(app, db)


# Импорт моделей для использования в shell
# from app.models import User, Role, Article, ArticleCategory

@app.shell_context_processor
def make_shell_context():
    """Добавление объектов в контекст flask shell"""
    return {
        'db': db,
        'app': app,
        # Здесь будут добавляться модели по мере их создания
        # 'User': User,
        # 'Role': Role,
        # 'Article': Article,
        # 'ArticleCategory': ArticleCategory,
    }


@app.cli.command()
def deploy():
    """Выполнение задач развертывания."""
    # Применение миграций базы данных
    upgrade()

    # Здесь могут быть дополнительные команды развертывания
    # например, создание ролей, начального пользователя и т.д.


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015)