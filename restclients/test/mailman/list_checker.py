from django.test import TestCase
from restclients.mailman.list_checker import _get_url_path, exists,\
    get_instructor_term_list_name, exists_instructor_term_combined_list,\
    _get_list_name_curr_abbr, get_course_list_name, exists_course_list
from restclients.test import fdao_mailman_override


@fdao_mailman_override
class TestMailmanLists(TestCase):

    def test_get_url_path(self):
        self.assertEqual(_get_url_path('aaa_au12'),
                         ("/%s/admin/v1.0/uwnetid/available/?uwnetid=%s" %
                          ("__mock_key__", 'aaa_au12')))

    def test_exists(self):
        self.assertFalse(exists('bbio180a_au12'))
        self.assertTrue(exists('bbio180a_au13'))
        self.assertFalse(exists("tbus310a_au13"))

    def test_exists_instructor_term_combined_list(self):
        self.assertEqual(
            get_instructor_term_list_name('bill', 2013, 'autumn'), "bill_au13")
        self.assertTrue(
            exists_instructor_term_combined_list('bill', 2013, 'autumn'))

    def test_get_list_name_curr_abbr(self):
        self.assertEqual(_get_list_name_curr_abbr("B BIO"), 'bbio')
        self.assertEqual(_get_list_name_curr_abbr("T BUS"), 'tbus')
        self.assertEqual(_get_list_name_curr_abbr("MATH"), 'math')

    def test_get_course_list_name(self):
        self.assertEqual(get_course_list_name("B BIO", "180", "A",
                                              "autumn", 2012),
                         'bbio180a_au12')
        self.assertEqual(get_course_list_name("T BUS", "310", "A",
                                              "autumn", 2013),
                         'tbus310a_au13')
        self.assertEqual(get_course_list_name("MATH", "125", "G",
                                              "summer", 2013),
                         'math125g_su13')

    def test_exists_course_list(self):
        self.assertFalse(exists_course_list("B BIO", "180",
                                            "A", "autumn", 2012))
        self.assertTrue(exists_course_list("B BIO", "180",
                                           "A", "autumn", 2013))
        self.assertFalse(exists_course_list("T BUS", "310", "A",
                                            "autumn", 2013))
        self.assertFalse(exists_course_list("MATH", "125", "G",
                                            "summer", 2013))
