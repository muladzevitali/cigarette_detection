"""Authorization endpoints for applications"""

from flask import request, current_app
from flask_restful import Resource, abort
from werkzeug.local import LocalProxy

from apps import database
from apps.auth.models import User

logger = LocalProxy(lambda: current_app.logger)


class Register(Resource):
    """Register a user"""

    def post(self):
        # Get username and password from request
        username = request.json.get('username')
        password = request.json.get('password')
        # Check if password is short
        if len(password) < 8:
            logger.info(f"username: {username} tried to register with short password.")
            abort(http_status_code=401, message='Password too short.')
        # Check if username is already taken
        if User.query.get(username):
            logger.info(f"username: {username} tried to register with already taken username.")
            abort(http_status_code=402, message='Username already taken.')
        # Create new user
        new_user = User(username=username)
        new_user.hash_password(password)
        new_user.active = False
        # Insert user into the database
        database.session.add(new_user)
        database.session.commit()
        logger.info(f"username: {username} registered for the service.")

        return {'username': username}
