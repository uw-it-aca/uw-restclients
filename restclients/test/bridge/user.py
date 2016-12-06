from datetime import datetime
from django.test import TestCase
from restclients.test.bridge import FBridgeWS
from restclients.exceptions import DataFailureException
from restclients.models.bridge import BridgeUser, BridgeCustomField
from restclients.bridge.custom_field import new_regid_custom_field
from restclients.bridge.user import get_user, get_all_users, get_user_by_id,\
    add_user, admin_id_url, admin_uid_url, author_id_url,\
    author_uid_url, ADMIN_URL_PREFIX, AUTHOR_URL_PREFIX,\
    change_uid, replace_uid, restore_user_by_id, update_user,\
    restore_user, delete_user, delete_user_by_id


class TestBridgeUser(TestCase):

    def test_admin_id_url(self):
        self.assertEqual(admin_id_url(None),
                         ADMIN_URL_PREFIX)
        self.assertEqual(admin_id_url(123),
                         ADMIN_URL_PREFIX + '/123')

    def test_author_id_url(self):
        self.assertEqual(author_id_url(None),
                         AUTHOR_URL_PREFIX)
        self.assertEqual(author_id_url(123),
                         AUTHOR_URL_PREFIX + '/123')

    def test_admin_uid_url(self):
        self.assertEqual(admin_uid_url(None),
                         ADMIN_URL_PREFIX)
        self.assertEqual(admin_uid_url('staff'),
                         ADMIN_URL_PREFIX + '/uid%3Astaff%40uw%2Eedu')

    def test_author_uid_url(self):
        self.assertEqual(author_uid_url(None),
                         AUTHOR_URL_PREFIX)
        self.assertEqual(author_uid_url('staff'),
                         AUTHOR_URL_PREFIX + '/uid%3Astaff%40uw%2Eedu')

    def test_bridge_custom_field(self):
        bcf = BridgeCustomField()
        bcf.value_id = "1"
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEqual(bcf.to_json(),
                         {'id': '1',
                          'value': '787',
                          'name': 'REGID',
                          'custom_field_id': '5'})
        self.assertTrue(bcf.is_regid())
        self.assertEqual(bcf.value, '787')

        bcf = BridgeCustomField()
        bcf.field_id = "5"
        bcf.name = "REGID"
        bcf.value = "787"
        self.assertEqual(bcf.to_json(),
                         {'custom_field_id': '5',
                          'name': 'REGID',
                          'value': '787'})

    def test_get_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_user('javerage', include_course_summary=True)
            self.assertEqual(len(user_list), 1)
            user = user_list[0]
            self.assertEqual(user.bridge_id, 195)
            self.assertEqual(user.name, "James Average Student")
            self.assertEqual(user.first_name, "James")
            self.assertEqual(user.last_name, "Student")
            self.assertEqual(user.full_name, "James Student")
            self.assertEqual(user.sortable_name, "Student, James Average")
            self.assertEqual(user.email, "javerage@uw.edu")
            self.assertEqual(user.netid, "javerage")
            self.assertEqual(user.get_uid(), "javerage@uw.edu")
            self.assertEqual(
                str(user.updated_at), '2016-07-25 16:24:42.131000-07:00')
            self.assertEqual(
                str(user.logged_in_at), "2016-09-02 15:27:01.827000-07:00")
            self.assertEqual(user.next_due_date, None)
            self.assertEqual(user.completed_courses_count, 0)
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
                        "name": "REGID",
                        "custom_field_id": "5"}
                       ]}]})

            self.assertEqual(len(user.custom_fields), 1)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value_id, "1")
            self.assertEqual(cus_field.field_id, "5")
            self.assertEqual(cus_field.name, "REGID")
            self.assertEqual(cus_field.value,
                             "9136CCB8F66711D5BE060004AC494FFE")

            user_list = get_user('bill', include_course_summary=True)
            self.verify_bill(user_list)
            user_list = get_user_by_id(17637,  include_course_summary=True)
            self.verify_bill(user_list)

            self.assertRaises(DataFailureException,
                              get_user, 'bill')
            self.assertRaises(DataFailureException,
                              get_user_by_id, 17637)

    def verify_bill(self, user_list):
        self.assertEqual(len(user_list), 1)
        user = user_list[0]
        self.assertEqual(user.name, "Bill Average Teacher")
        self.assertEqual(user.bridge_id, 17637)
        self.assertEqual(user.first_name, "Bill Average")
        self.assertEqual(user.last_name, "Teacher")
        self.assertEqual(user.full_name, "Bill Average Teacher")
        self.assertEqual(user.sortable_name, "Teacher, Bill Average")
        self.assertEqual(user.email, "bill@u.washington.edu")
        self.assertEqual(user.netid, "bill")
        self.assertEqual(user.get_uid(), "bill@uw.edu")
        cus_field = user.custom_fields[0]
        self.assertEqual(cus_field.value,
                         "FBB38FE46A7C11D5A4AE0004AC494FFE")

    def test_get_alluser(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            user_list = get_all_users(include_course_summary=True)
            self.assertEqual(len(user_list), 4)
            user = user_list[0]
            self.assertEqual(user.name, "Bill Average Teacher")
            self.assertEqual(user.bridge_id, 17637)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "FBB38FE46A7C11D5A4AE0004AC494FFE")
            user = user_list[1]
            self.assertEqual(user.name, "Eight Class Student")
            self.assertEqual(user.bridge_id, 106)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "12345678901234567890123456789012")
            user = user_list[2]
            self.assertEqual(user.name, "James Student")
            self.assertEqual(user.bridge_id, 195)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "9136CCB8F66711D5BE060004AC494FFE")
            user = user_list[3]
            self.assertEqual(user.name, "None Average Student")
            self.assertEqual(user.bridge_id, 17)
            cus_field = user.custom_fields[0]
            self.assertEqual(cus_field.value,
                             "00000000000000000000000000000001")

    def test_add_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            regid = "12345678901234567890123456789012"
            cus_fie = new_regid_custom_field(regid)
            user = BridgeUser()
            user.netid = "eight"
            user.full_name = "Eight Class Student"
            user.first_name = "Eight Class"
            user.last_name = "Student"
            user.email = "eight@uw.edu"
            user.custom_fields.append(cus_fie)

            added_users = add_user(user)
            self.assertEqual(len(added_users), 1)
            added = added_users[0]
            self.assertEqual(added.bridge_id, 123)
            self.assertEqual(added.name, "Eight Class Student")
            self.assertEqual(added.first_name, "Eight Class")
            self.assertEqual(added.last_name, "Student")
            self.assertEqual(added.full_name, "Eight Class Student")
            self.assertEqual(added.sortable_name, "Student, Eight Class")
            self.assertEqual(added.email, "eight@uw.edu")
            self.assertEqual(added.netid, "eight")
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
            self.assertTrue(delete_user("javerage"))
            self.assertTrue(delete_user_by_id(195))
            try:
                reps = delete_user("staff")
            except Exception as ex:
                self.assertEqual(ex.status, '404')

    def test_update_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            orig_users = get_user('bill', include_course_summary=True)
            upded_users = update_user(orig_users[0])
            self.verify_bill(upded_users)
            self.assertEqual(
                str(upded_users[0].updated_at),
                '2016-09-08 13:58:20.635000-07:00')

            orig_users = get_user('bill', include_course_summary=True)
            upded_users = update_user(orig_users[0])
            self.verify_bill(upded_users)

    def test_change_uid(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            self.verify_uid(change_uid(17637, "billchanged"))
            self.verify_uid(replace_uid("bill", "billchanged"))

    def test_restore_user(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            self.verify_uid(restore_user_by_id(17637))
            self.verify_uid(restore_user("billchanged"))

    def verify_uid(self, users):
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].bridge_id, 17637)
        self.assertEqual(users[0].get_uid(), "billchanged@uw.edu")
