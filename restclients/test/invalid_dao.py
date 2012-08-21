from django.test import TestCase
from django.conf import settings
from restclients.dao import DAO
from django.core.exceptions import *

class TestInvalidDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_DAO_CLASS='restclients.dao_implementation.always404.Always500'):
            self.assertRaises(ImproperlyConfigured, DAO)
