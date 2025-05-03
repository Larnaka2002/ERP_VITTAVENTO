"""
Инициализация базы данных для проекта ERP_VITTAVENTO
Скрипт для создания начальных данных в базе
"""
import click
from flask import current_app
from flask.cli import with_appcontext

from app.extensions import db


# from app.models.users import User, Role, Permission
# from app.models.article import ArticleCategory


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Инициализация базы данных начальными данными."""
    click.echo('Инициализация базы данных...')
    init_db()
    click.echo('База данных инициализирована!')


def init_db():
    """
    Создание начальных данных в базе
    """
    # Создание базовых ролей
    create_roles()

    # Создание администратора системы
    create_admin_user()

    # Создание базовых категорий артикулов
    create_article_categories()

    # Создание базовых типов операций
    create_operation_types()

    # Фиксация изменений
    db.session.commit()


def create_roles():
    """Создание базовых ролей пользователей"""
    """
    # Код будет добавлен после создания модели Role
    roles = {
        'admin': 'Администратор системы',
        'manager': 'Менеджер',
        'warehouse': 'Кладовщик',
        'production': 'Производственный мастер',
        'accountant': 'Бухгалтер'
    }

    for role_name, description in roles.items():
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            role = Role(name=role_name, description=description)
            db.session.add(role)
    """
    current_app.logger.info('Роли пользователей созданы')


def create_admin_user():
    """Создание администратора системы"""
    """
    # Код будет добавлен после создания модели User
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_role = Role.query.filter_by(name='admin').first()
        admin = User(
            username='admin',
            email='admin@example.com',
            password='admin',  # В производстве использовать надежный пароль
            is_active=True,
            role=admin_role
        )
        db.session.add(admin)
    """
    current_app.logger.info('Администратор системы создан')


def create_article_categories():
    """Создание базовых категорий артикулов"""
    """
    # Код будет добавлен после создания модели ArticleCategory
    categories = [
        {
            'name': 'Двери',
            'code': 'DOORS',
            'article_prefix': 'DR',
            'sequence_start': 1000,
            'subcategories': [
                {
                    'name': 'Двери массив',
                    'code': 'SOLIDWOOD',
                    'article_prefix': 'DRS',
                    'sequence_start': 1000
                },
                {
                    'name': 'Двери МДФ',
                    'code': 'MDF',
                    'article_prefix': 'DRM',
                    'sequence_start': 1000
                }
            ]
        },
        {
            'name': 'Фрезы',
            'code': 'MILLS',
            'article_prefix': 'ML',
            'sequence_start': 1000,
            'subcategories': []
        },
        {
            'name': 'Комплектующие',
            'code': 'COMPONENTS',
            'article_prefix': 'CP',
            'sequence_start': 1000,
            'subcategories': []
        },
        {
            'name': 'Станки ЧПУ',
            'code': 'CNC',
            'article_prefix': 'CN',
            'sequence_start': 1000,
            'subcategories': []
        }
    ]

    for category_data in categories:
        subcategories = category_data.pop('subcategories', [])
        category = ArticleCategory.query.filter_by(code=category_data['code']).first()

        if not category:
            category = ArticleCategory(**category_data)
            db.session.add(category)
            db.session.flush()  # Получение ID категории

            # Создание подкатегорий
            for subcat_data in subcategories:
                subcat_data['parent_id'] = category.id
                subcategory = ArticleCategory.query.filter_by(code=subcat_data['code']).first()

                if not subcategory:
                    subcategory = ArticleCategory(**subcat_data)
                    db.session.add(subcategory)
    """
    current_app.logger.info('Категории артикулов созданы')


def create_operation_types():
    """Создание базовых типов складских операций"""
    """
    # Код будет добавлен после создания модели OperationType
    operation_types = [
        {
            'name': 'Поступление от поставщика',
            'code': 'RECEIPT',
            'direction': 'in',
            'affects_cost': True
        },
        {
            'name': 'Перемещение между складами',
            'code': 'TRANSFER',
            'direction': 'internal',
            'affects_cost': False
        },
        {
            'name': 'Отгрузка клиенту',
            'code': 'SHIPMENT',
            'direction': 'out',
            'affects_cost': False
        },
        {
            'name': 'Списание',
            'code': 'WRITEOFF',
            'direction': 'out',
            'affects_cost': True
        },
        {
            'name': 'Оприходование излишков',
            'code': 'SURPLUS',
            'direction': 'in',
            'affects_cost': True
        },
        {
            'name': 'Производство',
            'code': 'PRODUCTION',
            'direction': 'in',
            'affects_cost': True
        },
        {
            'name': 'Расход на производство',
            'code': 'CONSUMPTION',
            'direction': 'out',
            'affects_cost': True
        }
    ]

    for op_data in operation_types:
        op_type = OperationType.query.filter_by(code=op_data['code']).first()

        if not op_type:
            op_type = OperationType(**op_data)
            db.session.add(op_type)
    """
    current_app.logger.info('Типы складских операций созданы')


def register_commands(app):
    """Регистрация CLI команд для приложения"""
    app.cli.add_command(init_db_command)