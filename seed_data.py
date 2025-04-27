from app import create_app, db
from app.modules.articles.models import ArticleCategory, Article


def seed_data():
    """Добавление тестовых данных"""
    app = create_app()
    with app.app_context():
        # Проверка, есть ли уже данные
        if ArticleCategory.query.count() > 0:
            print("В базе данных уже есть категории. Очистка не требуется.")
            return

        print("Начинаем добавление тестовых данных...")

        # Создание категорий
        doors_category = ArticleCategory(
            name="Двери",
            code="DOORS",
            article_prefix="DR",
            sequence_start=1000
        )

        accessories_category = ArticleCategory(
            name="Фурнитура",
            code="ACCESSORIES",
            article_prefix="AC",
            sequence_start=1000
        )

        cnc_category = ArticleCategory(
            name="Станки ЧПУ",
            code="CNC",
            article_prefix="CNC",
            sequence_start=1000
        )

        templates_category = ArticleCategory(
            name="Дверные шаблоны",
            code="TEMPLATES",
            article_prefix="TPL",
            sequence_start=1000
        )

        materials_category = ArticleCategory(
            name="Материалы",
            code="MATERIALS",
            article_prefix="MAT",
            sequence_start=1000
        )

        # Добавление категорий
        db.session.add(doors_category)
        db.session.add(accessories_category)
        db.session.add(cnc_category)
        db.session.add(templates_category)
        db.session.add(materials_category)
        db.session.commit()

        print("Категории успешно добавлены")

        # Создание артикулов
        articles = [
            # Двери
            Article(
                article_code="DR1001",
                name="Дверь межкомнатная стандарт",
                description="Стандартная межкомнатная дверь из массива сосны",
                category=doors_category
            ),
            Article(
                article_code="DR1002",
                name="Дверь межкомнатная премиум",
                description="Межкомнатная дверь премиум-класса из массива дуба",
                category=doors_category
            ),
            Article(
                article_code="DR1003",
                name="Дверь входная металлическая",
                description="Утепленная металлическая входная дверь с системой безопасности",
                category=doors_category
            ),

            # Фурнитура
            Article(
                article_code="AC1001",
                name="Петля дверная универсальная",
                description="Универсальная петля для межкомнатных дверей",
                category=accessories_category
            ),
            Article(
                article_code="AC1002",
                name="Ручка дверная классическая",
                description="Классическая дверная ручка из латуни",
                category=accessories_category
            ),
            Article(
                article_code="AC1003",
                name="Замок врезной",
                description="Врезной замок для межкомнатных дверей",
                category=accessories_category
            ),

            # Станки ЧПУ
            Article(
                article_code="CNC1001",
                name="Станок ЧПУ для фрезеровки",
                description="Фрезерный станок с ЧПУ для производства дверных компонентов",
                category=cnc_category
            ),
            Article(
                article_code="CNC1002",
                name="Лазерный гравировальный станок",
                description="Станок для гравировки и декоративной отделки дверей",
                category=cnc_category
            ),

            # Дверные шаблоны
            Article(
                article_code="TPL1001",
                name="Шаблон для стандартной двери",
                description="Базовый шаблон для производства стандартных межкомнатных дверей",
                category=templates_category
            ),
            Article(
                article_code="TPL1002",
                name="Шаблон с декоративными элементами",
                description="Шаблон для дверей с декоративной резьбой",
                category=templates_category
            ),

            # Материалы
            Article(
                article_code="MAT1001",
                name="Массив сосны",
                description="Пиломатериал из сосны для производства дверей",
                category=materials_category
            ),
            Article(
                article_code="MAT1002",
                name="Массив дуба",
                description="Пиломатериал из дуба для премиальных дверей",
                category=materials_category
            ),
            Article(
                article_code="MAT1003",
                name="Фурнитура крепежная",
                description="Набор крепежных элементов для сборки дверей",
                category=materials_category
            )
        ]

        # Добавление артикулов
        db.session.add_all(articles)
        db.session.commit()

        print(f"Успешно добавлено {len(articles)} артикулов")
        print("Тестовые данные успешно добавлены.")


if __name__ == "__main__":
    seed_data()