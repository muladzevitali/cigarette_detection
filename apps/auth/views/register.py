"""Authorization endpoints for applications"""

from flask import request
from flask_restful import Resource, abort

from apps import database
from apps.auth.models import User
from src.config import app_config


class Register(Resource):
    """Register a user"""

    def post(self):
        # Do not continue if registration is not enabled in config
        if not app_config.ENABLE_REGISTRATION:
            return abort(http_status_code=404, message='Registration not allowed')
        # if not data is sent to server
        if not request.json:
            return abort(http_status_code=400, message='No credentials sent for registration')
        # Get username and password from request
        username = request.json.get('username')
        password = request.json.get('password')
        # Check if username is already taken
        if User.query.get(username):
            return abort(http_status_code=402, message='Username already taken.')
        # Create new user
        new_user = User(username=username)
        new_user.password = password
        # Insert user into the database
        database.session.add(new_user)
        database.session.commit()

        return {'username': username}
