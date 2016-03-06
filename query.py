"""This module contains the Query object."""


class Query(object):

    """The Query class constructs the URL params for a request.

    :param api: The :class:`NassApi <nass.api.NassApi>` object
    """

    def __init__(self, api):
        self.api = api
        self.params = {}

    def filter(self, param, value, op=None):
        """Apply a filter to the query.

        Returns the :class:`Query <nass.query.Query>` object, so this
        method is chainable.

        The following code:
          >>> q.filter('commodity_desc', 'CORN')
          >>> q.filter('year', 2012)
        is equivalent to this code:
          >>> q.filter('commodity_desc', 'CORN').filter('year', 2012)

        :param param: Parameter name to filter
        :param value: Value to test against
        :param op: (optional) Operator comparing param and value
        :return: :class:`Query <nass.query.Query>` object
        :rtype: nass.query.Query
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
        """Pass count request to :class:`NassApi <nass.api.NassApi>`.

        :return: The number of rows in the result
        :rtype: int
        """
        return self.api.count_query(self)

    def execute(self):
        """Pass query along to :class:`NassApi <nass.api.NassApi>`.

        :return: The results of the query
        """
        return self.api.call_query(self)