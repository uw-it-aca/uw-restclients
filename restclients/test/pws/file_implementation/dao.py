from django.test import TestCase
from django.conf import settings
from restclients.dao import *
import re

class PWSTestFileDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            dao = SWS_DAO()
            response = dao.getURL("/file_doesnt_exist", {})
            self.assertEqual(response.status, 404, "File DAO returns a 404 for missing files")
