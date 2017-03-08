"""
Contains UW Bookstore DAO implementations.
"""

from restclients.dao_implementation import get_timeout
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from django.conf import settings


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
        host = getattr(settings,
                       "RESTCLIENTS_BOOKSTORE_HOST",
                       'http://www3.bookstore.washington.edu/')
        if Live.pool is None:
            cert = getattr(settings, "RESTCLIENTS_BOOKSTORE_CERT", None)
            key = getattr(settings, "RESTCLIENTS_BOOKSTORE_KEY", None)
            pool_size = getattr(settings, "BOOKSTORE_MAX_POOL_SIZE", 10)
            Live.pool = get_con_pool(host,
                                     key,
                                     cert,
                                     max_pool_size=pool_size,
                                     socket_timeout=get_timeout("book"))

        # For rest router...
        url_prefix = getattr(settings, "RESTCLIENTS_BOOKSTORE_PREFIX", "")
        url = "%s%s" % (url_prefix, url)

        return get_live_url(Live.pool,
                            'GET',
                            host,
                            url,
                            headers=headers,
                            service_name='book')
