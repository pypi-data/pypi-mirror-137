import json
from .exceptions import NotFoundException, AuthenticationError, ServerError, Error, RequestError


def api_exceptions_handler(api_func):
    def wrapper(*args, **kwargs):
        response = api_func(*args, **kwargs)
        response_json = response.json()
        response_str = str(response_json)

        if response.status_code in (200, 201, 202, 204):
            return response
        if response.status_code == 404:
            raise NotFoundException(response_str)
        elif response.status_code == 400:
            raise RequestError(response_str)
        elif response.status_code == 403:
            raise AuthenticationError(response_str)
        elif response.status_code in (500, 501, 502):
            raise ServerError(response_str)
        else:
            raise Error(response_str)
    return wrapper
