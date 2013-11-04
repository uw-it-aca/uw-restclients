from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.trumba.calendar import Calendar
from restclients.trumba.exceptions import TrumbaException, CalendarNotExist, CalendarOwnByDiffAccount, NoDataReturned, UnknownError

class TrumbaTestCalendars(TestCase):

    def test_get_bot_calendars_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_BOT_DAO_CLASS='restclients.dao_implementation.trumba.FileBot'
            ):
            result = Calendar.get_bot_calendars()
            self.assertTrue(result is not None and len(result) == 4)

    def test_get_sea_calendars_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            result = Calendar.get_sea_calendars()
            self.assertTrue(result is not None and len(result) == 10)

            cal_grp = result[0]
            self.assertEqual(cal_grp.calendarid, 11)
            self.assertEqual(cal_grp.campus, 'sea')
            self.assertEqual(cal_grp.name, 'Seattle calendar')
            self.assertTrue(cal_grp.is_sea())
            self.assertFalse(cal_grp.is_bot())
            self.assertFalse(cal_grp.is_tac())
            self.assertEqual(cal_grp.get_uw_editor_groupid(),
                             'u_eventcal_sea_11-editor')
            self.assertEqual(cal_grp.get_uw_showon_groupid(),
                             'u_eventcal_sea_11-showon')
            
            cal_grp = result[9]
            self.assertEqual(cal_grp.calendarid, 11321)
            self.assertEqual(cal_grp.campus, 'sea')
            self.assertEqual(cal_grp.name, 'Seattle child-sub-sub-calendar321')
            self.assertTrue(cal_grp.is_sea())
            self.assertFalse(cal_grp.is_bot())
            self.assertFalse(cal_grp.is_tac())
            self.assertEqual(cal_grp.get_uw_editor_groupid(),
                             'u_eventcal_sea_11321-editor')
            self.assertEqual(cal_grp.get_uw_showon_groupid(),
                             'u_eventcal_sea_11321-showon')
            
    def test_get_tac_calendars_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_TAC_DAO_CLASS='restclients.dao_implementation.trumba.FileTac'
            ):
            self.assertTrue(Calendar.get_tac_calendars() is None)
            

    def test_get_sea_permissions_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            result = Calendar.get_sea_permissions(1)
            self.assertTrue(result is not None and len(result) == 3)
            perm = result[0]
            self.assertEqual(perm.calendarid, 1)
            self.assertEqual(perm.campus, 'sea')
            self.assertEqual(perm.name, 'Dummy publisher')
            self.assertEqual(perm.uwnetid, 'dummyp')
            self.assertEqual(perm.level, 'PUBLISH')
            self.assertFalse(perm.is_edit())
            self.assertFalse(perm.is_showon())
            self.assertTrue(perm.is_sea())
            self.assertFalse(perm.is_bot())
            self.assertFalse(perm.is_tac())

            perm = result[1]
            self.assertEqual(perm.calendarid, 1)
            self.assertEqual(perm.campus, 'sea')
            self.assertEqual(perm.name, 'Dummy editor')
            self.assertEqual(perm.uwnetid, 'dummye')
            self.assertEqual(perm.level, 'EDIT')
            self.assertTrue(perm.is_edit())
            self.assertFalse(perm.is_showon())
            self.assertTrue(perm.is_sea())
            self.assertFalse(perm.is_bot())
            self.assertFalse(perm.is_tac())

            perm = result[2]
            self.assertEqual(perm.calendarid, 1)
            self.assertEqual(perm.campus, 'sea')
            self.assertEqual(perm.name, 'Dummy showon')
            self.assertEqual(perm.uwnetid, 'dummys')
            self.assertEqual(perm.level, 'SHOWON')
            self.assertFalse(perm.is_edit())
            self.assertTrue(perm.is_showon())
            self.assertTrue(perm.is_sea())
            self.assertFalse(perm.is_bot())
            self.assertFalse(perm.is_tac())

    def test_get_sea_permissions_error_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            self.assertRaises(CalendarNotExist,
                              Calendar.get_sea_permissions, 0)

            self.assertRaises(CalendarOwnByDiffAccount,
                              Calendar.get_sea_permissions, 2)
