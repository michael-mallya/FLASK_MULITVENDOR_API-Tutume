from src.helpers.models.base import BaseModel
from src.extension import db


class Address(BaseModel):
    __tablename__ = 'address'
    appartment = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    
class Coupon(BaseModel):
    __tablename__ = 'coupons'
    
    code = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer,nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey("products.id"),nullable=True)
    discount = db.Column(db.Integer,nullable=False)
    multiple_uses  = db.Column(db.Boolean,nullable=False)
    
    
class CartItem(BaseModel):
    """ CartItem Model class """

    __tablename__ = 'cart_items'

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='product', lazy='joined')


class Cart(BaseModel):
    """ Cart Model class """

    __tablename__ = 'carts'

    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), unique=True, nullable=False)
    
    owner = db.relationship('User', backref='owner', lazy='joined')
    items = db.relationship('CartItem', backref='items', lazy='joined')
    # delivery_address = db.relationship('Address', backref='delivery_address', lazy='joined')
class CheckOut(BaseModel):
    """ CheckOut Model class """

    __tablename__ = 'checkouts'
    delivery_address_id = db.Column(
        db.Integer, db.ForeignKey('address.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'),unique=True,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)   
    total_price = db.Column(db.Integer,nullable=False)
    coupon =  db.Column(db.Integer,db.ForeignKey('coupons.id'),nullable=False)
    
    
