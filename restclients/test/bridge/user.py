from django.test import TestCase
from restclients.test.bridge import FBridgeWS
from restclients.models.bridge import BridgeUser
from restclients.bridge.user import get_user, get_all_users


class BridgeTestUser(TestCase):

    def test_get_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_user('javerage')
            self.assertEquals(len(user_list), 1)
            user = user_list[0]
            self.assertEquals(user.bridge_id, "195")
            self.assertEquals(user.name, "James Average Student")
            self.assertEquals(user.first_name, "James")
            self.assertEquals(user.last_name, "Student")
            self.assertEquals(user.full_name, "James Student")
            self.assertEquals(user.sortable_name, "Student, James Average")
            self.assertEquals(user.email, "javerage@uw.edu")
            self.assertEquals(len(user.custom_fields), 1)
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value_id, "1")
            self.assertEquals(cus_field.field_id, "5")
            self.assertEquals(cus_field.name, "REGID")
            self.assertEquals(cus_field.value,
                              "9136CCB8F66711D5BE060004AC494FFE")
            user_list = get_user('bill')
            self.assertEquals(len(user_list), 1)
            user = user_list[0]
            self.assertEquals(user.name, "Bill Average Teacher")
            self.assertEquals(user.bridge_id, "17637")
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "FBB38FE46A7C11D5A4AE0004AC494FFE")

    def test_get_alluser(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_all_users()
            self.assertEquals(len(user_list), 3)
            user = user_list[0]
            self.assertEquals(user.name, "Bill Average Teacher")
            self.assertEquals(user.bridge_id, "17637")
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "FBB38FE46A7C11D5A4AE0004AC494FFE")
            user = user_list[1]
            self.assertEquals(user.name, "Eight Class Student")
            self.assertEquals(user.bridge_id, "106")
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "12345678901234567890123456789012")
            user = user_list[2]
            self.assertEquals(user.name, "James Student")
            self.assertEquals(user.bridge_id, "195")
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "9136CCB8F66711D5BE060004AC494FFE")
