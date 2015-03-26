from django.test import TestCase
from django.conf import settings
from restclients.iasystem.evaluation import search_evaluations
import datetime
import pytz

class IASystemTest(TestCase):

    def test_get_hfs_accounts(self):
        evals = search_evaluations(year=2014, term_name='Autumn', student_id=1033334)
        self.assertEqual(evals[0].section_sln, 15314)
        self.assertEqual(evals[0].instructor_id, 851006409)
        self.assertEqual(evals[0].eval_open_date, datetime.datetime(2014, 11, 24, 15, 0, tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date, datetime.datetime(2051, 12, 3, 7, 59, 59,  tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_status, "Open")
        self.assertEqual(evals[0].eval_is_online, True)
        self.assertEqual(evals[0].eval_url, "https://uw.iasysdev.org/survey/132068")
        self.assertEqual(evals[1].eval_status, "Closed")
        self.assertEqual(evals[2].eval_is_online, False)


