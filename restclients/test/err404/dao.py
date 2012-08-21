from django.test import TestCase
from django.conf import settings
from restclients.dao import DAO

class TestDAO404(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_DAO_CLASS='restclients.dao_implementation.always404.Always404'):
            dao = DAO()
            response = dao.getURL("/v4/", {})
            self.assertEqual(response.status, 404, "Always 404 always returns a 404")
