from flask_restx import fields

login_schema = {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
}
reset_schema = {
    'password': fields.String(required=True, description='User new password')
}
request_schema = {
    'email': fields.String(required=True, description='User email')
}


normal_user = {
    'username': fields.String(required=True, description='User Username'),
    'firstname': fields.String(required=True, description='User firstname'),
    'lastname': fields.String(required=True, description='User lastname'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'phone_number': fields.String(required=True, description='Enter Phone Number')
}
