
from flask import request
from flask_restx import Namespace, Resource,fields
from src.auth.authentication.permission_required import permission_seller

from src.auth.authentication.token_required import token_required
from src.category.models import Category
from src.category.schema import CategorySchema
from src.helpers import remove_space
from src.helpers.validators.category import CategoryValidators
from src.helpers.responses import success_response,error_response

api = Namespace('category', description='category related operations')
category_model = api.model('Category', {
    'name': fields.String(required=True, description='Category name'),
    'description': fields.String(required=False, description='Category description'),
    'parent_id': fields.String(required=False, description='Category parent ID'),
})

@api.route('')
class CategoryView(Resource):
    """" Resource class for category endpoints """

    @token_required
    @permission_seller
    @api.expect(category_model)
    def post(self):
        """ Endpoint to create the category """
    
        request_data = request.get_json()
        CategoryValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()
        new_category = Category(**request_data)
        new_category.save()

        category_schema = CategorySchema()
        category_data = category_schema.dump(new_category)

        success_response['message'] = 'Category successfully created'
        success_response['data'] = {
            'category': category_data
        }

        return success_response, 201

    def get(self):
        """ Endpoint to get all categories """

        categories_schema = CategorySchema(many=True)
        categories = categories_schema.dump(
            Category.query.all())

        success_response['message'] = 'Categories successfully fetched'
        success_response['data'] = {
            'categories': categories
        }

        return success_response, 200


@api.route('<int:category_id>')
class SingleCategoryView(Resource):
    """" Resource class for single category endpoints """

    def get(self, category_id):
        """" Endpoint to get a single category """

        category_schema = CategorySchema()
        category = category_schema.dump(Category.find_by_id(category_id))

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404
        success_response['message'] = 'Category successfully fetched'
        success_response['data'] = {
            'category': category
        }

        return success_response, 200

    @token_required
    @api.expect(category_model)
    def put(self, category_id):
        """" Endpoint to update category """

        category_schema = CategorySchema()
        category = Category.find_by_id(category_id)

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404

        request_data = request.get_json()
        CategoryValidators.validate(request_data, category_id=category_id)
        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()

        category.update(request_data)

        success_response['message'] = 'Category successfully updated'
        success_response['data'] = {
            'category': category_schema.dump(category)
        }

        return success_response, 200

    @token_required
    def delete(self, category_id):
        """" Endpoint to delete a category """

        category_schema = CategorySchema()
        category = Category.find_by_id(category_id)

        if not category:
            error_response['message'] = 'Category not found'
            return error_response, 404

        category.delete()

        success_response['message'] = 'Category successfully deleted'
        success_response['data'] = {
            'category': category_schema.dump(category)
        }

        return success_response, 200
