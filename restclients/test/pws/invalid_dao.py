from django.test import TestCase
from django.conf import settings
from restclients.dao import *
from restclients_core.exceptions import ImproperlyConfigured

class PWSTestInvalidDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.invalid.Always50000'):
            dao = PWS_DAO()
            self.assertRaises(ImproperlyConfigured, dao.getURL, '/', {})
