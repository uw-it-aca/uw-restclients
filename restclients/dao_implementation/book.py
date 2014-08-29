"""
Contains UW Bookstore DAO implementations.
"""

from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

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
        host = 'http://www3.bookstore.washington.edu/'
        if Live.pool == None:
            Live.pool = get_con_pool(host, None, None)
        return get_live_url (Live.pool, 'GET', 
                             host, url, headers=headers,
                             service_name='book')

