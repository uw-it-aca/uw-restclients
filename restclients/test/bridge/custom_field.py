from datetime import datetime
from django.test import TestCase
from restclients.test.bridge import FBridgeWS
from restclients.bridge.custom_field import get_custom_fields,\
    get_regid_field_id, new_regid_custom_field


class TestBridgeCustomFields(TestCase):

    def test_get_custom_fields(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            fields = get_custom_fields()
            self.assertEqual(len(fields), 1)
            bcf = fields[0]
            self.assertEqual(bcf.field_id, "5")
            self.assertEqual(bcf.name, "REGID")

    def test_get_regid_field_id(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            self.assertEqual(get_regid_field_id(), "5")

    def test_new_regid_custom_field(self):
        with self.settings(RESTCLIENTS_BRIDGE_DAO_CLASS=FBridgeWS):
            regid = "12345678901234567890123456789012"
            cf = new_regid_custom_field(regid)
            self.assertEqual(cf.field_id, "5")
            self.assertEqual(cf.value, regid)
            self.assertEqual(cf.name, "REGID")
            self.assertIsNone(cf.value_id)
