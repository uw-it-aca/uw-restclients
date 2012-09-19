from django.test import TestCase
from django.conf import settings
from restclients.gws import GWS

class GWSGroupBasics(TestCase):

    def test_group_attributes(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    group = gws.get_group_by_id('u_acadev_tester')
                    self.assertEquals(group.name, "u_acadev_tester")


    def test_effective_group_membership(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    members = gws.get_effective_members('u_acadev_tester')

                    self.assertEquals(len(members), 3)
                    has_pmichaud = False
                    has_javerage = False
                    has_eight = False

                    for member in members:
                        if member.uwnetid == "pmichaud":
                            has_pmichaud = True
                        elif member.uwnetid == "javerage":
                            has_javerage = True
                        elif member.uwnetid == "eight":
                            has_eight = True

                    self.assertEquals(has_pmichaud, True)
                    self.assertEquals(has_javerage, True)
                    self.assertEquals(has_eight, True)
