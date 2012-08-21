from django.test import TestCase
from django.conf import settings
from restclients.dao import *

class SWSTestDAO500(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.errors.Always500'):
            dao = SWS_DAO()
            response = dao.getURL("/v4/", {})
            self.assertEqual(response.status, 500, "Always 500 always returns a 500")
