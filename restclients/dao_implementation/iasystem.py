"""
Contains IASystem DAO implementations.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from restclients.mock_http import MockHTTP
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
import datetime
import hashlib
import pytz


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_IASYSTEM_DAO_CLASS = 'restclients.dao_implementation.iasystem.File'
    """
    def getURL(self, url, headers, subdomain):
        return get_mockdata_url("iasystem", subdomain, url, headers)


class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.
    RESTCLIENTS_IASYSTEM_HOST
    """
    pool = {}

    def getURL(self, url, headers, subdomain):
        host = self._get_host(subdomain)

        if subdomain not in Live.pool:
            Live.pool[subdomain] = get_con_pool(host,
                key_file=settings.RESTCLIENTS_IASYSTEM_KEY_FILE,
                cert_file=settings.RESTCLIENTS_IASYSTEM_CERT_FILE)

        return get_live_url(Live.pool[subdomain], "GET", host, url, headers=headers,
                            service_name="iasystem")

    def _get_host(self, subdomain):
        host_setting = settings.RESTCLIENTS_IASYSTEM_HOST
        if "[subdomain]" not in host_setting:
            raise ImproperlyConfigured("Host configuration requires a [subdomain] placeholder")
        return host_setting.replace('[subdomain]', subdomain)

