"""This module contains the Query object."""


class Query(object):

    """The Query class constructs the URL params for a request.

    :param api: The :class:`USDAApi <nassusda.api.USDAApi>` object
    """

    def __init__(self, api):
        self.api = api
        self.params = {}

    def filter(self, param, value, op=None):
        """Apply a filter to the query.
        """
        if op is None:
            self.params[param] = value
        elif op in ('le', 'lt', 'ge', 'gt', 'like', 'not_like', 'ne'):
            param_key = '{param}__{op}'.format(param=param, op=op.upper())
            self.params[param_key] = value
        else:
            raise TypeError('Invalid operator: %r' % op)
        return self

    def count(self):
        """Pass count request to :class:`USDAApi <nassusda.api.USDAApi>`.
        :return: The number of rows in the result
        """
        return self.api.count_query(self)

    def execute(self):
        """Pass query along to :class:`USDAApi <nassusda.api.USDAApi>`.
        :return: The results of the query
        """
        return self.api.call_query(self)