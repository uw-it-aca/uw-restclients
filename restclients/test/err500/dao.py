from django.test import TestCase
from django.conf import settings
from restclients.dao import DAO

class TestDAO500(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_DAO_CLASS='restclients.dao_implementation.always500.Always500'):
            dao = DAO()
            response = dao.getURL("/v4/", {})
            self.assertEqual(response.status, 500, "Always 500 always returns a 500")
