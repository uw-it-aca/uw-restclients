from datetime import datetime
from django.test import TestCase
from restclients.test.bridge import FBridgeWS
from restclients.models.bridge import BridgeUser, BridgeCustomField
from restclients.bridge.user import get_user, get_all_users, update_user,\
    add_user, delete_user


class BridgeTestUser(TestCase):

    def test_bridge_custom_field(self):
        bcf = BridgeCustomField()
        bcf.value_id = "1"
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEqual(bcf.to_json(),
                         {'id': '1',
                          'value': '787',
                          'custom_field_id': '5'})
        bcf = BridgeCustomField()
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEqual(bcf.to_json(),
                         {'custom_field_id': '5',
                          'value': '787'})

    def test_get_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_user('javerage')
            self.assertEqual(len(user_list), 1)
            user = user_list[0]
            self.assertEqual(user.bridge_id, "195")
            self.assertEqual(user.name, "James Average Student")
            self.assertEqual(user.first_name, "James")
            self.assertEqual(user.last_name, "Student")
            self.assertEqual(user.full_name, "James Student")
            self.assertEqual(user.sortable_name, "Student, James Average")
            self.assertEqual(user.email, "javerage@uw.edu")
            self.assertEqual(user.uwnetid, "javerage")
            self.assertEqual(user.get_uid(), "javerage@uw.edu")
            self.assertEqual(
                str(user.updated_at), '2016-07-25 16:24:42.131000-07:00')
            self.assertEqual(
                str(user.logged_in_at), "2016-09-02 15:27:01.827000-07:00")
            self.assertEqual(user.next_due_date, None)
            self.assertEqual(user.completed_courses_count, 0)
            self.assertEqual(
                user.to_json(),
                {"users":[
                  {"first_name": "James",
                   "last_name": "Student",
                   "uid": "javerage@uw.edu",
                   "roles": [
                        {
                         "id": "account_admin",
                         "name": "account_admin",
                         "permissions": []
                         }],
                   "full_name": "James Student",
                   "email": "javerage@uw.edu",
                   "custom_fields": [
                        {"id": "1",
                         "value": "9136CCB8F66711D5BE060004AC494FFE",
                         "custom_field_id": "5"}]}]})
            self.assertEqual(
                user.to_json_post(),
                {"users":[
                   {"first_name": "James",
                    "last_name": "Student",
                    "uid": "javerage@uw.edu",
                    "full_name": "James Student",
                    "email": "javerage@uw.edu",
                    "custom_fields": [
                       {"id": "1",
                        "value": "9136CCB8F66711D5BE060004AC494FFE",
                        "custom_field_id": "5"}
                       ]}]})

            self.assertEqual(len(user.custom_fields), 1)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value_id, "1")
            self.assertEqual(cus_field.field_id, "5")
            self.assertEqual(cus_field.name, "REGID")
            self.assertEqual(cus_field.value,
                             "9136CCB8F66711D5BE060004AC494FFE")
            user_list = get_user('bill')
            self.assertEqual(len(user_list), 1)
            user = user_list[0]
            self.assertEqual(user.name, "Bill Average Teacher")
            self.assertEqual(user.bridge_id, "17637")
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "FBB38FE46A7C11D5A4AE0004AC494FFE")

    def test_get_alluser(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_all_users()
            self.assertEqual(len(user_list), 4)
            user = user_list[0]
            self.assertEqual(user.name, "Bill Average Teacher")
            self.assertEqual(user.bridge_id, "17637")
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "FBB38FE46A7C11D5A4AE0004AC494FFE")
            user = user_list[1]
            self.assertEqual(user.name, "Eight Class Student")
            self.assertEqual(user.bridge_id, "106")
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "12345678901234567890123456789012")
            user = user_list[2]
            self.assertEqual(user.name, "James Student")
            self.assertEqual(user.bridge_id, "195")
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "9136CCB8F66711D5BE060004AC494FFE")
            user = user_list[3]
            self.assertEqual(user.name, "None Average Student")
            self.assertEqual(user.bridge_id, "17")
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
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
            self.assertEqual(len(added_users), 1)
            added = added_users[0]
            self.assertEqual(added.bridge_id, "123")
            self.assertEqual(added.name, "Eight Class Student")
            self.assertEqual(added.first_name, "Eight Class")
            self.assertEqual(added.last_name, "Student")
            self.assertEqual(added.full_name, "Eight Class Student")
            self.assertEqual(added.sortable_name, "Student, Eight Class")
            self.assertEqual(added.email, "eight@uw.edu")
            self.assertEqual(added.uwnetid, "eight")
            self.assertEqual(added.get_uid(), "eight@uw.edu")
            self.assertEqual(
                str(added.updated_at), '2016-09-06 21:42:48.821000-07:00')
            cus_field = added.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "12345678901234567890123456789012")
            self.assertEqual(cus_field.field_id, "5")
            self.assertEqual(cus_field.value_id, "922202")

    def test_delete_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            reps = delete_user("javerage")
            self.assertEqual(reps.status, 204)
            try:
                reps = delete_user("staff")
            except Exception as ex:
                self.assertEqual(ex.status, '404')

    def test_update_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            orig_users = get_user('bill')
            upded_users = update_user(orig_users[0])
            self.assertEqual(len(upded_users), 1)
            upded = upded_users[0]
            self.assertEqual(upded.bridge_id, "17637")
            self.assertEqual(upded.name, "Bill Average Teacher")
            self.assertEqual(upded.first_name, "Bill Average")
            self.assertEqual(upded.last_name, "Teacher")
            self.assertEqual(upded.full_name, "Bill Average Teacher")
            self.assertEqual(upded.sortable_name, "Teacher, Bill Average")
            self.assertEqual(upded.email, "bill@u.washington.edu")
            self.assertEqual(upded.uwnetid, "bill")
            self.assertEqual(upded.get_uid(), "bill@uw.edu")
            self.assertEqual(
                str(upded.updated_at), '2016-09-08 13:58:20.635000-07:00')
            cus_field = upded.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "FBB38FE46A7C11D5A4AE0004AC494FFE")
