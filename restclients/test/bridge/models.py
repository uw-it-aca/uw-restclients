from datetime import datetime
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from restclients.exceptions import DataFailureException
from restclients.models.bridge import BridgeUser, BridgeCustomField
from restclients.test import fdao_pws_override


class TestBridgeModel(TestCase):

    def test_bridge_custom_field(self):
        bcf = BridgeCustomField(value_id="1",
                                field_id="5",
                                name="REGID",
                                value="787")
        self.assertEqual(bcf.to_json(),
                         {'id': '1',
                          'value': '787',
                          'name': 'REGID',
                          'custom_field_id': '5'})
        self.assertTrue(bcf.is_regid())

        bcf = BridgeCustomField(field_id="5",
                                name="REGID")
        self.assertEqual(bcf.to_json(),
                         {'name': 'REGID',
                          'custom_field_id': '5',
                          'value': None})
        self.assertIsNotNone(str(bcf))

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
        self.assertEqual(
            user.to_json_post(),
            {'users': [
                    {'custom_fields': [
                            {'custom_field_id': '5',
                             'name': 'REGID',
                             'value': '12345678901234567890123456789012'}],
                     'uid': 'iamstudent@uw.edu',
                     'email': 'iamstudent@uw.edu',
                     'first_name': 'Iam A',
                     'full_name': 'Iam Student',
                     'last_name': 'Student'
                     }]})
        self.assertIsNotNone(str(user))
        self.assertFalse(user.has_course_summary())
        self.assertFalse(user.no_learning_history())
        self.assertEqual(user.get_uid(), "iamstudent@uw.edu")
        user = BridgeUser()
        user.netid = "iamstudent"
        user.full_name = "Iam Student"
        user.email = "iamstudent@uw.edu"
        user.custom_fields.append(bcf)
        self.assertEqual(
            user.to_json_post(),
            {'users': [
                    {'custom_fields': [
                            {'custom_field_id': '5',
                             'name': 'REGID',
                             'value': '12345678901234567890123456789012'}],
                     'email': 'iamstudent@uw.edu',
                     'full_name': 'Iam Student',
                     'uid': 'iamstudent@uw.edu'}]})

        user.bridge_id = 123
        self.assertEqual(
            user.to_json_post(),
            {'users': [
                    {'custom_fields': [
                            {'custom_field_id': '5',
                             'name': 'REGID',
                             'value': '12345678901234567890123456789012'}],
                     'id': 123,
                     'email': 'iamstudent@uw.edu',
                     'full_name': 'Iam Student',
                     'uid': 'iamstudent@uw.edu'}]})
        user.completed_courses_count = 3
        self.assertTrue(user.has_course_summary())
        self.assertFalse(user.no_learning_history())
        self.assertIsNotNone(str(user))
