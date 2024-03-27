from flask_restx import fields
from src.helpers.schema.base import BaseSchema
from src.helpers.constants import EXCLUDED_FIELDS
from src.user.helper.schema import UserSchema
from src.product.helper.schema import ProductSchema


class CartItemSchema(BaseSchema):
    """ CartItem Schema Class """

    excluded_fields = EXCLUDED_FIELDS.copy()
    excluded_fields.extend(
        ['quantity', 'brand_id', 'description', 'category_id', 'images'])

    quantity = fields.Integer(required=True)
    product = fields.Nested(ProductSchema(exclude=excluded_fields))


class CartSchema(BaseSchema):
    """ Cart Schema Class """

    user_excluded_fields = EXCLUDED_FIELDS.copy()
    user_excluded_fields.extend(['password', 'is_admin', 'is_activated'])

    owner = fields.Nested(UserSchema(exclude=user_excluded_fields))
    items = fields.Nested(CartItemSchema(many=True, exclude=EXCLUDED_FIELDS))
