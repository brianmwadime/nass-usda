USDA NASS
=========
Python wrapper around the USDA National Agricultural Statistics Service public API.

Usage
-----

.. code-block:: python

    >>> import nassusda
    >>> api = nassusda.USDAApi('APIKEY')
    >>> q = api.query()
    >>> q.filter('sector_desc', 'CROPS').filter('year', '2014', 'ge').filter('year', '2016', 'le')
    >>> q.count()
    25259
    >>> q.execute()
    [{'sector_desc': 'CROPS', ...}, ...]

See https://quickstats.nass.usda.gov/ for the full list of fields.

Exceptions
----------

If something goes wrong communicating with NASS, an exception will be raised.
This includes connection problems (e.g. timeout, DNS failure), as well as
specific error messages.

All exceptions subclass ``RestException``, so you can use it to catch all
exceptions.
