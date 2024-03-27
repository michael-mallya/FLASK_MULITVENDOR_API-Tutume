from flask_restx import fields


user_fields = {
    'username': fields.String(required=True, description='User Username'),
    'firstname': fields.String(required=True, description='User firstname'),
    'lastname': fields.String(required=True, description='User lastname'),
    'phone_number': fields.String(required=True, description='Enter Phone Number')
}

delete_fields={
    "id":fields.Integer(required=True,description="User Id")
}