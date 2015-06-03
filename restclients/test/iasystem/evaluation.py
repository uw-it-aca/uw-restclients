from django.test import TestCase
from django.conf import settings
from restclients.iasystem.evaluation import search_evaluations,\
    get_evaluation_by_id
import datetime
import pytz

class IASystemTest(TestCase):

    def test_search_eval(self):
         with self.settings(
                RESTCLIENTS_PWS_DAO_CLASS=\
                    'restclients.dao_implementation.iasystem.File'):
            evals = search_evaluations("seattle",
                                       year=2014,
                                       term_name='Autumn',
                                       student_id=1033334)
            self.assertEqual(evals[0].section_sln, 15314)
            self.assertIsNotNone(evals[0].instructor_ids)
            self.assertEqual(len(evals[0].instructor_ids), 1)
            self.assertEqual(evals[0].instructor_ids[0], 851006409)
            self.assertEqual(evals[0].eval_open_date,
                             datetime.datetime(2014, 11, 24,
                                               15, 0,
                                               tzinfo=pytz.utc))
            self.assertEqual(evals[0].eval_close_date,
                             datetime.datetime(2051, 12, 3,
                                               7, 59, 59,
                                               tzinfo=pytz.utc))
            self.assertEqual(evals[0].eval_status, "Open")
            self.assertEqual(evals[0].eval_url,
                             "https://uw.iasysdev.org/survey/132068")
            self.assertEqual(evals[1].eval_status, "Closed")

    def test_all_campuses(self):
        evals = search_evaluations("seattle", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 2)

        evals = search_evaluations("bothell", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 2)

        evals = search_evaluations("tacoma", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 2)

    def test_get_by_id(self):
        evals = get_evaluation_by_id(132136, "seattle")
        self.assertEqual(len(evals), 1)

    def test_multiple_instructor(self):
        evals = get_evaluation_by_id(141412, "seattle")
        self.assertEqual(len(evals), 1)
        self.assertEqual(len(evals[0].instructor_ids), 3)
        self.assertEqual(evals[0].instructor_ids[0], 849004282)
        self.assertEqual(evals[0].instructor_ids[1], 849007339)
        self.assertEqual(evals[0].instructor_ids[2], 859003192)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2015, 3, 13,
                                           14, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date,
                         datetime.datetime(2015, 3, 21,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_url,
                         "https://uw.iasystem.org/survey/141412")
