import functools
from flask import request
from flask import current_app as app
from flask_bcrypt import Bcrypt

from DB.models.user import User
from .jwt import decode_auth_token, jwt

# init bcrypt - library for hashing and addind salt yummmy
bcrypt = Bcrypt(app)

# decerator for auth with username and password
def username_password_auth(handler):

    @functools.wraps(handler)
    def auth(*args, **kwargs):

        username = request.view_args["username"]

        content = request.get_json()
        password = content["password"]

        user = User.query.filter_by(username=username).first()

        if user is None:
            return {
                'statusCode': 403,
                'message': 'user dosn`t exist or wrong password'
            }, 403

        match = bcrypt.check_password_hash(user.password, str(password))

        if not match:
            return {
                'statusCode': 403,
                'message': 'user dosn`t exist or wrong password'
            }, 403

        return handler(**{**request.view_args, **kwargs})
    return auth


# decerator for auth with jwt token
def token_auth(handler):

    @functools.wraps(handler)
    def auth(*args, **kwargs):
        username = request.view_args["username"]

        token = None
        try:
            auth_header = request.headers['Authorization']

            token = auth_header.split(" ")[1]
        except Exception:
            return {
                'statusCode': 401,
                'message': 'The Authorization header is missing or in the wrong format'
            }, 401

        try:
            username_in_token = decode_auth_token(token)
            if username_in_token != username:
                raise jwt.InvalidTokenError()
        except jwt.ExpiredSignatureError:
            return {
                'statusCode': 401,
                'message': 'Token expired.'
            }, 401
        except jwt.InvalidTokenError:
            return {
                'statusCode': 401,
                'message': 'Invalid token for user {}.'.format(username)
            }, 401

        return handler(**{**request.view_args, **kwargs})
    return auth
