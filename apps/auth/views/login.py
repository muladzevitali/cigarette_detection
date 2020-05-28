"""Authorization endpoints for applications"""

import datetime

from flask import request
from flask_restful import Resource, abort
from jwt import encode

from apps.auth.models import User
from src.config import app_config


class Login(Resource):
    """User authorization"""
    def post(self):
        # Get username and password from request
        if not request.json:
            abort(http_status_code=404, message='Please provide valid credentials')
        username = request.json.get('username')
        password = request.json.get('password')
        # Find specified username in database
        user = User.query.get(username)
        # If no user was found
        if not user:
            abort(http_status_code=404, message='User not found.')
        # Verify the password
        if not user.verify_password(password):
            abort(http_status_code=406, message='Password incorrect.')
        # Expiration date for each user
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        # Encode user information to get a token
        encoded = encode({'username': username, 'exp': expiration_date}, app_config.SECRET_KEY, algorithm='HS256')

        return {'username': username, 'token': encoded.decode('utf-8')}
