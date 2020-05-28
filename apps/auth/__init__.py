import functools

from flask import request
from flask_restful import abort
from jwt import decode, DecodeError, ExpiredSignatureError

from apps.auth.models import User
from src.config import (app_config)
from .views import (Login, Register)


def login_required(method):
    """
    Check if the user is logged in
    """

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        # Get the token from header
        token = request.headers.get('Authorization')
        if not token:
            abort(http_status_code=401, message='Authorization required.')
        try:
            # Try to decode the token
            decoded = decode(token, app_config.SECRET_KEY, algorithms='HS256')
        except DecodeError:
            return abort(http_status_code=403, message='Token invalid.')
        except ExpiredSignatureError:
            return abort(http_status_code=403, message='Token expired.')
        # Get the username from decoded token
        username = decoded['username']
        # Check if the username exist in our database
        user = User.query.get(username)
        if not user:
            return abort(http_status_code=404, message='User not found.')

        return method(*args, **kwargs)

    return wrapper
