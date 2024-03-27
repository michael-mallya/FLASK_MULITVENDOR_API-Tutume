from src.helpers.models.base import BaseModel
from src.extension import db


class Category(BaseModel):
    """ Category Model class"""

    __tablename__ = 'categories'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship(
        'Product', cascade='all, delete-orphan', backref='category_products', lazy='joined') 
