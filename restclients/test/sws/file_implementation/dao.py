from django.test import TestCase
from django.conf import settings
from restclients.dao import *
import re

class SWSTestFileDAO(TestCase):
    def test_dao_response(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            dao = SWS_DAO()
            response = dao.getURL("/file_doesnt_exist", {})
            self.assertEqual(response.status, 404, "File DAO returns a 404 for missing files")

            response = dao.getURL("/student/", {})
            self.assertEqual(response.status, 200, "File DAO returns 200 for found files")

            html = response.read()
            if not re.search('student/v4', html):
                self.fail("Doesn't contains a link to v4")

            if re.search('student/v2', html):
                self.fail("shouldn't contain a link to v2")
