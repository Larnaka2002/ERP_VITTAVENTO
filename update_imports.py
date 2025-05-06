import os
import re

# Модули, которые были перемещены
app_modules = ["config", "db_test", "fix_alembic", "run", "version_push", "__init__"]
config_modules = ["render", "Procfile", ".flaskenv"]  # Только для исключения из обработки

def should_update_import(line, module_name):
    # Обрабатывает импорты вида: from config import ... или import config
    pattern_from = re.compile(rf"^from\s+{module_name}(\.|$)")
    pattern_import = re.compile(rf"^import\s+{module_name}(\.|$)")
    return pattern_from.match(line) or pattern_import.match(line)

def update_line(line, module_name):
    if f"from {module_name}" in line:
        return line.replace(f"from {module_name}", f"from app.{module_name}")
    elif f"import {module_name}" in line:
        return line.replace(f"import {module_name}", f"import app.{module_name}")
    return line

def update_imports_in_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    changed = False
    new_lines = []

    for line in lines:
        new_line = line
        for mod in app_modules:
            if should_update_import(line, mod):
                new_line = update_line(line, mod)
                changed = True
                break
        new_lines.append(new_line)

    if changed:
        backup_path = file_path + ".bak"
        shutil.copy(file_path, backup_path)
        with open(file_path, 'w') as file:
            file.writelines(new_lines)
        print(f"Updated imports in {file_path} (backup: {backup_path})")

import shutil

def process_project(directory="."):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and not filename.endswith("_bak.py"):
                full_path = os.path.join(root, filename)
                update_imports_in_file(full_path)

process_project()
print("✅ Импорты обновлены автоматически.")