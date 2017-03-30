from datetime import datetime
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from restclients.exceptions import DataFailureException
from restclients.models.bridge import BridgeUser, BridgeCustomField,\
    BridgeUserRole
from restclients.test import fdao_pws_override


class TestBridgeModel(TestCase):

    def test_bridge_user_role(self):
        role = BridgeUserRole(role_id='user', name='user')
        self.assertEqual(role.to_json(),
                         {"id": "user", "name": "user"})

    def test_bridge_custom_field(self):
        bcf = BridgeCustomField(value_id="1",
                                field_id="5",
                                name="Regid",
                                value="787")
        self.assertEqual(bcf.to_json(),
                         {'id': '1',
                          'value': '787',
                          'custom_field_id': '5'})
        self.assertTrue(bcf.is_regid())
        self.assertEqual(bcf.value, '787')

        bcf = BridgeCustomField(field_id="5",
                                name="REGID")
        self.assertEqual(bcf.to_json(),
                         {'custom_field_id': '5',
                          'value': None})
        self.assertIsNotNone(str(bcf))

        bcf = BridgeCustomField(field_id="5",
                                name="REGID",
                                value="787")
        self.assertEqual(bcf.to_json(),
                         {'custom_field_id': '5',
                          'value': '787'})

    def test_bridge_user(self):
        bcf = BridgeCustomField(
            field_id="5",
            name="REGID",
            value="12345678901234567890123456789012")
        user = BridgeUser()
        user.netid = "iamstudent"
        user.full_name = "Iam Student"
        user.first_name = "Iam A"
        user.last_name = "Student"
        user.email = "iamstudent@uw.edu"
        user.custom_fields.append(bcf)
        user.updated_at = parse_datetime("2016-08-08T13:58:20.635-07:00")
        self.assertIsNotNone(str(user))
        self.assertFalse(user.has_course_summary())
        self.assertFalse(user.no_learning_history())
        self.assertEqual(user.get_uid(), "iamstudent@uw.edu")
        user = BridgeUser()
        user.netid = "iamstudent"
        user.full_name = "Iam Student"
        user.email = "iamstudent@uw.edu"
        user.custom_fields.append(bcf)
        user.completed_courses_count = 3
        self.assertTrue(user.has_course_summary())
        self.assertFalse(user.no_learning_history())
        self.assertIsNotNone(str(user))

    def test_to_json_patch(self):
        user = BridgeUser(netid="iamstudent",
                          full_name="Iam Student",
                          first_name="Iam A",
                          last_name="Student",
                          email="iamstudent@uw.edu"
                          )
        json_patch = user.to_json_patch()
        self.assertEqual(
            user.to_json_patch(),
            {'user': {
                'uid': 'iamstudent@uw.edu',
                'email': 'iamstudent@uw.edu',
                'first_name': 'Iam A',
                'last_name': 'Student',
                'full_name': 'Iam Student'}})

        user.bridge_id = 123
        self.assertTrue(user.has_bridge_id())
        self.assertEqual(
            user.to_json_patch(),
            {'user': {
                'id': 123,
                'uid': 'iamstudent@uw.edu',
                'email': 'iamstudent@uw.edu',
                'full_name': 'Iam Student',
                'first_name': 'Iam A',
                'last_name': 'Student'}})

        bcf = BridgeCustomField(field_id="5",
                                name="REGID",
                                value="12345678901234567890123456789012")
        user.custom_fields.append(bcf)
        json_patch = user.to_json_patch()
        self.assertEqual(
            user.to_json_patch(),
            {'user': {
                'id': 123,
                'uid': 'iamstudent@uw.edu',
                'email': 'iamstudent@uw.edu',
                'first_name': 'Iam A',
                'last_name': 'Student',
                'full_name': 'Iam Student',
                'custom_fields': [
                    {'custom_field_id': '5',
                     'value': '12345678901234567890123456789012'}],
                }})

    def test_to_json_post(self):
        bcf = BridgeCustomField(field_id="5",
                                name="REGID",
                                value="12345678901234567890123456789012")
        user = BridgeUser(netid="iamstudent",
                          full_name="Iam Student",
                          email="iamstudent@uw.edu"
                          )
        user.custom_fields.append(bcf)
        json_post = user.to_json_post()
        self.assertEqual(
            user.to_json_post(),
            {'users': [{
                'uid': 'iamstudent@uw.edu',
                'email': 'iamstudent@uw.edu',
                'full_name': 'Iam Student',
                'custom_fields': [
                    {'custom_field_id': '5',
                     'value': '12345678901234567890123456789012'}],
                }]})
        user.bridge_id = 123
        self.assertEqual(
            user.to_json_post(),
            {'users': [{
                'id': 123,
                'uid': 'iamstudent@uw.edu',
                'email': 'iamstudent@uw.edu',
                'full_name': 'Iam Student',
                'custom_fields': [
                    {'custom_field_id': '5',
                     'value': '12345678901234567890123456789012'}],
                }]})
