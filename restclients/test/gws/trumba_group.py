from django.test import TestCase
from restclients.models.gws import GroupUser
from restclients.exceptions import DataFailureException
from restclients.gws import GWS
from restclients.test import fdao_gws_override


@fdao_gws_override
class TestGwsTrumbaGroup(TestCase):

    def test_get_group(self):
        group = GWS().get_group_by_id('u_eventcal_sea_1013649-editor')

        self.assertEquals(group.name, "u_eventcal_sea_1013649-editor")
        self.assertEquals(group.uwregid, "143bc3d173d244f6a2c3ced159ba9c97")
        self.assertEquals(group.title,
                          "College of Arts and Sciences calendar editor group")
        self.assertEquals(
            group.description,
            "Specifying the editors who are able to add/edit/delete any event on the corresponding Seattle Trumba calendar")

        self.assertIsNotNone(group.admins)
        self.assertEquals(len(group.admins) , 1)
        self.assertEquals(group.admins[0].user_type, GroupUser.GROUP_TYPE)
        self.assertEquals(group.admins[0].name, "u_eventcal_support")

        self.assertIsNotNone(group.updaters)
        self.assertEquals(len(group.updaters) , 1)
        self.assertEquals(group.updaters[0].user_type, GroupUser.GROUP_TYPE)
        self.assertEquals(
            group.updaters[0].name, "u_eventcal_sea_1013649-editor")

        self.assertIsNotNone(group.readers)
        self.assertEquals(len(group.readers) , 1)
        self.assertEquals(group.readers[0].user_type, GroupUser.NONE_TYPE)
        self.assertEquals(group.readers[0].name, "dc=all")

        self.assertIsNotNone(group.optouts)
        self.assertEquals(len(group.optouts) , 1)
        self.assertEquals(group.optouts[0].user_type, GroupUser.NONE_TYPE)
        self.assertEquals(group.optouts[0].name, "dc=all")
