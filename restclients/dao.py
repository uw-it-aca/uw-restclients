from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao_implementation.pws import File as PWSFile
from restclients.dao_implementation.sws import File as SWSFile
from restclients.cache_implementation import NoCache

class MY_DAO(object):
    def _getCache(self):
        if hasattr(settings, 'DAO_CACHE_CLASS'):
            # This is all taken from django's static file finder
            module, attr = settings.DAO_CACHE_CLASS.rsplit('.', 1)
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
