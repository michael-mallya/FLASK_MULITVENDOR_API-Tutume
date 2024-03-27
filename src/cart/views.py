

from flask_restx import Namespace, Resource

from src.auth.authentication.token_required import token_required
from src.cart.models import Cart
from src.helpers.constants import EXCLUDED_FIELDS
from src.cart.schema import CartSchema,CartItemSchema
from src.extension import session
from src.helpers.responses import success_response,error_response




api = Namespace('cart', description='cart related operations')



@api.route('')
class CartView(Resource):
    @token_required
    def get(self):
        "endpoint to get user cart"
        cart_schema = CartSchema(exclude=EXCLUDED_FIELDS)
        user_id  = session.current_user.get('id')
        cart = Cart.query.filter_by(user_id=user_id).first()
        cart_data = cart_schema.dump(cart)
        
        success_response['message'] = 'Cart successfully fetched'
        success_response['data'] = {
            'cart': cart_data
        }
        return success_response
    
