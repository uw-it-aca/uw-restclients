from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.models.trumba import is_view_permission,\
    is_showon_permission, is_edit_permission, is_publish_permission,\
    is_higher_permission
import restclients.trumba.calendar as Calendar
from restclients.trumba.exceptions import TrumbaException, CalendarNotExist, CalendarOwnByDiffAccount, NoDataReturned, UnknownError, UnexpectedError
from restclients.test import fdao_trumba_sea_override,\
    fdao_trumba_bot_override, fdao_trumba_tac_override


@fdao_trumba_sea_override
@fdao_trumba_bot_override
@fdao_trumba_tac_override
class TrumbaTestCalendars(TestCase):

    def test_get_bot_calendars_normal_cases(self):
        result = Calendar.get_bot_calendars()
        self.assertTrue(result is not None and len(result) == 4)

    def test_get_sea_calendars_normal_cases(self):
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
        self.assertEqual(trumba_cal.name,
                         "%s%s%s%s" % ('Seattle calendar >> Seattle',
                                       ' child calendar3 >> Seattle',
                                       ' child-sub-calendar32 >> Seattle',
                                       ' child-sub-sub-calendar321'))
        sorted_cals = sorted(result.values())
        self.assertEqual(sorted_cals[0].name, "Seattle calendar")
        self.assertEqual(sorted_cals[1].name,
                         "Seattle calendar >> Seattle child calendar1")
        self.assertEqual(sorted_cals[4].name,
                         "Seattle calendar >> Seattle child calendar2")
        self.assertEqual(sorted_cals[5].name,
                         "Seattle calendar >> Seattle child calendar3")
        self.assertEqual(sorted_cals[9].name,
                         "%s%s%s%s" % ("Seattle calendar >> Seattle",
                                       " child calendar3 >> Seattle",
                                       " child-sub-calendar32 >> Seattle",
                                       " child-sub-sub-calendar322"))
        self.assertTrue(trumba_cal.is_sea())
        self.assertFalse(trumba_cal.is_bot())
        self.assertFalse(trumba_cal.is_tac())

    def test_get_tac_calendars_normal_cases(self):
        self.assertIsNotNone(Calendar.get_tac_calendars())
        self.assertTrue(len(Calendar.get_tac_calendars()) == 1)

    def test_get_sea_permissions_normal_cases(self):
        result = Calendar.get_sea_permissions(1)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) == 3)

        perm = result[0]
        self.assertEqual(perm.calendarid, 1)
        self.assertEqual(perm.campus, 'sea')
        self.assertEqual(perm.name, 'Dummy publisher')
        self.assertEqual(perm.uwnetid, 'dummyp')
        self.assertEqual(perm.level, 'PUBLISH')
        self.assertTrue(perm.is_publish())
        self.assertTrue(perm.is_edit())
        self.assertFalse(perm.is_showon())
        self.assertTrue(perm.is_sea())
        self.assertFalse(perm.is_bot())
        self.assertFalse(perm.is_tac())
        self.assertTrue(is_higher_permission(perm.level, 'EDIT'))
        self.assertTrue(perm.is_gt_level('EDIT'))

        perm2 = result[1]
        self.assertEqual(perm2.calendarid, 1)
        self.assertEqual(perm2.campus, 'sea')
        self.assertEqual(perm2.name, 'Dummy editor')
        self.assertEqual(perm2.uwnetid, 'dummye')
        self.assertEqual(perm2.level, 'EDIT')
        self.assertTrue(perm2.is_edit())
        self.assertFalse(perm2.is_showon())
        self.assertTrue(perm2.is_sea())
        self.assertFalse(perm2.is_bot())
        self.assertFalse(perm2.is_tac())
        self.assertTrue(is_higher_permission(perm2.level, 'SHOWON'))
        self.assertFalse(perm2.is_gt_level('EDIT'))

        perm3 = result[2]
        self.assertEqual(perm3.calendarid, 1)
        self.assertEqual(perm3.campus, 'sea')
        self.assertEqual(perm3.name, 'Dummy showon')
        self.assertEqual(perm3.uwnetid, 'dummys')
        self.assertEqual(perm3.level, 'SHOWON')
        self.assertFalse(perm3.is_edit())
        self.assertTrue(perm3.is_showon())
        self.assertTrue(perm3.is_sea())
        self.assertFalse(perm3.is_bot())
        self.assertFalse(perm3.is_tac())
        self.assertFalse(perm3.is_gt_level('SHOWON'))

        unordered_list = []
        unordered_list.append(perm3)
        unordered_list.append(perm2)
        unordered_list.append(perm)
        sorted_list = sorted(unordered_list)
        self.assertEqual(sorted_list[0].uwnetid, 'dummyp')
        self.assertEqual(sorted_list[1].uwnetid, 'dummye')
        self.assertEqual(sorted_list[2].uwnetid, 'dummys')

    def test_get_sea_permissions_error_cases(self):
        self.assertRaises(CalendarNotExist,
                          Calendar.get_sea_permissions, 0)

        self.assertRaises(CalendarOwnByDiffAccount,
                          Calendar.get_sea_permissions, 2)

    def test_create_body(self):
        self.assertEqual(Calendar._create_get_perm_body(1),
                         '{"CalendarID": 1}')

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
        self.assertEqual(Calendar._extract_uwnetid('test@washington.edu'),
                         'test')
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
