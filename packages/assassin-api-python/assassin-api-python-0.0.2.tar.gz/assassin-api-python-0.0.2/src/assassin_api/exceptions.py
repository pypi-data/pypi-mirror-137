import sys

# sys.tracebacklimit = 0

class Error(Exception):
    __traceback__: None
    tb = None
    default_message = 'Unspecified error occurred.'

    def __init__(self, message=None, details=None):
        if message is None:
            message = self.default_message

        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        return self.default_message

    def with_traceback(self, tb):
        return None


class NotFoundException(Error):

    default_message = 'Object not found.'


class AuthenticationError(Error):

    default_message = 'Authentication error.'


class RequestError(Error):

    default_message = 'Invalid request data error.'


class ServerError(Error):

    default_message = 'Server reported error processing request.'


class InvalidQueryError(Error):

    default_message = 'Invalid query error.'


class ValidationError(Error):

    default_message = 'Validation error.'
