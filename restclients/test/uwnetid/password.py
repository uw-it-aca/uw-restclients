from datetime import date
from django.test import TestCase
from restclients.uwnetid.password import get_uwnetid_password
from restclients.exceptions import DataFailureException
from restclients.test import fdao_uwnetid_override


@fdao_uwnetid_override
class UwPassword(TestCase):

    def test_get_uwnetid_password(self):
        pw = get_uwnetid_password("javerage")
        self.assertEquals(len(pw.netid_status), 2)
        self.assertEquals(pw.netid_status[0], "Person")
        self.assertEquals(pw.netid_status[1], "Active")
        self.assertTrue(pw.is_active_person())
        self.assertTrue(pw.is_kerb_status_active())
        self.assertEqual(str(pw.last_change), '2015-01-27 10:49:42-08:00')
        self.assertEqual(str(pw.time_stamp), '2016-12-16 14:21:40-08:00')
        self.assertEqual(str(pw.time_stamp,), '2016-12-16 14:21:40-08:00')
        self.assertEqual(pw.minimum_length, 8)

        pw = get_uwnetid_password("bill")
        self.assertEquals(len(pw.netid_status), 2)
        self.assertEquals(pw.netid_status[0], "Person")
        self.assertEquals(pw.netid_status[1], "Active")
        self.assertTrue(pw.is_active_person())
        self.assertTrue(pw.is_kerb_status_active())
        self.assertEqual(str(pw.last_change), '2016-10-13 10:33:52-07:00')
        self.assertEqual(str(pw.time_stamp), '2016-12-16 14:23:11-08:00')
        self.assertEqual(str(pw.expires_med), '2017-02-10 10:57:06-08:00')
        self.assertEqual(str(pw.last_change_med), '2016-10-13 10:57:06-07:00')
        self.assertEqual(pw.get_med_interval_day(), 120)
        self.assertEqual(pw.minimum_length, 8)
