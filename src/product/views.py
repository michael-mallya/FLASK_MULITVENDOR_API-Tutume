from flask_restx import Resource, Namespace
from src.auth.authentication.token_required import token_required
from src.auth.authentication.permission_required import permission_required, permission_seller
from src.helpers import remove_space
from flask import request,jsonify
from azure.storage.blob import BlobServiceClient, ContainerClient
from os import environ
from werkzeug.datastructures import FileStorage

from flask_restx import reqparse,fields
from src.helpers.paginate import paginate_resource
from src.helpers.responses import success_response,error_response
from src.helpers.validators.product import ProductValidators
from src.product.helper.schema import ProductSchema
from src.product.models import Product
from src.product.helper.variable import product_var,product_delete as product_del_variable,product_update
from uuid import uuid4
AZURE_CONNECTION_STRING = environ.get("CONNECTION_STRING")

api = Namespace('products', description='product related operations')
product_model = api.model('Product', product_var)
product_delete = api.model('Product-Delete', product_del_variable)
product_update_model = api.model('Product-Update-Model', product_update)
upload_parser = api.parser()
upload_parser.add_argument('image', location='files',
                           type=FileStorage, required=True)
upload_parser_many = api.parser()
upload_parser_many.add_argument('file', location='files',
                           type=FileStorage, required=True,action='append')

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload(f,name):
    try:
        service_client = BlobServiceClient.from_connection_string(
            AZURE_CONNECTION_STRING)
        container_client = service_client.get_container_client(
            "flaskcontainer")
        blob_client = container_client.get_blob_client(name)
        blob_client.upload_blob(f)
        success_response['message'] = "file uploaded successfully"
        success_response['data'] = {
            "public_id":uuid4().hex,
            "url": blob_client.url
            
        }
        

        return success_response
    except:
        error_response['message'] = "file upload failed"
        return error_response
        
@api.route("upload/main_img/")
class UploadMainImageView(Resource): 
    @api.expect(upload_parser)
    @token_required
    @permission_seller
    def post(self):
        "Upload main image"
        args  = upload_parser.parse_args()
        f = args['image']
        name = make_unique(f.filename)
        if allowed_file(name):
            response=upload(f,name)
            return response
        else:
            error_response['message'] =  "file is not allowed to upload"
            return error_response
@api.route("upload/images/")
class UploadImagesView(Resource):
    @api.expect(upload_parser_many)
    @token_required
    @permission_seller
    def post(self):
        "upload multiple images for product "

        images = request.files.getlist("images")
        metas = []
        for image in images:
            name = make_unique(image.filename)
            if allowed_file(name):
                response = upload(image,name)
                metas.append(response.get("data"))
        success_response['message'] = 'Images successfully uploaded'
        success_response['data'] = metas
                       
       
        return success_response
        


@api.route("")
class ProductView(Resource):
    """Resource class for product endpoint"""
    def get(self):
        """ Endpoint to get all products """

        products_schema = ProductSchema(many=True)
        data, meta = paginate_resource(Product, products_schema)

        success_response['message'] = 'Products successfully fetched'
        success_response['data'] = {
            'products': data,
            'meta': meta
        }

        return success_response, 
    @api.expect(product_model)
    @token_required
    @permission_seller
    def post(self):
        "ENDPOINT  to create product by the seller"
        request_data = request.get_json()
        ProductValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()
        new_product = Product(**request_data)
        new_product.save()

        product_schema = ProductSchema()
        product_data = product_schema.dump(new_product)

        success_response['message'] = 'Product successfully created'
        success_response['data'] = {
            'product': product_data
        }
        return success_response, 201
    @api.expect(product_delete)
    @token_required
    @permission_seller    
    def delete(self):
        "delete a product by id"
        request_data = request.get_json()
        
        product = Product.find_by_id(request_data.get("id"))
        if not product:
            error_response['message']= 'product is not existed'
            return error_response,400
        
        
        product.delete()
        
        success_response['message'] =  'product is deleted successfully'
        return success_response,204

    @api.expect(product_update_model)
    # @token_required
    # @permission_seller
    def patch(self):
        "ENDPOINT  to update product by the seller"
        request_data = request.get_json()
        id = request_data['id']
        del request_data['id']
        ProductValidators.validate(request_data)

        request_data = remove_space(request_data)
        request_data['name'] = request_data['name'].lower()
        updated_product = Product.find_by_id(id)
        if not updated_product:
            error_response['message'] = "Product is not existed"
            return error_response, 400
        updated_product.update(request_data)

        product_schema = ProductSchema()
        product_data = product_schema.dump(updated_product)

        success_response['message'] = 'Product successfully updated'
        success_response['data'] = {
            'product': product_data
        }
        return success_response, 201
    
