from datetime import datetime
from django.test import TestCase
from restclients.test.bridge import FBridgeWS
from restclients.models.bridge import BridgeUser, BridgeCustomField
from restclients.bridge.user import get_user, get_all_users, update_user,\
    add_user


class BridgeTestUser(TestCase):

    def test_bridge_custom_field(self):
        bcf = BridgeCustomField()
        bcf.value_id = "1"
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEquals(bcf.to_json(),
                          {'id': '1',
                           'value': '787',
                           'custom_field_id': '5'})
        bcf = BridgeCustomField()
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEquals(bcf.to_json(),
                          {'custom_field_id': '5',
                           'value': '787'})

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
            self.assertEquals(user.uwnetid, "javerage")
            self.assertEquals(user.get_uid(), "javerage@uw.edu")
            self.assertEquals(
                str(user.updated_at), '2016-07-25 16:24:42.131000-07:00')
            self.assertEquals(
                str(user.logged_in_at), "2016-09-02 15:27:01.827000-07:00")
            # user.next_due_date
            self.assertEquals(user.completed_courses_count, 0)
            self.assertEquals(
                user.to_json(),
                {"first_name": "James",
                 "last_name": "Student",
                 "uid": "javerage@uw.edu",
                 "roles": [
                        {"permissions": [],
                         "id": "account_admin",
                         "name": "account_admin"}],
                 "full_name": "James Student",
                 "email": "javerage@uw.edu",
                 "custom_fields": [
                        {"id": "1",
                         "value": "9136CCB8F66711D5BE060004AC494FFE",
                         "custom_field_id": "5"}]})
            self.assertEquals(
                user.to_json_post(),
                {"first_name": "James",
                 "last_name": "Student",
                 "uid": "javerage@uw.edu",
                 "full_name": "James Student",
                 "email": "javerage@uw.edu",
                 "custom_fields": [
                     {"id": "1",
                      "value": "9136CCB8F66711D5BE060004AC494FFE",
                      "custom_field_id": "5"}
                     ]})

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
            self.assertEquals(len(user_list), 4)
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
            user = user_list[3]
            self.assertEquals(user.name, "None Average Student")
            self.assertEquals(user.bridge_id, "17")
            cus_field = user.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "00000000000000000000000000000001")

    def test_add_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            cus_fie = BridgeCustomField()
            cus_fie.field_id = BridgeCustomField.REGID_FIELD_ID
            cus_fie.name = BridgeCustomField.REGID_NAME
            cus_fie.value = "12345678901234567890123456789012"

            user = BridgeUser()
            user.uwnetid = "eight"
            user.full_name = "Eight Class Student"
            user.first_name = "Eight Class"
            user.last_name = "Student"
            user.email = "eight@uw.edu"
            user.custom_fields.append(cus_fie)

            added_users = add_user(user)
            self.assertEquals(len(added_users), 1)
            added = added_users[0]
            self.assertEquals(added.bridge_id, "123")
            self.assertEquals(added.name, "Eight Class Student")
            self.assertEquals(added.first_name, "Eight Class")
            self.assertEquals(added.last_name, "Student")
            self.assertEquals(added.full_name, "Eight Class Student")
            self.assertEquals(added.sortable_name, "Student, Eight Class")
            self.assertEquals(added.email, "eight@uw.edu")
            self.assertEquals(added.uwnetid, "eight")
            self.assertEquals(added.get_uid(), "eight@uw.edu")
            self.assertEquals(
                str(added.updated_at), '2016-09-06 21:42:48.821000-07:00')
            cus_field = added.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "12345678901234567890123456789012")
            self.assertEquals(cus_field.field_id, "5")
            self.assertEquals(cus_field.value_id, "922202")

    def test_update_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            orig_users = get_user('bill')
            upded_users = update_user(orig_users[0])
            self.assertEquals(len(upded_users), 1)
            upded = upded_users[0]
            self.assertEquals(upded.bridge_id, "17637")
            self.assertEquals(upded.name, "Bill Average Teacher")
            self.assertEquals(upded.first_name, "Bill Average")
            self.assertEquals(upded.last_name, "Teacher")
            self.assertEquals(upded.full_name, "Bill Average Teacher")
            self.assertEquals(upded.sortable_name, "Teacher, Bill Average")
            self.assertEquals(upded.email, "bill@u.washington.edu")
            self.assertEquals(upded.uwnetid, "bill")
            self.assertEquals(upded.get_uid(), "bill@uw.edu")
            self.assertEquals(
                str(upded.updated_at), '2016-09-08 13:58:20.635000-07:00')
            cus_field = upded.custom_fields[0]
            self.assertEquals(cus_field.value,
                              "FBB38FE46A7C11D5A4AE0004AC494FFE")
