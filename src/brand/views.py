from flask import request
from flask_restx import Namespace, Resource
from src.auth.authentication.permission_required import permission_required,permission_seller

from src.auth.authentication.token_required import token_required
from flask_restx import fields
from src.brand.schema import BrandSchema
from src.helpers import remove_space
from src.helpers.validators.brand import BrandValidators

from src.brand.models import Brand
from src.helpers.responses import success_response

api = Namespace('brand', description='brand related operations')

brand_model = api.model('Brand', {
    'name': fields.String(required=True, description='Brand name'),
    'description': fields.String(required=False, description='Brand description')
})



@api.route("")
class BrandView(Resource):
    @token_required
    @permission_seller
    @api.expect(brand_model)
    def post(self):
        """ Endpoint to create the brand you have to be a seller"""

        request_data = request.get_json()
        BrandValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()

        new_brand = Brand(**request_data)
        new_brand.save()

        brand_schema = BrandSchema()
        brand_data = brand_schema.dump(new_brand)

        success_response['message'] = 'Brand successfully created'
        success_response['data'] = {
            'brand': brand_data
        }

        return success_response, 201

    def get(self):
        """ Endpoint to get all brands """

        brands_schema = BrandSchema(many=True)
        brands = brands_schema.dump(
            Brand.query.all())

        success_response['message'] = 'Brands successfully fetched'
        success_response['data'] = {
            'brands': brands
        }

        return success_response, 200
