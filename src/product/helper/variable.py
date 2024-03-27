
from flask_restx import fields

product_var: dict = {
    'name': fields.String(required=True, description='Product name'),
    'description': fields.String(required=False, description='Product description'),
    'main_image': fields.Raw(require=True, description='Product image', example={
        'public_id': 'fsfdfd',
        'url': 'http://someimage.url'
    }),
    'images': fields.List(fields.Raw(example={
        'public_id': 'fsfdfd',
        'url': 'http://someimage.url'
    }), required=False, description='Product other images'),
    'category_id': fields.Integer(required=True, description='Product category ID'),
    'brand_id': fields.Integer(required=True, description='Product brand ID'),
    'price': fields.Fixed(required=True, description='Product price'),
    'quantity': fields.Integer(required=True, description='Product quantity', default=0)
}
product_update: dict = {
    'id': fields.Integer(required=True),
    'name': fields.String(description='Product name'),
    'description': fields.String(description='Product description'),
    'main_image': fields.Raw(description='Product image', example={
        'public_id': 'fsfdfd',
        'url': 'http://someimage.url'
    }),
    'images': fields.List(fields.Raw(example={
        'public_id': 'fsfdfd',
        'url': 'http://someimage.url'
    }), required=False, description='Product other images'),
    'category_id': fields.Integer(description='Product category ID'),
    'brand_id': fields.Integer(description='Product brand ID'),
    'price': fields.Fixed(description='Product price'),
    'quantity': fields.Integer(description='Product quantity', default=0)
}
product_delete: dict = {
    'id': fields.Integer(required=True, description='Product ID',example=1) 
}   
