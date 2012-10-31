"""
Contains NWS DAO implementations.
"""

from django.conf import settings
from urllib3 import connection_from_url
from restclients.mock_http import MockHTTP
import re
from mock import get_mockdata_url


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_NWS_DAO_CLASS = 'restclients.dao_implementation.nws.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("nws", "file", url, headers)


class ETag(object):
    """
    The ETag DAO is a testing DAO, that is just here for
    testing the ETag cache class.  You don't want to use it
    for anything else.
    """


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    """
