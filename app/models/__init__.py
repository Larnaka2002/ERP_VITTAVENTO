"""
Инициализация пакета моделей
"""
from app.models.base import BaseModel, TimestampMixin, SoftDeleteMixin
from app.models.users import User, Role

# Импорт других моделей будет добавляться по мере разработки
# from app.models.article import Article, ArticleCategory, ArticleAttribute
# from app.models.inventory import Stock, StockBatch, StockOperation
# from app.models.production import BillOfMaterials, TechnologyCard
# from app.models.sales import SalesOrder, SalesOrderItem, Invoice