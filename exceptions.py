"""
This module contains exceptions raised by this package.

All exceptions subclass RestException, you can use it to catch all
exceptions
"""


class RestException(Exception):

    """Base exception class for an erroneous response.

    :param response: :class:`requests.Response` object

    """

    def __init__(self, response):
        super(RestException, self).__init__()
        self.response = response


class NetworkException(RestException):

    """Something went wrong making the request to the server.

    Raised when a :class:`requests.exceptions.RequestException` is
    caught.

    """

    def __init__(self):
        super(NetworkException, self).__init__(None)


class InvalidJson(RestException):

    """Server returned malformed JSON."""


class UnexpectedResponseData(RestException):

    """Server returned different response data than we expected.

    :param data: The data the server did return
    :param response: :class:`requests.Response` object

    """

    def __init__(self, data, response):
        super(UnexpectedResponseData, self).__init__(response)
        self.data = data


class ApiException(RestException):

    """Base exception class for error messages returned by NASS.

    :param message: Error message
    :param response: :class:`requests.Response` object

    """

    def __init__(self, message, response):
        super(ApiException, self).__init__(response)
        self.message = message

    def __str__(self):
        """Return the error message."""
        return 'Server returned error message \"%s\"' % self.message


class ExceptionList(RestException):

    """Raised when we get more than one error message.

    :param errors: The list of error messages
    :param response: :class:`requests.Response` object

    """

    def __init__(self, errors, response):
        super(ExceptionList, self).__init__(response)
        self.errors = errors

    def __str__(self):
        """Return the comma-separated list of errors."""
        return 'Server returned error messages %s' % ', '.join(self.errors)


class ExceedsRowLimit(ApiException):

    """The request would return more than 50,000 records/rows.

    :param rows: The row limit
    :param message: Error message
    :param response: :class:`requests.Response` object

    """

    def __init__(self, rows, message, response):
        super(ExceedsRowLimit, self).__init__(message, response)
        self.rows = rows


class Unauthorized(ApiException):

    """There is no key or invalid key parameter."""


class InvalidQuery(ApiException):

    """There is an error in the query string."""


class BadMediaType(ApiException):

    """The request format parameter is not JSON or CSV or XML."""