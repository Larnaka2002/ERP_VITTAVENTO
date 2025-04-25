from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение строки подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")


def test_db_connection():
    print(f"Попытка подключения к базе данных: {DATABASE_URL}")
    try:
        # Создание движка SQLAlchemy
        engine = create_engine(DATABASE_URL)

        # Проверка подключения
        connection = engine.connect()
        print("Подключение успешно установлено!")

        # Закрытие соединения
        connection.close()
        print("Соединение закрыто.")

        return True
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return False


if __name__ == "__main__":
    test_db_connection()