""" Module for the Category Schema """

from marshmallow import fields
from src.helpers.constants import EXCLUDED_FIELDS
from src.helpers.schema.base import BaseSchema
from src.product.helper.schema import ProductSchema


class CategorySchema(BaseSchema):
    """ Category Schema Class """

    name = fields.String(required=True)
    description = fields.String(required=True)
    parent_id = fields.Integer(required=True)
    products = fields.Nested(ProductSchema(many=True, exclude=EXCLUDED_FIELDS))
