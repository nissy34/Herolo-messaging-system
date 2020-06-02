import logging
from flask import request
from flask import current_app as app
from flask_request_validator import (
    PATH,
    FORM,
    JSON,
    Param,
    validate_params
)

from validators.validator_rules import (
    Pattern,
    MinLength,
    MaxLength
)

# TODO use a service instead of interacting straight with the models  
from DB.models.message import Message, db
from DB.models.user import User
from DB.models.messageReceiver import MessageReceiver

from auth.decorators import token_auth

logger = logging.getLogger('rest')

@app.route('/users/<username>/message', methods=['POST'])
@token_auth
@validate_params(
    Param('username', PATH, str, required=True, rules=[
          MinLength(1, error='Invalid length. can`t be empty')]),
    Param('receiver', JSON, str, required=True, rules=[
          MinLength(1, error='Invalid length. can`t be empty')]),
    Param('subject', JSON, str, required=True, rules=[MaxLength(120, error='Invalid length. Max length = 120'),
                                                      MinLength(1, error='Invalid length. Min length = 1')]),
    Param('message', JSON, str, required=True, rules=[MaxLength(120, error='Invalid length. Max length = 120'),
                                                      MinLength(1, error='Invalid length. Min length = 1')])
)
def message_create(username, receiver, subject, message):
    """  """
    sender = User.query.filter_by(username=username).first()

    if sender is None:
        return {
            'statusCode': 400,
            'message': 'Sender dosn\'t exist'
        }, 400

    receiver = User.query.filter_by(username=content["receiver"]).first()

    # we only allow to send to existing receivers 
    if receiver is None:
        return {
            'statusCode': 400,
            'message': 'Receiver dosn\'t exist'
        }, 400

    # create the message
    message = Message(subject=subject, message=message)

    # attach the message to the sender
    sender.sentMessagas.append(message)

    # attach the message to the sender
    receiver.receivedMessages.append(MessageReceiver(message=message))

    # save changes to db
    db.session.add(message)
    db.session.commit()

    return {
        'statusCode': 201,
        'message': 'OK',
        'result': message.id
    }, 201


@app.route('/users/<username>/messages', methods=['GET'])
@token_auth
@validate_params(
    Param('username', PATH, str, required=True, rules=[
          MinLength(1, error='Invalid length. can`t be empty')]),
)
def message_get(username):
    receiver = User.query.filter_by(username=username).first()
    unread_only = request.args.get('unread', None, lambda x: x == "true")
    if receiver is None:
        return {
            'statusCode': 404,
            'message': 'User dosn\'t exist'
        }, 404
    query = MessageReceiver.query.with_parent(receiver)\
        .options(db.joinedload("message").joinedload("sender"))

    if unread_only is not None:
        query = query.filter_by(read=not unread_only)
    messages = query.paginate()
    return {
        'statusCode': 200,
        'message': 'OK',
        'result': list(map(lambda message:
                           {
                               'id': message.message.id,
                               'sender':  message.message.sender.username,
                               'receiver': username,
                               'subject': message.message.subject,
                               'message': message.message.message,
                               'creation_date': message.message.creation_date,
                           }, messages.items))

    }


@app.route('/users/<username>/messages/<message_id>', methods=['PATCH'])
@token_auth
@validate_params(
    Param('username', PATH, str, required=True, rules=[MinLength(1, error='Invalid length. can`t be empty')]),
    Param('message_id', PATH, str, required=True, rules=[MinLength(1, error='Invalid length. can`t be empty')]),
    Param('read', JSON, bool, required=True)
)
def message_read(username, message_id, read):
    receiver = User.query.filter_by(username=username).first()

    if receiver is None:
        return {
            'statusCode': 404,
            'message': 'User dosn\'t exist'
        }, 404

    message = MessageReceiver.query.with_parent(receiver)\
        .filter_by(message_id=message_id)\
        .first()
    if message is None:
        return {
            'statusCode': 404,
            'message': 'Message dosn\'t exist'
        }, 404

    message.read = read
    db.session.add(message)
    db.session.commit()

    return {
        'statusCode': 200,
        'message': 'OK',
        'result': {
            'id': message.message.id,
            'sender':  message.message.sender.username,
            'receiver': username,
            'subject': message.message.subject,
            'message': message.message.message,
            'creation_date': message.message.creation_date,
        },

    }


@app.route('/users/<username>/messages/<message_id>', methods=['DELETE'])
@token_auth
@validate_params(
    Param('username', PATH, str, required=True, rules=[MinLength(1, error='Invalid length. can`t be empty')]),
    Param('message_id', PATH, str, required=True, rules=[MinLength(1, error='Invalid length. can`t be empty')]),
)
def message_delete(username, message_id):

    user = User.query.filter_by(username=username).first()

    # sender
    message = Message.query.with_parent(user).filter_by(id=message_id).first()

    # receiver
    if message is None:
        message = MessageReceiver.query.with_parent(
            user).filter_by(message_id=message_id).first()

    if message is not None:
        db.session.delete(message)
        db.session.commit()
    return {
        'statusCode': 200,
        'message': 'OK'
    }
