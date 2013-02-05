from django.test import TestCase
from django.conf import settings
from restclients.gws import GWS
from restclients.models import Group

class GWSGroupBasics(TestCase):

    def test_get_group(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    group = gws.get_group_by_id('u_acadev_tester')
                    self.assertEquals(group.name, "u_acadev_tester")

    def test_update_group(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    group = gws.get_group_by_id("u_acadev_tester")
                    group.title = "ACA Tester"
                    new_group = gws.update_group(group)
                    self.assertEquals(new_group.title, group.title)

    def test_delete_group(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    group = Group(name='u_acadev_tester')
                    result = gws.delete_group(group)
                    self.assertEquals(result, True)

    def test_effective_group_membership(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    members = gws.get_effective_members('u_acadev_unittest')

                    self.assertEquals(len(members), 3)
                    has_pmichaud = False
                    has_javerage = False
                    has_eight = False

                    for member in members:
                        if member.name == "pmichaud":
                            has_pmichaud = True
                        elif member.name == "javerage":
                            has_javerage = True
                        elif member.name == "eight":
                            has_eight = True

                    self.assertEquals(has_pmichaud, True)
                    self.assertEquals(has_javerage, True)
                    self.assertEquals(has_eight, True)

    def test_is_effective_member(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()

                    self.assertEquals(gws.is_effective_member('u_acadev_unittest', 'pmichaud'), True)
                    self.assertEquals(gws.is_effective_member('u_acadev_unittest', 'javerage'), True)
                    self.assertEquals(gws.is_effective_member('u_acadev_unittest', 'eight'), True)
                    self.assertEquals(gws.is_effective_member('u_acadev_unittest', 'not_member'), False)
