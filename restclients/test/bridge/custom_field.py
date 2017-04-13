from datetime import datetime
from django.test import TestCase
from restclients.bridge.custom_field import get_custom_fields,\
    get_regid_field_id, new_regid_custom_field
from restclients.test import fdao_bridge_override


@fdao_bridge_override
class TestBridgeCustomFields(TestCase):

    def test_get_custom_fields(self):
        fields = get_custom_fields()
        self.assertEqual(len(fields), 1)
        bcf = fields[0]
        self.assertEqual(bcf.field_id, "5")
        self.assertTrue(bcf.is_regid())
        self.assertEqual(
            str(bcf),
            '{"name": "REGID", "value": null, "custom_field_id": "5"}')

    def test_get_regid_field_id(self):
        self.assertEqual(get_regid_field_id(), "5")

    def test_new_regid_custom_field(self):
        regid = "12345678901234567890123456789012"
        cf = new_regid_custom_field(regid)
        self.assertEqual(cf.field_id, "5")
        self.assertEqual(cf.value, regid)
        self.assertIsNone(cf.value_id)
        self.assertTrue(cf.is_regid())
        self.assertEqual(
            str(cf),
            ('{"name": "regid", "value": "12345678901234567890123456789012",'
             ' "custom_field_id": "5"}'))
