

from ..extension import  db
from ..user.models import User
from ..cart.models import Cart,CartItem
from ..product.models import Product,Brand,Category
from .views import MyModelView as ModelView

#registers models


def register_model(admin):
    admin.add_view(ModelView(User, db.session, name="Users",
                   menu_icon_type="fa", menu_icon_value="fa-users"))
    admin.add_view(ModelView(Cart, db.session, name="Carts",
                   menu_icon_type="fa", menu_icon_value="fa-cart"))
    admin.add_view(ModelView(CartItem, db.session, name="CartItem",
                   menu_icon_type="fa", menu_icon_value="fa-cart"))
    admin.add_view(ModelView(Product, db.session, name="Products",
                   menu_icon_type="fa", menu_icon_value="fa-products"))
    admin.add_view(ModelView(Brand, db.session, name="Brands",
                   menu_icon_type="fa", menu_icon_value="fa-brands"))
    admin.add_view(ModelView(Category, db.session, name="Categories",
                   menu_icon_type="fa", menu_icon_value="fa-category"))
