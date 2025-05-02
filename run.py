"""
Точка входа для запуска приложения ERP_VITTAVENTO
"""

import os
from app import create_app, db
from flask_migrate import Migrate, upgrade

# Создание экземпляра приложения — доступно для gunicorn
app = create_app(os.getenv('FLASK_ENV', 'default'))
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    """Добавление объектов в контекст flask shell"""
    return {
        'db': db,
        'app': app,
        # Добавляй модели при необходимости
    }

@app.cli.command()
def deploy():
    """Выполнение задач развертывания."""
    upgrade()