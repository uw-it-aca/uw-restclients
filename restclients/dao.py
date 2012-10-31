from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao_implementation.pws import File as PWSFile
from restclients.dao_implementation.sws import File as SWSFile
from restclients.dao_implementation.gws import File as GWSFile
from restclients.dao_implementation.book import File as BookFile
from restclients.dao_implementation.amazon_sqs import Local as SQSLocal
from restclients.cache_implementation import NoCache


class MY_DAO(object):
    def _getCache(self):
        if hasattr(settings, 'RESTCLIENTS_DAO_CACHE_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_DAO_CACHE_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                CacheModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class' % (module, attr))

            return CacheModule()
        else:
            return NoCache()

    def _getURL(self, service, url, headers):
        dao = self._getDAO()
        cache = self._getCache()
        cache_response = cache.getCache(service, url, headers)
        if cache_response != None:
            if "response" in cache_response:
                return cache_response["response"]
            if "headers" in cache_response:
                headers = cache_response["headers"]

        response = dao.getURL(url, headers)

        cache_post_response = cache.processResponse(service, url, response)

        if cache_post_response != None:
            if "response" in cache_post_response:
                return cache_post_response["response"]

        return response


class SWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('sws', url, headers)

    def _getDAO(self):
        if hasattr(settings, 'RESTCLIENTS_SWS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_SWS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class' % (module, attr))

            return DAOModule()
        else:
            return SWSFile()


class PWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('pws', url, headers)

    def _getDAO(self):
        if hasattr(settings, 'RESTCLIENTS_PWS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_PWS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return PWSFile()


class GWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('gws', url, headers)

    def _getDAO(self):
        if hasattr(settings, 'RESTCLIENTS_GWS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_GWS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return GWSFile()


class Book_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('books', url, headers)

    def _getDAO(self):
        if hasattr(settings, 'RESTCLIENTS_BOOK_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_BOOK_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return BookFile()


class AmazonSQS_DAO(MY_DAO):
    def create_queue(self, queue_name):
        dao = self._getDAO()
        return dao.create_queue(queue_name)

    def get_queue(self, queue_name):
        dao = self._getDAO()
        res = dao.get_queue(queue_name)
        return res

    def _getDAO(self):
        if hasattr(settings, 'AMAZON_SQS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.AMAZON_SQS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return SQSLocal()


class SMS_DAO(MY_DAO):
    def create_message(self, to, body):
        dao = self._getDAO()
        return dao.create_message(to, body)

    def send_message(self, message):
        dao = self._getDAO()
        return dao.send_message(message)

    def _getDAO(self):
        if hasattr(settings, 'SMS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.SMS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return SMSLocal()


class NWS_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('nws', url, headers)

    def _getDAO(self):
        if hasattr(settings, 'RESTCLIENTS_NWS_DAO_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.RESTCLIENTS_NWS_DAO_CLASS.rsplit('.', 1)
            try:
                mod = import_module(module)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                           (module, e))
            try:
                DAOModule = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a '
                                   '"%s" class ' % (module, attr))

            return DAOModule()
        else:
            return NWSFile()
