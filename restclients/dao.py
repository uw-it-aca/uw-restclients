try:
    from importlib import import_module
except:
    # python 2.6
    from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao_implementation.pws import File as PWSFile
from restclients.dao_implementation.sws import SWS_DAO
from restclients.dao_implementation.hfs import Hfs_DAO
from restclients.dao_implementation.gws import File as GWSFile
from restclients.dao_implementation.kws import File as KWSFile
from restclients.dao_implementation.book import File as BookFile
from restclients.dao_implementation.bridge import File as BridgeFile
from restclients.dao_implementation.canvas import File as CanvasFile
from restclients.dao_implementation.catalyst import File as CatalystFile
from restclients.dao_implementation.mailman import File as MailmanFile
from restclients.dao_implementation.nws import File as NWSFile
from restclients.dao_implementation.sms import Local as SMSLocal
from restclients.dao_implementation.amazon_sqs import Local as SQSLocal
from restclients.dao_implementation.trumba import FileSea
from restclients.dao_implementation.trumba import FileBot
from restclients.dao_implementation.trumba import FileTac
from restclients.dao_implementation.trumba import CalendarFile
from restclients.dao_implementation.grad import File as GradFile
from restclients.dao_implementation.hrpws import File as HrpwsFile
from restclients.dao_implementation.library.mylibinfo import (
    File as MyLibInfoFile)
from restclients.dao_implementation.library.currics import (
    File as LibCurricsFile)
from restclients.dao_implementation.myplan import File as MyPlanFile
from restclients.dao_implementation.uwnetid import File as UwnetidFile
from restclients.dao_implementation.r25 import File as R25File
from restclients.dao_implementation.iasystem import File as IASystemFile
from restclients.dao_implementation.o365 import File as O365File
from restclients.dao_implementation.upass import File as UPassFile
from restclients.cache_implementation import NoCache
from restclients.mock_http import MockHTTP
import logging
import time
from restclients_core.util.performance import PerformanceDegradation

logger = logging.getLogger(__name__)


class DAO_BASE(object):
    def _getModule(self, settings_key, default_class):
        if hasattr(settings, settings_key):
            # This is all taken from django's static file finder
            module, attr = getattr(settings, settings_key).rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                config_module = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                           '"%s" class' % (module, attr))
            return config_module()
        else:
            return default_class()


class MY_DAO(DAO_BASE):
    def _log(self, service, url, method, start_time, cached=False):
        from_cache = "yes" if cached else "no"
        total_time = time.time() - start_time
        args = (service, method, url, from_cache, total_time)
        msg = "service:%s method:%s url:%s from_cache:%s time:%s" % args
        logger.info(msg)

    def _getCache(self):
        return self._getModule('RESTCLIENTS_DAO_CACHE_CLASS', NoCache)

    def _getURL(self, service, url, headers):
        start_time = time.time()

        bad_response = PerformanceDegradation.get_response(service, url)
        if bad_response:
            return bad_response

        dao = self._getDAO()
        cache = self._getCache()
        cache_response = cache.getCache(service, url, headers)
        if cache_response is not None:
            if "response" in cache_response:
                self._log(service=service, url=url, method="GET",
                          cached=True, start_time=start_time)
                return cache_response["response"]
            if "headers" in cache_response:
                headers = cache_response["headers"]

        response = dao.getURL(url, headers)

        cache_post_response = cache.processResponse(service, url, response)

        if cache_post_response is not None:
            if "response" in cache_post_response:
                self._log(service=service, url=url, method="GET",
                          cached=True, start_time=start_time)
                return cache_post_response["response"]

        self._log(service=service, url=url, method="GET",
                  start_time=start_time)
        return response

    def _postURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        start_time = time.time()
        response = dao.postURL(url, headers, body)

        self._log(service=service, url=url, method="POST",
                  start_time=start_time)
        return response

    def _deleteURL(self, service, url, headers):
        dao = self._getDAO()
        start_time = time.time()
        response = dao.deleteURL(url, headers)
        self._log(service=service, url=url, method="DELETE",
                  start_time=start_time)
        return response

    def _putURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        start_time = time.time()
        response = dao.putURL(url, headers, body)
        self._log(service=service, url=url, method="PUT",
                  start_time=start_time)
        return response

    def _patchURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        start_time = time.time()
        response = dao.patchURL(url, headers, body)
        self._log(service=service, url=url, method="PATCH",
                  start_time=start_time)
        return response


class Subdomain_DAO(MY_DAO):
    def _getURL(self, service, url, headers, subdomain):
        dao = self._getDAO()
        cache = self._getCache()
        cache_url = subdomain + url
        cache_response = cache.getCache(service, cache_url, headers)
        if cache_response is not None:
            if "response" in cache_response:
                return cache_response["response"]
            if "headers" in cache_response:
                headers = cache_response["headers"]

        response = dao.getURL(url, headers, subdomain)

        cache_post_response = cache.processResponse(service,
                                                    cache_url,
                                                    response)

        if cache_post_response is not None:
            if "response" in cache_post_response:
                return cache_post_response["response"]

        return response


class PWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('pws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_PWS_DAO_CLASS', PWSFile)


class KWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('kws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_KWS_DAO_CLASS', KWSFile)


class GWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('gws', url, headers)

    def putURL(self, url, headers, body):
        return self._putURL('gws', url, headers, body)

    def deleteURL(self, url, headers):
        return self._deleteURL('gws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_GWS_DAO_CLASS', GWSFile)


class Book_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('books', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_BOOK_DAO_CLASS', BookFile)


class Bridge_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('bridge', url, headers)

    def patchURL(self, url, headers, body):
        return self._patchURL('bridge', url, headers, body)

    def putURL(self, url, headers, body):
        return self._putURL('bridge', url, headers, body)

    def postURL(self, url, headers, body):
        return self._postURL('bridge', url, headers, body)

    def deleteURL(self, url, headers):
        return self._deleteURL('bridge', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_BRIDGE_DAO_CLASS', BridgeFile)


class Canvas_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('canvas', url, headers)

    def putURL(self, url, headers, body):
        return self._putURL('canvas', url, headers, body)

    def postURL(self, url, headers, body):
        return self._postURL('canvas', url, headers, body)

    def deleteURL(self, url, headers):
        return self._deleteURL('canvas', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_CANVAS_DAO_CLASS', CanvasFile)


class Catalyst_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('catalyst', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_CATALYST_DAO_CLASS', CatalystFile)


class Hrpws_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('hrpws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_HRPWS_DAO_CLASS', HrpwsFile)


class Grad_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('grad', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_GRAD_DAO_CLASS', GradFile)


class R25_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('r25', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_R25_DAO_CLASS', R25File)


class AmazonSQS_DAO(MY_DAO):
    def create_queue(self, queue_name):
        dao = self._getDAO()
        return dao.create_queue(queue_name)

    def get_queue(self, queue_name):
        dao = self._getDAO()
        res = dao.get_queue(queue_name)
        return res

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_AMAZON_SQS_DAO_CLASS', SQSLocal)


class SMS_DAO(MY_DAO):
    def create_message(self, to, body):
        dao = self._getDAO()
        return dao.create_message(to, body)

    def send_message(self, message):
        dao = self._getDAO()
        return dao.send_message(message)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_SMS_DAO_CLASS', SMSLocal)


class NWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('nws', url, headers)

    def postURL(self, url, headers, body):
        return self._postURL('nws', url, headers, body)

    def putURL(self, url, headers, body):
        return self._putURL('nws', url, headers, body)

    def deleteURL(self, url, headers):
        return self._deleteURL('nws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_NWS_DAO_CLASS', NWSFile)


class Mailman_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('mailman', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_MAILMAN_DAO_CLASS',
                               MailmanFile)


class MyLibInfo_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('libraries', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_LIBRARIES_DAO_CLASS',
                               MyLibInfoFile)


class LibCurrics_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('libcurrics', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_LIBCURRICS_DAO_CLASS',
                               LibCurricsFile)


class MyPlan_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('myplan', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_MYPLAN_DAO_CLASS', MyPlanFile)


class Uwnetid_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('uwnetid', url, headers)

    def postURL(self, url, headers, body):
        return self._postURL('uwnetid', url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_UWNETID_DAO_CLASS', UwnetidFile)


class TrumbaCalendar_DAO(MY_DAO):
    def getURL(self, url, headers=None):
        return self._getURL('calendar', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_CALENDAR_DAO_CLASS', CalendarFile)


class TrumbaBot_DAO(MY_DAO):
    service_id = FileBot().get_path_prefix()

    def getURL(self, url, headers):
        return self._getURL(TrumbaBot_DAO.service_id, url, headers)

    def postURL(self, url, headers, body):
        return self._postURL(TrumbaBot_DAO.service_id, url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_TRUMBA_BOT_DAO_CLASS',
                               FileBot)


class TrumbaSea_DAO(MY_DAO):
    service_id = FileSea().get_path_prefix()

    def getURL(self, url, headers):
        return self._getURL(TrumbaSea_DAO.service_id, url, headers)

    def postURL(self, url, headers, body):
        return self._postURL(TrumbaSea_DAO.service_id, url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_TRUMBA_SEA_DAO_CLASS',
                               FileSea)


class TrumbaTac_DAO(MY_DAO):
    service_id = FileTac().get_path_prefix()

    def getURL(self, url, headers):
        return self._getURL(TrumbaTac_DAO.service_id, url, headers)

    def postURL(self, url, headers, body):
        return self._postURL(TrumbaTac_DAO.service_id, url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_TRUMBA_TAC_DAO_CLASS',
                               FileTac)


class IASYSTEM_DAO(Subdomain_DAO):
    def getURL(self, url, headers, subdomain):
        return self._getURL('iasystem', url, headers, subdomain)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_IASYSTEM_DAO_CLASS', IASystemFile)


class O365_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('o365', url, headers)

    def postURL(self, url, headers, body):
        return self._postURL('o365', url, headers, body)

    def patchURL(self, url, headers, body):
        return self._patchURL('o365', url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_O365_DAO_CLASS', O365File)


class UPass_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('upass', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_UPASS_DAO_CLASS', UPassFile)
