from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.article_form import ArticleForm
from app.forms.generator_form import GeneratorForm # Новый импорт формы генератора
from app.models.article import Article
from app.extensions import db

articles_bp = Blueprint(
    name='articles',
    import_name=__name__,
    template_folder='templates'
)

@articles_bp.route('/', methods=['GET'])
def index():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles/index.html', articles=articles)

@articles_bp.route('/create', methods=['GET', 'POST'], endpoint='create_article')
def create_article():
    form = ArticleForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_article = Article(
            code=form.code.data,
            description=form.description.data
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('articles.index'))

    return render_template('articles/create_article.html', form=form)

@articles_bp.route('/edit/<int:article_id>', methods=['GET', 'POST'], endpoint='edit_article')
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)
    if request.method == 'POST' and form.validate_on_submit():
        article.code = form.code.data
        article.description = form.description.data
        db.session.commit()
        flash('Артикул обновлён успешно.', 'success')
        return redirect(url_for('articles.index'))
    return render_template('articles/edit_article.html', form=form, article=article)

@articles_bp.route('/delete/<int:article_id>', methods=['GET'], endpoint='delete_article')
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Артикул удалён.', 'success')
    return redirect(url_for('articles.index'))

@articles_bp.route('/generator', methods=['GET', 'POST'], endpoint='article_generator')
def article_generator():
    form = GeneratorForm()
    article_code = None

    if request.method == 'POST' and form.validate_on_submit():
        # Формируем базовый код из введённых данных
        base_code = (
            f"{form.prefix.data.upper()}"
            f"{form.hierarchy_code.data}"
            f"-{form.material_code.data}"
            f"{form.color.data}"
            f"{form.material_type.data}"
        )

        # Проверка уникальности и добавление суффикса при необходимости
        article_code = base_code
        counter = 1
        while Article.query.filter_by(code=article_code).first():
            article_code = f"{base_code}-{counter}"
            counter += 1

        # Сохраняем в базу
        new_article = Article(code=article_code, description=form.name.data)
        db.session.add(new_article)
        db.session.commit()

    return render_template('articles/generator.html', form=form, article_code=article_code)