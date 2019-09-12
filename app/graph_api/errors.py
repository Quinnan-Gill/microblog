from flask import jsonify
from graphql import GraphQLError
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    if message:
        raise GraphQLError(message)
    else:
        raise GraphQLError('Unknown error of '+str(status_code))

def bad_request(message):
    raise GraphQLError(message)