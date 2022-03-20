"""This module contains the high-level API object."""

import requests
from . import exceptions
from .query import Query


class USDAApi(object):

    """USDA National Agricultural Statistics Service API wrapper class.
    :param key: API key
    Usage::
      >>> from nassusda import USDAApi
      >>> api = USDAApi('APIKEY')
    """

    BASE_URL = 'https://quickstats.nass.usda.gov/api'

    def __init__(self, key):
        self.key = key
        self.http = requests.Session()

    def _api_request(self, url, params, field_name):
        """Make the HTTP request.
        The API key is added to the params dictionary. If there is an
        error connecting, or if the response isn't valid JSON, raises an
        exception.
        :param url: The url (appended to API base url)
        :param params: Values to be encoded as the query string
        :param field_name: Key of result in JSON response to be returned
        :return: The decoded value of field_name in the response
        """
        api_url = self.BASE_URL + url
        params.update({'key': self.key})

        try:
            resp = self.http.get(api_url, params=params)
        except requests.RequestException:
            raise exceptions.NetworkException()

        try:
            data = resp.json()
        except ValueError:
            raise exceptions.InvalidJson(resp)

        return self._handle_response_data(data, resp, field_name)

    @classmethod
    def _handle_response_data(cls, data, response, field_name):
        """Parse response object.
        Expects the response text to be a dictionary containing a key
        with the name field_name.
            1. Makes sure response contains no errors
            2. Checks that the status code was 200
            3. Returns the desired value from the JSON object
        If any of the above steps fail, raises an exception
        :param data: The decoded JSON data
        :param response: :class:`requests.Response` object
        :param field_name: Key of result in data to be returned
        :return: The value of field_name in data
        """
        try:
            errors = data['error']
        except (KeyError, TypeError):
            pass
        else:
            cls._raise_for_error_message(data['error'], response)

        if response.status_code != 200:
            raise exceptions.NassException(response)

        try:
            result = data[field_name]
        except (KeyError, TypeError):
            raise exceptions.UnexpectedResponseData(data, response)

        return result

    @classmethod
    def _raise_for_error_message(cls, errors, response):
        """Raise an exception from an error message.
        Will attempt to raise some subclass of ApiException
        :param errors: The list of error messages
        :param response: :class:`requests.Response` object
        """
        if isinstance(errors, list):
            if len(errors) > 1:
                raise exceptions.ExceptionList(errors, response)
            elif len(errors) == 1:
                message = errors[0]
                error_classes = {
                    'unauthorized': exceptions.Unauthorized,
                    'bad request - invalid query': exceptions.InvalidQuery,
                    'bad request - unsupported media type':
                        exceptions.BadMediaType,
                }
                if message in error_classes:
                    exc_class = error_classes[message]
                    raise exc_class(message, response)
                elif message.startswith('exceeds limit'):
                    try:
                        rows = int(message.split('=')[1])
                    except (IndexError, ValueError):
                        rows = None
                    raise exceptions.ExceedsRowLimit(rows, message, response)
                else:
                    raise exceptions.ApiException(message, response)

    def param_values(self, param):
        """Return all possible values of the given parameter.
        :param param: The parameter name
        :return: Possible values
        :rtype: list
        Usage::
          >>> from nassusda import USDAApi
          >>> api = USDAApi('APIKEY')
          >>> api.param_values('source_desc')
          >>> ['CENSUS', 'SURVEY']
        """
        return self._api_request('/get_param_values/', {'param': param}, param)

    def query(self):
        """Create a query used for filtering.
        :return: :class:`Query <nassusda.query.Query>` object
        :rtype: nassusda.query.Query
        Usage::
          >>> from usda import USDAApi
          >>> api = USDAApi('api key')
          >>> q = api.query()
          >>> q.filter('sector_desc', 'CROPS').filter('year', 2016)
          >>> q.count()
          141811
        """
        return Query(self)

    def count_query(self, query):
        """Return the row count of a given query.
        This is called internally by :meth:`Query.count()
        <nassusda.query.Query.count>`, try not to call it directly.
        :param query: the :class:`Query <nassusda.query.Query>` object
        :return: The number of rows in the result
        :rtype: int
        """
        count = self._api_request('/get_counts/', query.params, 'count')
        return int(count)

    def call_query(self, query):
        """Return the result of a given query.
        This is called internally by :meth:`Query.execute()
        <nassusda.query.Query.execute>`, try not to call it directly.
        :param query: the :class:`Query <nassusda.query.Query>` object
        :return: The results of the query
        :rtype: list
        """
        return self._api_request('/api_GET/', query.params, 'data')
