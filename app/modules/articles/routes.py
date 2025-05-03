# app/articles/routes.py

from flask import render_template
from app.articles import articles_bp
from app.modules.articles.models import Article


@articles_bp.route('/articles')
def index():
    articles = Article.query.filter_by(parent_id=None).all()
    return render_template('articles/index.html', articles=articles)


@articles_bp.route('/articles/<int:article_id>')
def detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template('articles/detail.html', article=article)