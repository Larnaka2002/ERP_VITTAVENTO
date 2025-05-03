from flask import Blueprint, render_template, request, redirect, url_for
from app.forms.article_form import ArticleForm
from app.models.article import Article
from app import db  # не забудь импортировать db
from flask import redirect, url_for, flash

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
        return redirect(url_for('articles.index'))  # ← редирект на список после сохранения

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