from app import create_app, db

app = create_app()

with app.app_context():
    try:
        db.engine.execute("DELETE FROM alembic_version")
        print("✅ Удалена запись из alembic_version.")
    except Exception as e:
        print("❌ Ошибка при удалении записи:", e)