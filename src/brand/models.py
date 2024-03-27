from src.helpers.models.base import BaseModel
from src.extension import db


class Brand(BaseModel):
    """ Brand Model class """

    __tablename__ = 'brands'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship(
        'Product', backref='brand_products', lazy='joined')
