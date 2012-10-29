"""
Contains UW Bookstore DAO implementations.
"""
from django.conf import settings
from urllib3 import connection_from_url
from mock import get_mockdata_url

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_BOOK_DAO_CLASS = 'restclients.dao_implementation.book.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("book", "file", url, headers)

class Live(object):
    """
    This DAO provides real data.
    Access is controlled by IP address.
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool == None:

            host = 'http://www3.bookstore.washington.edu/'
            Live.pool = connection_from_url(host)

        r = Live.pool.urlopen('GET', url, headers=headers)

        return r
