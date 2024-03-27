import datetime
from os import environ
from itsdangerous import Serializer, SignatureExpired, URLSafeTimedSerializer
import jwt
from src.user.models import User
from src.helpers.responses import error_response

s = URLSafeTimedSerializer(environ.get('SECRET_KEY'))
_email_secret = "email-confirm"

def get_token(user_id) -> str:
    """
    Generates the token for the user

    Returns:
        token(str): a string Token
    """
 
    return s.dumps({"user_id":user_id},salt=_email_secret)


def verify_token(token,expire_sec = 10):
    
    try:
        user_id = s.loads(token,salt=_email_secret,max_age=expire_sec).get('user_id')
    except SignatureExpired:
        return None
    return User.find_by_id(user_id)
    
    
def generate_auth_token(user: dict):
    """
    Generates the authentication token
    Args:
        user(dict): user data

    Returns:
        token(str): Json Web Token
    """

    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'user': user
    }
    token = jwt.encode(
        payload,
        environ.get('SECRET_KEY'),
        algorithm='HS256'
    )
    return token
