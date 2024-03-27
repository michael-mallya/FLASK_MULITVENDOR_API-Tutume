from flask import request
from flask_restx import Namespace, Resource
from src.auth.helper.variable import login_schema,reset_schema,request_schema,normal_user
from src.helpers import remove_space
from src.helpers.gen_token import verify_token,generate_auth_token
from src.helpers.send_mail import send_email
from src.user.helper.schema import UserSchema
from src.user.helper.validators import UserValidators
from src.user.models import User
from src.helpers.responses import error_response,success_response
from src.extension import bcrypt
from sqlalchemy.exc import IntegrityError
from datetime import timedelta




api = Namespace('auth', description='auth related operations')

login_model  = api.model("login-model",login_schema)
reset_model =api.model("reset-model",reset_schema)
request_model =api.model("request-model",request_schema)
signup_model = api.model("signup", normal_user)

@api.route("login/")
class LoginView(Resource):
    @api.expect(login_model)
    def post(self):
        "endpoint to login"
        request_data = request.get_json()
        email = request_data.get("email")
        password =  request_data.get("password")
        user = User.query.filter_by(email=email).first()
        user_schema = UserSchema()

        if user:
            user_data  = user_schema.dump(user)
            
            if user_data.get('is_activated'):
                if bcrypt.check_password_hash(user_data.get("password"),password):
                    #Timedelta is a function that allows a time period to be specified in any unit and it will calculate and return how many minutes that is. This token will expire after 5 days. # change this to one before deployment. Delta means difference.
                            token = generate_auth_token(user_data)
                            # The token isn't stored on the server. Instead the server uses the secret key to validate the token.               
                            # The payload of the token identifys the user.
                            user_schema = UserSchema(exclude=['password'])
                            logged_in_user = user_schema.dump(user)
                            success_response['message'] = 'User successfully logged in'
                            success_response['data'] = {
                                'token': token,
                                'user': logged_in_user
                            }
                            return success_response,200
                  
            
            else:
                # send_email(user_data, 'Confirmation Email', 'confirmation_email.html')
                error_response['message'] = "Account is not activated. Activation link is send to your mail."
                return error_response,203



@api.route("reset-password/")
class PasswordResetRequestView(Resource):
    """Resource class for user password"""
    @api.expect(request_model)
    def post(self):
        # request for password reset 
        request_data = request.get_json()
        email = request_data.get("email")
        user = User.find_by_email(email)
        
        if not user:
            error_response['message'] = 'User not found'
            return error_response, 404
        user_schema = UserSchema()
        token=send_email(user_schema.dump(user), 'Password Reset Request',
                   'password_reset_email.html')
        
        success_response['message'] = 'Request successfully submitted. Please check your email to continue.'
        success_response['data'] = {
            "token":token
        }
        
        return success_response,200


@api.route("reset-password/<string:token>/", endpoint="recovery")
class PasswordResetView(Resource):
    @api.expect(reset_model)
    def patch(self,token):
        user =  verify_token(token,expire_sec=600)
        if not user:
            error_response['message'] = 'Password reset token is invalid'
            return error_response,400
        request_data = request.get_json()
        UserValidators.validate_password(request_data.get("password"))
        request_data = remove_space(request_data)
        password = bcrypt.generate_password_hash(request_data.get("password"))
        user.update({'password':password})
        return {
            'status': 'success',
            'message': 'User password successfully changed'
        }, 200





@api.route("signup/buyer/")
class SignupBuyerView(Resource):
    @api.expect(signup_model)
    def post(self):
        "signup as a buyer"
        try:
            data = request.get_json()
            #validate data
            UserValidators.validate(data)
            data = remove_space(data)
            data['password'] = bcrypt.generate_password_hash(
                data.get("password")).decode('utf-8')
            new_user = User(**data)
            new_user.save()
            user_schema = UserSchema()
            user_data = user_schema.dump(new_user)
            # print(user_data)
            token = send_email(user_data, 'Confirmation Email',
                               'confirmation_email.html')

            return {
                'status': 'success',
                'message': 'User successfully created. Please check your email to continue.',
                'token': token
            }, 201
        except IntegrityError:
            return {"message": "Email is already existed."}, 409
@api.route("signup/seller/")
class SignupSellerView(Resource):
    @api.expect(signup_model)
    def post(self):
        "signup as a seller"
        try:
            
            data = request.get_json()
            #validate data
            UserValidators.validate(data)
            data = remove_space(data)
            data['password'] = bcrypt.generate_password_hash(
                data.get("password")).decode('utf-8')
            new_user = User(**data)
            new_user.save_seller()
            user_schema = UserSchema()
            user_data = user_schema.dump(new_user)
            # print(user_data)
            token = send_email(user_data, 'Confirmation Email',
                               'confirmation_email.html')

            return {
                'status': 'success',
                'message': 'Seller Account successfully created. Please check your email to continue.',
                'token': token
            }, 201
        except IntegrityError:
            return {"message": "Email is already existed."}, 409
    
        
    
                
                
        
