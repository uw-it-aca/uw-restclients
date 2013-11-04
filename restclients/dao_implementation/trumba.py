from os.path import dirname
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.dao_implementation.live import get_con_pool, get_live_url
from django.conf import settings
import logging
import base64
import json

class FileSea(object):
    """
    Return the url for accessing the Seattle calendars' 
    mock data in local file.
    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_SEA_DAO_CLASS =
    'restclients.dao_implementation.trumba.FileSea'
    """
    logger = logging.getLogger(
        'restclients.dao_implementation.trumba.File')

    def get_path_prefix(self):
        return "trumba_sea"
    
    def getURL(self, url, headers):
        #FileSea.logger.info("%s/file%s" % (self.get_path_prefix(), url))    
        return get_mockdata_url(self.get_path_prefix(), "file",
                                url, headers,
                                dir_base=dirname(__file__))

    def postURL(self, url, headers, body):
        # convert to a get method call    
        new_url = url
        if body is not None:
            new_url = FileSea.convert_body(url, body)
        return self.getURL(new_url, headers)

    @staticmethod
    def convert_body(url, body):
        new_url = "%s.Post" % url
        params = json.loads(body)
        for key in params:
            new_url = "%s&%s=%s" % (new_url, key, params[key])
        return new_url

class LiveSea(object):
    """
    This DAO provides real data of Seattle calendars.
    It requires further configuration, e.g.
    RESTCLIENTS_TRUMBA_HOST=
    RESTCLIENTS_TRUMBA_SEA_ID=
    RESTCLIENTS_TRUMBA_SEA_PSWD=

    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_SEA_DAO_CLASS =
    'restclients.dao_implementation.trumba.LiveSea'
    """

    logger = logging.getLogger(
        'restclients.dao_implementation.trumba.Live')

    pool = None

    def get_basic_auth(self):
        return "%s:%s" % (settings.RESTCLIENTS_TRUMBA_SEA_ID,
                          settings.RESTCLIENTS_TRUMBA_SEA_PSWD)

    def add_basicauth_header(self, headers):
        basic_auth_value = base64.urlsafe_b64encode(self.get_basic_auth())
        headers["Authorization"] = "Basic %s" % basic_auth_value
        return headers

    @staticmethod
    def set_pool():
        if LiveSea.pool == None:
            LiveSea.pool = get_con_pool(settings.RESTCLIENTS_TRUMBA_HOST,
                                        None, None)

    def getURL(self, url, headers):
        self.set_pool()
        return get_live_url(LiveSea.pool, 'GET',
                            settings.RESTCLIENTS_TRUMBA_HOST, url, 
                            headers=self.add_basicauth_header(headers))

    def postURL(self, url, headers, body):
        self.set_pool()
        return get_live_url(LiveSea.pool, 'POST',
                            settings.RESTCLIENTS_TRUMBA_HOST, url,
                            headers=self.add_basicauth_header(headers),
                            body=body)

class FileBot(FileSea):
    """
    Return the url for accessing the bothell mock data in local file
    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_BOT_DAO_CLASS =
    'restclients.dao_implementation.trumba.FileBot'
    """
    def get_path_prefix(self):
        return "trumba_bot"

class LiveBot(LiveSea):
    """
    This DAO provides real data of Bothell campus. 
    It requires further configuration, e.g.
    RESTCLIENTS_TRUMBA_HOST=
    RESTCLIENTS_TRUMBA_BOT_ID=
    RESTCLIENTS_TRUMBA_BOT_PSWD=

    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_BOT_DAO_CLASS =
    'restclients.dao_implementation.trumba.LiveBot'
    """

    def get_basic_auth(self):
        return "%s:%s" % (settings.RESTCLIENTS_TRUMBA_BOT_ID,
                          settings.RESTCLIENTS_TRUMBA_BOT_PSWD)
    
class FileTac(FileSea):
    """
    Return the url for accessing the Tacoma campus mock data in local file.  
    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_TAC_DAO_CLASS =
    'restclients.dao_implementation.trumba.FileTac'
    """
    def get_path_prefix(self):
        return "trumba_tac"

class LiveTac(LiveSea):
    """
    This DAO provides real data for Tacoma campus. 
    It requires further configuration, e.g.
    RESTCLIENTS_TRUMBA_HOST=
    RESTCLIENTS_TRUMBA_TAC_ID=
    RESTCLIENTS_TRUMBA_TAC_PSWD=

    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_TAC_DAO_CLASS =
    'restclients.dao_implementation.trumba.LiveTac'
    """

    def get_basic_auth(self):
        return "%s:%s" % (settings.RESTCLIENTS_TRUMBA_TAC_ID,
                          settings.RESTCLIENTS_TRUMBA_TAC_PSWD)
