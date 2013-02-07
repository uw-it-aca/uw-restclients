from django.test import TestCase
from django.conf import settings
from restclients.gws import GWS

class GWSGroupSearch(TestCase):

    def test_search(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    groups = gws.search_groups(member="javerage")
                    self.assertEquals(len(groups), 15)
