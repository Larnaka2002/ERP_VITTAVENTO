# app/articles/__init__.py

from flask import Blueprint

articles_bp = Blueprint('articles_bp', __name__, template_folder='templates')

