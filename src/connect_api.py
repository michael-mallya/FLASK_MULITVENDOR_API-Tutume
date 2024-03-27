
from flask_restx import Api 
from  flask_cors import CORS
from src.user.views import api as user
from src.auth.views import api as auth
from src.product.views import api as product 
from src.brand.views import api as brand
from src.cart.views import api as cart
from src.category.views import api as category 


authorizations = {
    'Token Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(
    title='TUTUME API',
    description='Ecommerce Multi Vendor Api',
    security='Token Auth',
    # doc='documentations/',
    authorizations=authorizations
)

def connect_blueprint(app): 
    api.add_namespace(user, path="/user/")
    api.add_namespace(auth, path="/auth/")
    api.add_namespace(product, path="/product/")
    api.add_namespace(brand, path="/brand/")
    api.add_namespace(cart, path="/cart/")
    api.add_namespace(category,path="/category/")
    
    api.init_app(app)
