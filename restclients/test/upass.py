from django.test import TestCase
from restclients.upass import get_upass_url, get_upass_status
from restclients.models.upass import UPassStatus
from restclients.exceptions import DataFailureException
from restclients.test import fdao_upass_override


@fdao_upass_override
class UPassTest(TestCase):
    def test_javerage(self):
        status = get_upass_status("javerage")
        self.assertTrue(status.is_current)
        self.assertTrue(status.is_student)
        self.assertFalse(status.is_employee)
        status_json = status.json_data()
        self.assertIsNotNone(status_json['status_message'])
        self.assertTrue(status_json['is_current'])
        self.assertFalse(status_json['is_employee'])
        self.assertIsNotNone(str(status))

        status = get_upass_status("javeragefac")
        self.assertTrue(status.is_current)
        self.assertTrue(status.is_employee)

        status = get_upass_status("phil")
        self.assertFalse(status.is_current)
        self.assertFalse(status.is_student)

        self.assertRaises(DataFailureException,
                          get_upass_status,
                          "none")

        self.assertRaises(Exception,
                          get_upass_status,
                          "jerror")

    def test_get_url(self):
        self.assertEquals(get_upass_url("javerage"),
                          "/upass/MyUWUpass.aspx?id=javerage")

    def test_message_parsing(self):
        fac_message = ("<p><span class='highlight'>Your Faculty/Staff U-PASS"
                       " Membership is current.</span></p><p>It can take 24 to"
                       " 48 hours after purchase or Husky Card replacement"
                       " for your U-PASS to be transmitted to ORCA readers."
                       "  You must tap your card on an ORCA reader within 60"
                       " days from purchase or receiving a replacement Husky"
                       " Card.  This updates your smart chip and finalizes"
                       " activation of your U-PASS.</p><p><a"
                       " href='http://www.washington.edu/u-pass'>Learn more"
                       "</a> about U-PASS program member benefits, finalizing"
                       " activation, and the U-PASS terms of use.</p>")
        stu_message = ("<p><span class='highlight'>Your Student U-PASS "
                       "Membership is current.</span></p><p>It can take 24 "
                       "to 48 hours after issuance or Husky Card replacement "
                       "for your U-PASS to be transmitted to ORCA readers.  "
                       "You must tap your card on an ORCA reader within 60 "
                       "days from U-PASS issuance or receiving a replacement "
                       "Husky Card.  This updates your smart chip and "
                       "finalizes activation of your U-PASS.</p><p><a "
                       "href='http://www.washington.edu/u-pass'>Learn more</a>"
                       " about U-PASS program member benefits and finalizing "
                       "activation.</p>")
        not_current = ("<p><span class='highlight'>Your U-PASS is not current."
                       "</span></p><p>"
                       "<a href='http://www.washington.edu/u-pass'>Learn more"
                       "</a> about U-PASS program member benefits.</p>")

        nc_status = UPassStatus.create(not_current)
        self.assertFalse(nc_status.is_current)
        self.assertFalse(nc_status.is_employee)
        self.assertFalse(nc_status.is_student)

        stu_status = UPassStatus.create(stu_message)
        self.assertTrue(stu_status.is_current)
        self.assertFalse(stu_status.is_employee)
        self.assertTrue(stu_status.is_student)

        fac_status = UPassStatus.create(fac_message)
        self.assertTrue(fac_status.is_current)
        self.assertTrue(fac_status.is_employee)
        self.assertFalse(fac_status.is_student)
