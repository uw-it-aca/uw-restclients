from django.test import TestCase
from restclients.sws.section import get_section_by_label
from restclients.mailman.course_list import _get_list_name_curr_abbr,\
    get_course_list_name, exists_course_list, get_section_list_name,\
    exists_section_list, get_secondary_combined_list_name,\
    exists_secondary_combined_list, get_section_secondary_combined_list_name,\
    exists_section_secondary_combined_list
from restclients.test import fdao_sws_override, fdao_mailman_override


@fdao_sws_override
@fdao_mailman_override
class TestMailmanCourseLists(TestCase):

    def test_get_list_name_curr_abbr(self):
        self.assertEqual(_get_list_name_curr_abbr("B BIO"), 'bbio')
        self.assertEqual(_get_list_name_curr_abbr("T BUS"), 'tbus')
        self.assertEqual(_get_list_name_curr_abbr("MATH"), 'math')
        self.assertEqual(_get_list_name_curr_abbr("JSIS B"), 'jsisb')
        self.assertEqual(_get_list_name_curr_abbr("CL AR"), "clar")
        self.assertEqual(_get_list_name_curr_abbr("EDC&I"), "edci")

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

    def test_bot_section_list_names(self):
        section = get_section_by_label('2012,autumn,B BIO,180/A')
        self.assertEqual(get_section_list_name(section),
                         'bbio180a_au12')
        self.assertEqual(get_section_secondary_combined_list_name(section),
                         'multi_bbio180a_au12')

    def test_tac_section_list_names(self):
        section = get_section_by_label('2013,autumn,T BUS,310/A')
        self.assertEqual(get_section_list_name(section),
                         'tbus310a_au13')
        self.assertEqual(get_section_secondary_combined_list_name(section),
                         'multi_tbus310a_au13')

    def test_section_list_names(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertEqual(get_section_list_name(section),
                         'math125g_su13')
        self.assertEqual(get_section_secondary_combined_list_name(section),
                         'multi_math125g_su13')

    def test_is_bot_class_list_available(self):
        section = get_section_by_label('2012,autumn,B BIO,180/A')
        self.assertFalse(exists_section_list(section))
        section = get_section_by_label('2013,autumn,B BIO,180/A')
        self.assertTrue(exists_section_secondary_combined_list(section))

    def test_is_tac_class_list_available(self):
        section = get_section_by_label('2013,autumn,T BUS,310/A')
        self.assertFalse(exists_section_list(section))
        section = get_section_by_label('2013,spring,T BUS,310/A')
        self.assertTrue(exists_section_list(section))

    def test_exists_section_list(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertFalse(exists_section_list(section))

    def test_exists_secondary_combined_list(self):
        self.assertFalse(
            exists_secondary_combined_list("MATH", "125", "A",
                                           "summer", 2013))
        self.assertTrue(
            exists_secondary_combined_list("B BIO", "180", "A",
                                           "autumn", 2013))

    def test_exists_secondary_section_combined_list(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertFalse(exists_section_secondary_combined_list(section))
