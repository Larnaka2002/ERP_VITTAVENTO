# app/modules/articles/views.py

from flask import Blueprint, render_template, request
from app.forms.article_form import ArticleForm
from flask import request

articles_bp = Blueprint(
    name='articles',
    import_name=__name__,
    template_folder='templates'
)

@articles_bp.route('/', methods=['GET'])
def index():
    return render_template('articles/index.html')

@articles_bp.route('/create', methods=['GET', 'POST'], endpoint='create_article')
def create_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Здесь можно сохранить данные в БД, позже добавим
        pass
    return render_template('articles/create_article.html', form=form)