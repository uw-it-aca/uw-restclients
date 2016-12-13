from django.test import TestCase
from restclients.gws import GWS
from restclients.test import fdao_gws_override


@fdao_gws_override
class GWSGroupSearch(TestCase):

    def test_search(self):
        gws = GWS()
        groups = gws.search_groups(member="javerage")
        self.assertEquals(len(groups), 15)
