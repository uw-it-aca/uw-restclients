from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao_implementation.pws import File as PWSFile
from restclients.dao_implementation.sws import File as SWSFile
from restclients.dao_implementation.gws import File as GWSFile
from restclients.dao_implementation.book import File as BookFile
from restclients.dao_implementation.canvas import File as CanvasFile
from restclients.dao_implementation.catalyst import File as CatalystFile
from restclients.dao_implementation.nws import File as NWSFile
from restclients.dao_implementation.sms import Local as SMSLocal
from restclients.dao_implementation.amazon_sqs import Local as SQSLocal
from restclients.dao_implementation.trumba import FileSea
from restclients.dao_implementation.trumba import FileBot
from restclients.dao_implementation.trumba import FileTac
from restclients.dao_implementation.libraries import File as LibrariesFile
from restclients.dao_implementation.hfs import File as HfsFile
from restclients.dao_implementation.uwnetid import File as UwnetidFile
from restclients.dao_implementation.r25 import File as R25File
from restclients.cache_implementation import NoCache


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
    def _getCache(self):
        return self._getModule('RESTCLIENTS_DAO_CACHE_CLASS', NoCache)

    def _getURL(self, service, url, headers):
        dao = self._getDAO()
        cache = self._getCache()
        cache_response = cache.getCache(service, url, headers)
        if cache_response != None:
            if "response" in cache_response:
                print "Returning the cached version..."
                return cache_response["response"]
            if "headers" in cache_response:
                headers = cache_response["headers"]

        response = dao.getURL(url, headers)

        cache_post_response = cache.processResponse(service, url, response)

        if cache_post_response != None:
            if "response" in cache_post_response:
                return cache_post_response["response"]

        return response

    def _postURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        response = dao.postURL(url, headers, body)
        return response

    def _deleteURL(self, service, url, headers):
        dao = self._getDAO()
        response = dao.deleteURL(url, headers)
        return response

    def _putURL(self, service, url, headers, body=None):
        dao = self._getDAO()
        response = dao.putURL(url, headers, body)
        return response


class SWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('sws', url, headers)

    def putURL(self, url, headers, body):
        return self._putURL('sws', url, headers, body)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_SWS_DAO_CLASS', SWSFile)


class PWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('pws', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_PWS_DAO_CLASS', PWSFile)


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


class Hfs_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('hfs', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_HFS_DAO_CLASS', HfsFile)


class Libraries_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('libraries', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_LIBRARIES_DAO_CLASS', LibrariesFile)


class Uwnetid_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('uwnetid', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_UWNETID_DAO_CLASS', UwnetidFile)


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
