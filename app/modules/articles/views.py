from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.article_form import ArticleForm
from app.forms.generator_form import GeneratorForm
from app.models.article import Article, article_components
from app.extensions import db
from flask import redirect, url_for
from app.modules.articles import articles_bp
from sqlalchemy import select

articles_bp = Blueprint(
    name='articles',
    import_name=__name__,
    template_folder='templates'
)

@articles_bp.route('/', methods=['GET'])
def index():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles/index.html', articles=articles)

# Ручное создание артикула
@articles_bp.route('/create', methods=['GET', 'POST'], endpoint='create_article')
def create_article():
    form = ArticleForm()
    if form.validate_on_submit():
        new_article = Article(
            code=form.code.data,
            description=form.description.data,
            characteristics=form.characteristics.data,
            additional_properties=form.additional_properties.data,
            weight_real=form.weight_real.data,
            weight_code=form.weight_code.data
        )
        db.session.add(new_article)
        db.session.commit()
        flash("Артикул успешно создан.", "success")
        return redirect(url_for('articles.index'))

    return render_template('articles/create_article.html', form=form)

# Генератор артикула
@articles_bp.route('/generator', methods=['GET', 'POST'], endpoint='article_generator')
def article_generator():
    form = GeneratorForm()
    available_articles = Article.query.order_by(Article.code.asc()).all()
    component_choices = [(a.id, f"{a.code} — {a.description}") for a in available_articles]

    for component_form in form.components.entries:
        component_form.form.component_id.choices = component_choices

    article_code = None

    if form.validate_on_submit():
        base_code = (
            f"{form.prefix.data.upper()}"
            f"{form.hierarchy_code.data}"
            f"-{form.material_code.data}"
            f"{form.color.data}"
            f"{form.material_type.data}"
        )

        component_codes = []
        for component_form in form.components.entries:
            component_id = component_form.component_id.data
            if component_id:
                component = Article.query.get(component_id)
                if component and component.code:
                    component_codes.append(component.code[-3:])

        component_part = ''.join(component_codes)
        article_code = f"{base_code}-{component_part}"

        original_code = article_code
        counter = 1
        while Article.query.filter_by(code=article_code).first():
            article_code = f"{original_code}-{counter}"
            counter += 1

        new_article = Article(
            code=article_code,
            description=form.name.data,
            characteristics=form.characteristics.data,
            additional_properties=form.additional_properties.data,
            weight_real=form.weight_real.data,
            weight_code=form.weight_code.data
        )
        db.session.add(new_article)
        db.session.flush()

        for component_form in form.components.entries:
            component_id = component_form.component_id.data
            quantity = component_form.quantity.data or 0
            if component_id:
                db.session.execute(
                    article_components.insert().values(
                        parent_id=new_article.id,
                        component_id=component_id,
                        quantity=quantity
                    )
                )

        try:
            db.session.commit()
            flash(f"Артикул {article_code} успешно создан!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при сохранении артикула", "danger")
            print("Ошибка:", e)

    return render_template('articles/generator.html', form=form, article_code=article_code)

# Просмотр артикула
@articles_bp.route('/view/<int:article_id>', methods=['GET'], endpoint='view_article')
def view_article(article_id):
    article = Article.query.get_or_404(article_id)

    components = db.session.execute(
        article_components.select().where(article_components.c.parent_id == article.id)
    ).fetchall()

    detailed_components = []
    for row in components:
        component_article = Article.query.get(row.component_id)
        if component_article:
            detailed_components.append({
                'id': component_article.id,
                'code': component_article.code,
                'description': component_article.description,
                'quantity': row.quantity
            })

    return render_template(
        'articles/view_article.html',
        article=article,
        components=detailed_components
    )
@articles_bp.route('/edit/<int:article_id>', methods=['GET', 'POST'], endpoint='edit_article')
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)

    if request.method == 'POST' and form.validate_on_submit():
        article.code = form.code.data
        article.description = form.description.data
        article.characteristics = form.characteristics.data
        article.additional_properties = form.additional_properties.data
        article.weight_real = form.weight_real.data
        article.weight_code = form.weight_code.data
        db.session.commit()
        flash('Артикул успешно обновлён.', 'success')
        return redirect(url_for('articles.view_article', article_id=article.id))

    return render_template('articles/edit_article.html', form=form, article=article)

@articles_bp.route('/delete/<int:article_id>', methods=['POST'], endpoint='delete_article')
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    flash('Артикул успешно удалён.', 'success')
    return redirect(url_for('articles.index'))

# Обновление веса артикула
@articles_bp.route('/update_weight/<int:article_id>', methods=['POST'], endpoint='update_weight')
def update_weight(article_id):
    article = Article.query.get_or_404(article_id)

    try:
        new_weight = float(request.form.get('weight_real'))
        article.weight_real = new_weight
        article.weight_code = round(new_weight)
        db.session.commit()
        flash("Вес успешно обновлён", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ошибка при обновлении веса", "danger")
        print(e)

    return redirect(url_for('articles.view_article', article_id=article.id))

@articles_bp.route('/')
def home():
    return redirect(url_for('articles.index'))