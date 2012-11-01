"""
Contains UW Bookstore DAO implementations.
"""

from live import get_live_url
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
        return get_live_url (Live.pool, 'GET', 
                             'http://www3.bookstore.washington.edu/', 
                             None, None,
                             url, headers=headers)

