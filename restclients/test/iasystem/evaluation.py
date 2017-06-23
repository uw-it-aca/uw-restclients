import datetime
import pytz
from django.test import TestCase
from restclients.iasystem.evaluation import search_evaluations,\
    get_evaluation_by_id
from restclients.test import fdao_ias_override, fdao_pws_override


@fdao_ias_override
@fdao_pws_override
class IASystemTest(TestCase):

    def test_search_eval(self):
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
        self.assertIsNone(evals[0].is_completed)
        self.assertEqual(evals[1].eval_status, "Closed")
        self.assertIsNone(evals[1].is_completed)

    def test_search_report(self):
        evals = search_evaluations("seattle",
                                   year=2014,
                                   term_name='Autumn',
                                   instructor_id='123456789')
        self.assertEqual(evals[0].section_sln, 15314)
        self.assertIsNotNone(evals[0].instructor_ids)
        self.assertEqual(len(evals[0].instructor_ids), 1)
        self.assertEqual(evals[0].instructor_ids[0], 123456789)
        self.assertEqual(evals[0].report_available_date,
                         datetime.datetime(2051, 3, 1,
                                           7, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_status, "Open")
        self.assertEqual(evals[0].report_url,
                         "https://uw.iasysdev.org/report/132068")
        self.assertIsNone(evals[0].is_completed)
        self.assertEqual(evals[1].eval_status, "Closed")

    def test_all_campuses(self):
        evals = search_evaluations("seattle", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 3)

        evals = search_evaluations("bothell", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 3)

        evals = search_evaluations("tacoma", year=2014,
                                   term_name='Autumn', student_id=1033334)
        self.assertEqual(len(evals), 3)

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
        self.assertIsNone(evals[0].is_completed)

    def test_evaluation_completion(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        evals = search_evaluations('seattle',
                                   term_name='Spring',
                                   curriculum_abbreviation="PHYS",
                                   student_id=1033334,
                                   section_id="AQ",
                                   course_number=121,
                                   year=2013)
        self.assertEqual(evals[0].section_sln, 18545)
        self.assertIsNotNone(evals[0].instructor_ids)
        self.assertEqual(len(evals[0].instructor_ids), 1)
        self.assertEqual(evals[0].instructor_ids[0], 123456789)
        self.assertTrue(evals[0].is_completed)

        regid = "9136CCB8F66711D5BE060004AC494F31"
        evals = search_evaluations('seattle',
                                   term_name='Spring',
                                   curriculum_abbreviation="PHYS",
                                   student_id=1233334,
                                   section_id="AQ",
                                   course_number=121,
                                   year=2013)
        self.assertEqual(evals[0].section_sln, 18545)
        self.assertIsNotNone(evals[0].instructor_ids)
        self.assertEqual(len(evals[0].instructor_ids), 2)
        self.assertEqual(evals[0].instructor_ids[0], 123456789)
        self.assertEqual(evals[0].instructor_ids[1], 987654321)
        self.assertFalse(evals[0].is_completed)

    def test_multiple_evals(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        evals = search_evaluations('seattle',
                                   term_name='Spring',
                                   curriculum_abbreviation="TRAIN",
                                   student_id=1033334,
                                   section_id="A",
                                   course_number=100,
                                   year=2013)
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 3)
        self.assertEqual(evals[0].section_sln, 17169)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2013, 5, 30,
                                           15, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date,
                         datetime.datetime(2013, 7, 1,
                                           7, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertFalse(evals[0].is_completed)
        self.assertEqual(evals[1].eval_open_date,
                         datetime.datetime(2013, 6, 5,
                                           7, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[1].eval_close_date,
                         datetime.datetime(2013, 6, 17,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertFalse(evals[1].is_completed)
        self.assertEqual(evals[2].eval_open_date,
                         datetime.datetime(2013, 6, 10,
                                           7, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[2].eval_close_date,
                         datetime.datetime(2013, 6, 19,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertTrue(evals[2].is_completed)
