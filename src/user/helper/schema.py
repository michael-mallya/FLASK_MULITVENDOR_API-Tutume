from marshmallow import fields
from src.helpers.schema.base import BaseSchema


class UserSchema(BaseSchema):
    """ User Schema Class """
    id = fields.Integer(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    username = fields.String(required=True)
    phone_number=fields.String(required=True)
    is_admin = fields.Boolean(required=False)
    is_activated = fields.Boolean(required=False)
    is_seller = fields.Boolean(required=False)
