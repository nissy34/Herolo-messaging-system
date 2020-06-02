from DB.models.messageReceiver import MessageReceiver
from DB.models.user import User
from DB.models.message import Message, db
from auth.jwt import encode_auth_token
from auth.decorators import username_password_auth, bcrypt, token_auth
from validators.email_validater import EmailRule
from validators.validator_rules import (
    Pattern,
    MinLength,
    MaxLength
)
from flask_request_validator import (
    PATH,
    FORM,
    JSON,
    Param,
    validate_params
)
from flask import current_app as app
from flask import request
import logging
logger = logging.getLogger()


@app.route('/user', methods=["POST"])
@validate_params(
    Param('username', JSON, str, required=True,
          rules=[MaxLength(80), MinLength(5)]),
    Param('email', JSON, str, required=True, rules=[EmailRule()]),
    Param('password', JSON, str, required=True, rules=[MinLength(6, error='Invalid length. Min length = 1'),
                                                       Pattern(r'^[a-zA-Z\d@$.!-_%*#?&]*$',
                                                               error='Invalid password. a pasword is a combination of lower and upper case digits and one of special car @$.!-_%*#?&')])
)
def create_user(username, email, password):

    # check if user name is available
    user = User.query.filter_by(username=username).first()

    if user is not None:
        return {
            'statusCode': 409,
            'message': 'A user with the user name `{}`  exists'.format(username)
        }

    # check if the email is available
    user = User.query.filter_by(email=email).first()

    if user is not None:
        return {
            'statusCode': 409,
            'message': 'A user with the email `{}`  exists'.format(email)
        }

    password = bcrypt.generate_password_hash(
        password, app.config.get('BCRYPT_LOG_ROUNDS')
    ).decode()

    user = User(email=email, username=username, password=password)

    db.session.add(user)
    db.session.commit()

    return {
        'statusCode': 201,
        'message': 'OK',
        'result': user.username
    }, 201


@app.route('/user/<username>/token', methods=["POST"])
@username_password_auth
def get_token(username):
    token = encode_auth_token(username)

    return {
        'statusCode': 201,
        'message': 'OK',
        'result': token.decode()
    }
