"""
Office 365 DAO implementations.
"""

from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url, \
    put_mockdata_url
from restclients.exceptions import DataFailureException
from django.conf import settings
from os.path import abspath, dirname
from urllib import urlencode
import json


class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_O365_DAO_CLASS = 'restclients.dao_implementation.o365.File'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("o365", "file", url, headers)

    def postURL(self, url, headers, body):
        response = post_mockdata_url("o365", "file", url, headers, body)
        if response.status == 400:
            return response

        path = abspath(dirname(__file__) + "/../resources/o365/file" +
                       url + ".POST")

        try:
            handle = open(path)
            response.data = handle.read()
            response.status = 200
        except IOError:
            response.status = 404

        return response


class Live(object):
    """
    This DAO provides real data.  It requires the following configuration:

    RESTCLIENTS_O365_PRINCIPLE_DOMAIAN='mumble.com'
    RESTCLIENTS_O365_TENANT='mumble.onmicrosoft.com'
    RESTCLIENTS_O365_CLIENT_ID='<uuid>'
    RESTCLIENTS_O365_CLIENT_SECRET='Base64Secret=='

    The following configuration can be overriden:

    RESTCLIENTS_O365_AUTH_HOST defauls to 'https://login.windows.net'
    RESTCLIENTS_O365_API_HOST defaults to 'https://graph.windows.net'

    """
    pool = None
    authorization = None
    ignore_security = getattr(settings,
                              'RESTCLIENTS_O365_IGNORE_CA_SECURITY',
                              False)
    verify_https = True
    if ignore_security:
        verify_https = False

    def __init__(self):
        self._auth_host = getattr(
            settings, 'RESTCLIENTS_O365_AUTH_HOST', 'https://login.windows.net')
        self._api_host = getattr(
            settings, 'RESTCLIENTS_O365_API_HOST', 'https://graph.windows.net')
        'https://login.windows.net'
        

    def getURL(self, url, headers):
        if Live.authorization is None:
            Live.authorization = self._get_auth_token()
        headers['Authorization'] = Live.authorization
        if Live.pool is None:
            Live.pool = self._get_pool(self._api_host)

        response = get_live_url(Live.pool, 'GET', self._api_host,
                                url, headers=headers,
                                service_name='o365')

        if self._expired_auth_token(response):
            return self.getURL(url, headers)

        return response


    def postURL(self, url, headers, body):
        if Live.authorization is None:
            Live.authorization = self._get_auth_token()

        headers['Authorization'] = Live.authorization
        if Live.pool is None:
            Live.pool = self._get_pool(self._api_host)

        response = get_live_url(Live.pool, 'POST', self._api_host,
                                url, headers=headers, body=body,
                                service_name='o365')

        if self._expired_auth_token(response):
            return self.postURL(url, headers, body)

        return response


    def _get_pool(self, host):
        socket_timeout = 15  # default values
        if hasattr(settings, "RESTCLIENTS_O365_SOCKET_TIMEOUT"):
            socket_timeout = settings.RESTCLIENTS_O365_SOCKET_TIMEOUT
        return get_con_pool(host,
                            verify_https=Live.verify_https,
                            socket_timeout=socket_timeout)

    def _get_auth_token(self):
        """Given the office356 tenant and client id, and client secret
        acquire a new authorization token
        """
        url = '/%s/oauth2/token' % getattr(
            settings, 'RESTCLIENTS_O365_TENANT', 'test')
        headers={ 'Accept': 'application/json' }
        data= {
            "grant_type": "client_credentials",
            "client_id": getattr(settings, 'RESTCLIENTS_O365_CLIENT_ID', None),
            "client_secret": getattr(settings, 'RESTCLIENTS_O365_CLIENT_SECRET', None),
            "resource": self._api_host
        }
        body = urlencode(data)
        auth_pool = self._get_pool(self._auth_host)
        response = get_live_url(auth_pool, 'POST', self._auth_host,
                                url, headers=headers, body=body,
                                service_name='o365')
        try:
            json_data = json.loads(response.data)
            if response.status == 200:
                return "%s %s" % (
                    json_data['token_type'], json_data['access_token'])
            else:
                raise DataFailureException(
                    url, response.status, 
                    'Auth token failure: %s - %s' % (
                        json_data.get('error', 'unknown'),
                        json_data.get('error_description', 'no description')))
        except ValueError:
            raise DataFailureException(
                url, response.status, 
                'Auth token failure: %s' % (response.data))

    def _expired_auth_token(self, response):
        try:
            if response.status == 401:
                odata_error = json.loads(response.data)['odata.error']
                if err_text['code'] == 'Authentication_ExpiredToken':
                    Live.authorization = None
                    return True
        except:
            pass

        return False
