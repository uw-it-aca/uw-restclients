from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.trumba.calendar import Calendar
from restclients.trumba.exceptions import TrumbaException, CalendarNotExist, CalendarOwnByDiffAccount, NoDataReturned, UnknownError, UnexpectedError

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
            self.assertIsNotNone(result)
            self.assertTrue(len(result) == 10)

            trumba_cal = result[1]
            self.assertEqual(trumba_cal.calendarid, 1)
            self.assertEqual(trumba_cal.campus, 'sea')
            self.assertEqual(trumba_cal.name, 'Seattle calendar')
            self.assertTrue(trumba_cal.is_sea())
            self.assertFalse(trumba_cal.is_bot())
            self.assertFalse(trumba_cal.is_tac())
            
            trumba_cal = result[11321]
            self.assertEqual(trumba_cal.calendarid, 11321)
            self.assertEqual(trumba_cal.campus, 'sea')
            self.assertEqual(trumba_cal.name, 'Seattle child-sub-sub-calendar321')
            self.assertTrue(trumba_cal.is_sea())
            self.assertFalse(trumba_cal.is_bot())
            self.assertFalse(trumba_cal.is_tac())

            
    def test_get_tac_calendars_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_TAC_DAO_CLASS='restclients.dao_implementation.trumba.FileTac'
            ):
            self.assertIsNotNone(Calendar.get_tac_calendars())
            self.assertTrue(len(Calendar.get_tac_calendars()) == 1)
            

    def test_get_sea_permissions_normal_cases(self):
        with self.settings(
            RESTCLIENTS_TRUMBA_SEA_DAO_CLASS='restclients.dao_implementation.trumba.FileSea'
            ):
            result = Calendar.get_sea_permissions(1)
            self.assertIsNotNone(result)
            self.assertTrue(len(result) == 3)
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

    def test_create_body(self):
        self.assertEqual(Calendar._create_get_perm_body(1), '{"CalendarID": 1}')

    def test_is_valid_calendarid(self):
        self.assertTrue(Calendar._is_valid_calendarid(1))
        self.assertFalse(Calendar._is_valid_calendarid(0))
        self.assertFalse(Calendar._is_valid_calendarid(-1))

    def test_is_valid_email(self):
        self.assertTrue(Calendar._is_valid_email('test@washington.edu'))
        self.assertFalse(Calendar._is_valid_email('test-email@washington.edu'))
        self.assertFalse(Calendar._is_valid_email('test_email@washington.edu'))
        self.assertFalse(Calendar._is_valid_email('test.email@washington.edu'))
        self.assertFalse(Calendar._is_valid_email('test@uw.edu'))
        self.assertFalse(Calendar._is_valid_email('0test@washington.edu'))
        self.assertFalse(Calendar._is_valid_email(''))

    def test_extract_uwnetid(self):
        self.assertEqual(Calendar._extract_uwnetid('test@washington.edu'), 'test')
        self.assertEqual(Calendar._extract_uwnetid('test'), 'test')
        self.assertEqual(Calendar._extract_uwnetid('@washington.edu'), '')
        self.assertEqual(Calendar._extract_uwnetid('bad@uw.edu'), 'bad@uw.edu')
        self.assertEqual(Calendar._extract_uwnetid(''), '')
        
    def test_check_err(self):
        self.assertRaises(UnexpectedError,
                          Calendar._check_err, 
                          {"d":{"Messages":[{"Code":3009,
                                             "Description":"..."}]}})

        self.assertRaises(CalendarOwnByDiffAccount,
                          Calendar._check_err, 
                          {"d":{"Messages":[{"Code":3007}]}})

        self.assertRaises(CalendarNotExist,
                          Calendar._check_err, 
                          {"d":{"Messages":[{"Code":3006}]}})

        self.assertRaises(NoDataReturned,
                          Calendar._check_err, {'d': None})

        self.assertRaises(UnknownError,
                          Calendar._check_err, 
                          {"d":{"Messages":[]}})

        self.assertRaises(UnknownError,
                          Calendar._check_err, 
                          {"d":{"Messages":[{"Code": None}]}})

        self.assertIsNone(Calendar._check_err({"d":{"Messages":None}}))

    def test_process_get_cal_resp(self):
        """
        Omit for now . To be implemented using httmock
        """
        pass

    def test_process_get_perm_resp(self):
        """
        Omit for now . To be implemented using httmock
        """
        pass

