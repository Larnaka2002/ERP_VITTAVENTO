# Changelog

## [v0.1.4] - 2025-05-03

### Добавлено
- **Модуль "Артикулы"**:
  - Создано представление `create_article` для отображения формы создания артикула.
  - Шаблон `create_article.html` с формой для ввода кода и описания артикула.
  - Подключена валидация формы через Flask-WTF.
- **Маршруты**:
  - Настроен Blueprint `articles_bp` с маршрутами `/articles/` и `/articles/create`.
  - Подключена генерация `url_for('articles.create_article')` для корректного перехода.

### Исправлено
- Ошибка `BuildError` при вызове `url_for('articles.create')` (заменено на `url_for('articles.create_article')`).
- Ошибка `UndefinedError: 'form' is undefined` при отрисовке шаблона.

### Структура
- Перемещён `ArticleForm` в `app/forms/article_form.py`.
- Обновлена инициализация форм и передача данных в шаблон.

---