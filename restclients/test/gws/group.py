from django.test import TestCase
from restclients.gws import GWS
from restclients.models.gws import Group, GroupUser, GroupMember
from restclients.exceptions import DataFailureException
from restclients.test import fdao_gws_override


@fdao_gws_override
class GWSGroupBasics(TestCase):
    def test_get_nonexistant_group(self):
        gws = GWS()
        self.assertRaises(DataFailureException,
                          gws.get_group_by_id,
                          "u_acadev_nonexistant_tester")

    def test_get_group(self):
        gws = GWS()
        group = gws.get_group_by_id('u_acadev_tester')
        self.assertEquals(group.name, "u_acadev_tester")

    def test_create_group(self):
        gws = GWS()
        group = Group(name="u_acadev_tester2",
                      title="New ACA Tester")
        group.admins = [GroupUser(user_type="uwnetid", name="acadev")]
        group.readers = [GroupUser(user_type="none", name="dc=all")]

        new_group = gws._group_from_xhtml(gws._xhtml_from_group(group))

        self.assertEquals(new_group.title, group.title)

    def test_update_group(self):
        gws = GWS()
        group = gws.get_group_by_id("u_acadev_tester")
        group.title = "ACA Tester"

        new_group = gws._group_from_xhtml(gws._xhtml_from_group(group))

        self.assertEquals(new_group.title, group.title)

    def test_delete_group(self):
        gws = GWS()
        group = Group(name='u_acadev_tester')
        result = gws.delete_group(group.name)
        self.assertEquals(result, True)

    def test_group_membership(self):
        gws = GWS()
        members = gws.get_members('u_acadev_unittest')
        self.assertEquals(len(members), 2)

    def test_update_members(self):
        gws = GWS()
        members = gws.get_members('u_acadev_unittest')

        members.remove(GroupMember(member_type="uwnetid", name="eight"))
        members.append(GroupMember(member_type="uwnetid", name="seven"))

        not_found_members = gws.update_members('u_acadev_unittest',
                                               members)
        self.assertEquals(len(not_found_members), 0)

    def test_effective_group_membership(self):
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

        count = gws.get_effective_member_count('u_acadev_unittest')
        self.assertEquals(count, 3)

    def test_is_effective_member(self):
        gws = GWS()

        self.assertEquals(
            gws.is_effective_member('u_acadev_unittest', 'pmichaud'), True)
        self.assertEquals(
            gws.is_effective_member('u_acadev_unittest',
                                    'pmichaud@washington.edu'), True)
        self.assertEquals(
            gws.is_effective_member('u_acadev_unittest', 'javerage'), True)
        self.assertEquals(
            gws.is_effective_member('u_acadev_unittest', 'eight'), True)
        self.assertEquals(
            gws.is_effective_member('u_acadev_unittest', 'not_member'), False)
