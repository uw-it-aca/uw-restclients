from os.path import dirname
import base64
import json
import logging
import re
from django.conf import settings
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.dao_implementation.live import get_con_pool, get_live_url


class CalendarFile(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_CALENDAR_DAO_CLASS =
                'restclients.dao_implementation.trumba.CalendarFile'
    """
    def getURL(self, url, headers):
        return get_mockdata_url("calendar", "file", url, headers)


class CalendarLive(object):
    """
    This DAO provides real calendar data.  It requires no configuration.
    """
    pool = None
    TRUMBA_HOST = 'https://www.trumba.com:443'
    MAX_POOL_SIZE = 5

    def _get_pool(self):
        return get_con_pool(CalendarLive.TRUMBA_HOST,
                            max_pool_size=CalendarLive.MAX_POOL_SIZE)

    def getURL(self, url, headers):
        if CalendarLive.pool is None:
            CalendarLive.pool = self._get_pool()

        return get_live_url(CalendarLive.pool, 'GET',
                            CalendarLive.TRUMBA_HOST,
                            url, headers=headers,
                            service_name='calendar')


class FileSea(object):
    """
    Return the url for accessing the Seattle calendars'
    mock data in local file.
    Use this DAO with this configuration:

    RESTCLIENTS_TRUMBA_SEA_DAO_CLASS =
    'restclients.dao_implementation.trumba.FileSea'
    """
    # logger = logging.getLogger('restclients.dao_implementation.trumba.File')

    def get_path_prefix(self):
        return "trumba_sea"

    def getURL(self, url, headers):
        # FileSea.logger.info("%s/file%s" % (self.get_path_prefix(), url))
        return get_mockdata_url(
            self.get_path_prefix(), "file",
            url, headers)

    def postURL(self, url, headers, body):
        """
        Implement post using a get call
        """
        new_url = url
        if body is not None:
            new_url = FileSea.convert_body(url, body)
        return self.getURL(new_url, headers)

    @staticmethod
    def convert_body(url, body):
        """
        :return: the url string with extra data in the body
        Extract the data in the body and convert to URL query string
        """
        new_url = "%s.Post" % url
        params = json.loads(body)
        for key in params:
            new_url = "%s&%s=%s" % (new_url, key,
                                    re.sub(' ', '%20',
                                           str(params[key])))
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
        if LiveSea.pool is None:
            LiveSea.pool = get_con_pool(settings.RESTCLIENTS_TRUMBA_HOST,
                                        None, None)

    def getURL(self, url, headers):
        self.set_pool()
        return get_live_url(LiveSea.pool, 'GET',
                            settings.RESTCLIENTS_TRUMBA_HOST, url,
                            headers=self.add_basicauth_header(headers),
                            service_name='trumba')

    def postURL(self, url, headers, body):
        self.set_pool()
        return get_live_url(LiveSea.pool, 'POST',
                            settings.RESTCLIENTS_TRUMBA_HOST, url,
                            headers=self.add_basicauth_header(headers),
                            body=body,
                            service_name='trumba')


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
