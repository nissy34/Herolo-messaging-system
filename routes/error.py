from flask import request, render_template, make_response
from flask import current_app as app
from flask_request_validator.exceptions import InvalidRequest
import logging
logger = logging.getLogger("app")

from werkzeug.exceptions import InternalServerError


@app.errorhandler(404)
def page_not_found(error):
    return {
        'statusCode': 404,
        'message': 'The resource dosn`t exist'
    }, 404


@app.errorhandler(405)
def page_not_found(error):
    return {
        'statusCode': 405,
        'message': 'The method is not allowed for the requested URL'
    }, 405

@app.errorhandler(InvalidRequest)
def input_wrong(e):
    logger.error('input vialation')
    return {
        'statusCode': 422,
        'message': 'Invalid request data',
        'errors': e.errors
    }

@app.errorhandler(Exception)
def handle_500(e):
    logger.error('an unexpected error happened', exc_info=1)
    return {
        'statusCode': 500,
        'message': 'An unexpected error happend please try later'
    }, 500
