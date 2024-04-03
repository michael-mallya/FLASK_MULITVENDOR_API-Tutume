from flask_restx import Resource,Namespace
from src.auth.authentication.permission_required import permission_required
from src.helpers import remove_space
from src.helpers.gen_token import verify_token
from src.helpers.responses import success_response, error_response
from src.auth.authentication.token_required import token_required
from flask import request
from flask_jwt_extended import get_jwt_identity
from src.extension import session
from src.user.helper.schema import UserSchema
from src.user.helper.validators import UserValidators
from src.user.helper.variable import user_fields,delete_fields
from src.user.models import User


api = Namespace('user', description='user related operations')
user_model  = api.model("user_model",user_fields)
delete_user = api.model("delete_user",delete_fields)
promote_admin = api.model("promote_admin",delete_fields)

@api.route('profile/')
class userView(Resource):
    @token_required
    def get(self):
        "endpoint to get user profile"
        user = session.current_user
        del user['password']
        del user['id']
        return user
    @api.expect(user_model)
    @token_required
    def patch(self):
        "endpoint to update user profile"
        data = request.get_json()
        #validate data
        user_data=UserValidators.validate(data)
        user_data = remove_space(user_data)
        user = User.find_by_id(session.current_user.get("id"))
        if  not user:
            error_response['message'] = "internal server error"
            return error_response,400
        user.update(user_data)
        success_response['message'] = "Profile is updated"
        return success_response
    @api.expect(delete_user)
    @token_required
    @permission_required
    def delete(self):
        "delete a user by id"
        request_data = request.get_json()
        
        user = User.find_by_id(request_data.get("id"))
        if not user:
            error_response['message']= 'user is not existed'
            return error_response,400
        
        
        user.delete()
        
        success_response['message'] =  'user is deleted successfully'
        return success_response,204
@api.route("promote-admin/")
class PromoteAdminView(Resource):
    @api.expect(promote_admin)
    @token_required
    @permission_required
    def post(self):
        "promote ac]count to admin"
        request_data = request.get_json()
        user =  User.find_by_id(request_data.get("id"))
        if not user:
            error_response['message'] = "User is not existed"
            return error_response,400
        user.update({"is_admin":True})
        success_response['message'] = "User is promoted to admin"
        return success_response,203
    
        
        


@api.route('activate/<string:token>',endpoint="activate")
class UserActivateView(Resource):
    """" Resource class for user account activation endpoint """

    def get(self, token):
        """ Endpoint to activate the user account """

        user = verify_token(token,expire_sec=600)
        if user is None:
            error_response['message'] = 'Account activation token is invalid'
            return error_response, 400

        if user.is_activated:
            error_response['message'] = 'User account already activated'
            return error_response, 400

        user.update({'is_activated': True})
        #user_cart = Cart(user_id=user.id)
        #user_cart.save()

        return {
            'status': 'success',
            'message': 'User successfully activated'
        }, 200



@api.route('all-users/')
class allUserView(Resource):
    @token_required
    @permission_required
    def get(self):
        "get all users"
        user_schema =  UserSchema(many=True)
        return user_schema.dump(User.query.all())
@api.route('all-users/buyer/')
class allUserBuyerView(Resource):
    @token_required
    @permission_required
    def get(self):
        "get all buyer"
        user_schema =  UserSchema(many=True)
        return user_schema.dump(User.query.filter_by(is_seller=False))
@api.route('all-users/seller/')
class allUserSellerView(Resource):
    @token_required
    @permission_required
    def get(self):
        "get all seller"
        user_schema =  UserSchema(many=True)
        return user_schema.dump(User.query.filter_by(is_seller=True))
@api.route('all-users/admin/')
class allUserAdminView(Resource):
    @token_required
    @permission_required
    def get(self):
        "get all admin"
        user_schema =  UserSchema(many=True)
        return user_schema.dump(User.query.filter_by(is_admin=True))