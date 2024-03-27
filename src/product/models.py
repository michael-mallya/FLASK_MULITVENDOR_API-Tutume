from src.helpers.models.base import BaseModel
from src.extension import db
from sqlalchemy.dialects.postgresql import JSON,ARRAY
# 
    
    
    

class Product(BaseModel):
    """ Product Model class """

    __tablename__ = 'products'

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    main_image = db.Column(JSON, nullable=False)
    
    images = db.Column(ARRAY(JSON), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey(
        'brands.id', ondelete='SET NULL'), nullable=True)
    price = db.Column(db.DECIMAL(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer,nullable=False,default=0)

