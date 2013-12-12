"""
Contains Catalyst DAO implementations.
"""
from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_CANVAS_DAO_CLASS = 'restclients.dao_implementation.catalyst.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("catalyst", "file", url, headers)


