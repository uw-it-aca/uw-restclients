from django.test import TestCase
from django.conf import settings
from restclients.dao import *
from django.core.exceptions import *

class TestInvalidDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.always404.Always500'):
            self.assertRaises(ImproperlyConfigured, SWS_DAO)
