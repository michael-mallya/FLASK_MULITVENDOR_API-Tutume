""" Module for auth token validation """

import os
from functools import wraps
import jwt
from flask import request,jsonify
from src.helpers.responses import error_response
from src.user.models import User
from src.extension import session

def token_required(f):
    """ Authentication decorator. Validates token from the client

        Args:
            f (function): Function to be decorated
        Returns:
            decorated (function): Decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            message = 'No authorization token provided'
            error_response['message'] = message
            return error_response, 401

        try:
            decoded_token = jwt.decode(token, os.getenv(
                'SECRET_KEY'), algorithms=['HS256'])
            
            current_user = User.query.filter_by(id=decoded_token['id']).first()
          
            session.current_user = decoded_token.get("user")
    
            
        except:
            error_response['message'] = 'The provided authorization token is invalid'
            return error_response, 401
        
        setattr(request, 'decoded_token', decoded_token)
        return f(*args, **kwargs)
    return decorated
