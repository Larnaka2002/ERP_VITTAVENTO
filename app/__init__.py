from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Убедись, что путь к конфигурации корректен

    db.init_app(app)

    # Здесь можно зарегистрировать блюпринты, если они есть
    # from app.routes import main as main_blueprint
    # app.register_blueprint(main_blueprint)

    return app