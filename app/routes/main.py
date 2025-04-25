"""
Основные маршруты приложения ERP_VITTAVENTO
"""
from flask import Blueprint, render_template, jsonify

# Создание Blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Главная страница приложения

    Returns:
        str: HTML-страница
    """
    return render_template('index.html', title='ERP VITTAVENTO')


@main_bp.route('/health')
def health():
    """
    Проверка состояния приложения

    Returns:
        JSON: Статус приложения
    """
    return jsonify({
        'status': 'ok',
        'app': 'ERP_VITTAVENTO',
        'version': '0.1.0'
    })