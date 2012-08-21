from django.test import TestCase
from django.conf import settings
from restclients.dao import *
from django.core.exceptions import *

class PWSTestInvalidDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.invalid.Always50000'):
            self.assertRaises(ImproperlyConfigured, PWS_DAO)
