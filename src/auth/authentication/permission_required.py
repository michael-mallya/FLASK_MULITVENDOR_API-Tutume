""" Module for permission validation """

from functools import wraps
from flask import request
from src.user.models import User
from src.user.helper.schema import UserSchema
from src.helpers.responses import error_response


def permission_required(f):
    """ Permission decorator. Validates user if is allowed to perform action

        Args:
            f (function): Function to be decorated
        Returns:
            decorated (function): Decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = request.decoded_token
        current_user = User.find_by_id(decoded_token['user']['id'])
        user_schema = UserSchema()
        user_data = user_schema.dump(current_user)

        if not user_data['is_admin']:
            message = 'Permission denied. You are not authorized to perform this action'
            error_response['message'] = message
            return error_response, 403

        return f(*args, **kwargs)
    return decorated
def permission_seller(f):
    """ Permission decorator. Validates user if is allowed to perform action

        Args:
            f (function): Function to be decorated
        Returns:
            decorated (function): Decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        decoded_token = request.decoded_token
        current_user = User.find_by_id(decoded_token['user']['id'])
        user_schema = UserSchema()
        user_data = user_schema.dump(current_user)

        if not user_data['is_seller']:
            message = 'Permission denied. You are not a seller to perform this task'
            error_response['message'] = message
            return error_response, 403

        return f(*args, **kwargs)
    return decorated
