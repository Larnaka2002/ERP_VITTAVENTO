"""
Точка входа для запуска приложения ERP_VITTAVENTO локально
"""

from app import create_app, db
from flask_migrate import upgrade

app = create_app()

# Команда CLI для развёртывания (миграция базы)
@app.cli.command()
def deploy():
    """Выполнение задач развёртывания."""
    upgrade()

# Запуск приложения локально
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)