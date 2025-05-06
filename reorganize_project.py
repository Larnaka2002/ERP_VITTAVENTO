import os
import shutil

# Файлы, которые нужно переместить в app/
app_files = [
    "config.py", "db_test.py", "fix_alembic.py",
    "run.py", "version_push.py", "__init__.py"
]

# Файлы, которые нужно переместить в config/
config_files = ["render.yaml", "Procfile", ".flaskenv"]

# Создание директорий
os.makedirs("app", exist_ok=True)
os.makedirs("config", exist_ok=True)

# Перемещение файлов в app/
for file in app_files:
    if os.path.isfile(file):
        print(f"Moving {file} to app/")
        shutil.move(file, os.path.join("app", file))

# Перемещение конфигурационных файлов
for file in config_files:
    if os.path.isfile(file):
        print(f"Moving {file} to config/")
        shutil.move(file, os.path.join("config", file))

# Обновление .gitignore
gitignore_path = ".gitignore"
lines_to_add = [".idea/", "__pycache__/", "*.pyc"]

if os.path.exists(gitignore_path):
    with open(gitignore_path, "r") as f:
        existing = f.read().splitlines()
else:
    existing = []

with open(gitignore_path, "a") as f:
    for line in lines_to_add:
        if line not in existing:
            f.write(line + "\n")
            print(f"Added '{line}' to .gitignore")

print("Структура проекта успешно обновлена.")