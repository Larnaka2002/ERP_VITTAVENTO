"""
Маршруты для модуля артикулов

Этот модуль содержит определения маршрутов для работы с артикулами.
"""
from flask import render_template, redirect, url_for, flash, request, jsonify
from app import db
from app.modules.articles import articles_bp
from app.modules.articles.models import Article, ArticleCategory


@articles_bp.route('/')
def index():
    """
    Отображение списка артикулов

    Returns:
        HTML-страница со списком артикулов
    """
    # Запрос для получения всех активных артикулов
    articles = Article.query.filter_by(is_active=True).all()

    # Отображение списка артикулов
    return render_template('articles/index.html', articles=articles)


@articles_bp.route('/view/<int:id>')
def view(id):
    """
    Просмотр детальной информации об артикуле

    Args:
        id (int): ID артикула

    Returns:
        HTML-страница с детальной информацией об артикуле
    """
    # Запрос для получения артикула по ID
    article = Article.query.get_or_404(id)

    # Отображение информации об артикуле
    return render_template('articles/view.html', article=article)


# API-маршрут для получения списка артикулов в формате JSON
@articles_bp.route('/api/list')
def api_list():
    """
    API для получения списка артикулов

    Returns:
        JSON с массивом артикулов
    """
    articles = Article.query.filter_by(is_active=True).all()
    return jsonify([article.to_dict() for article in articles])