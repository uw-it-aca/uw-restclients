"""
Contains Instructure Canvas DAO implementations.
"""

from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from django.conf import settings


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_CANVAS_DAO_CLASS = 'restclients.dao_implementation.canvas.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("canvas", "file", url, headers)

    def postURL(self, url, headers, body):
        return post_mockdata_url("canvas", "file", url, headers, body)


class Live(object):
    """
    This DAO provides real data.  It requires the following configuration:

    RESTCLIENTS_CANVAS_HOST="https://canvas.uw.edu"
    RESTCLIENTS_CANVAS_OAUTH_BEARER="..."
    """
    pool = None

    def getURL(self, url, headers):
        host = settings.RESTCLIENTS_CANVAS_HOST
        bearer_key = settings.RESTCLIENTS_CANVAS_OAUTH_BEARER

        headers["Authorization"] = "Bearer %s" % bearer_key

        if Live.pool == None:
            Live.pool = get_con_pool(host, None, None)
        return get_live_url(Live.pool, 'GET',
                            host, url, headers=headers)

    def postURL(self, url, headers, body):
        host = settings.RESTCLIENTS_CANVAS_HOST
        bearer_key = settings.RESTCLIENTS_CANVAS_OAUTH_BEARER

        headers["Authorization"] = "Bearer %s" % bearer_key

        if Live.pool == None:
            Live.pool = get_con_pool(host, None, None)
        return get_live_url(Live.pool, 'POST',
                            host, url, headers=headers, body=body)
