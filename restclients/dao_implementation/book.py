"""
Contains UW Bookstore DAO implementations.
"""
from restclients.mock_http import MockHTTP
from os.path import abspath, dirname
from django.conf import settings
from urllib3 import connection_from_url


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_BOOK_DAO_CLASS = 'restclients.dao_implementation.book.File'
    """
    def getURL(self, url, headers):
        RESOURCE_ROOT = abspath(dirname(__file__) + "/../resources/book/file")
        if url == "///":
            # Just a placeholder to put everything else in an else.
            # If there are things that need dynamic work, they'd go here
            pass
        else:
            try:
                handle = open(RESOURCE_ROOT + url)
            except IOError:
                try:
                    handle = open(RESOURCE_ROOT + url + "/index.html")
                except IOError:
                    response = MockHTTP()
                    response.status = 404
                    return response

            response = MockHTTP()
            response.status = 200
            response.data = handle.read()
            return response

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

        print url
        print r.status
        print r.data
        return r
