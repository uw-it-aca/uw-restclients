from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao_implementation.pws import File as PWSFile
from restclients.dao_implementation.sws import File as SWSFile

class SWS_DAO(object):
    def __new__(*args, **named_args):
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
                raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))

            return DAOModule()
        else:
            return SWSFile()

class PWS_DAO(object):
    def __new__(*args, **named_args):
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
                raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))

            return DAOModule()
        else:
            return PWSFile()

