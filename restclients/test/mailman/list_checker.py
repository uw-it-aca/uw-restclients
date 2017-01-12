from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.sws.section import get_section_by_label
from restclients.mailman.list_checker import exists_section_list,\
    exists_secondary_section_combined_list, _get_curriculum_abbr,\
    exists, exists_instructor_term_combined_list
from restclients.test import fdao_pws_override, fdao_sws_override,\
    fdao_mailman_override

@fdao_pws_override
@fdao_sws_override
@fdao_mailman_override
class TestMailmanListExists(TestCase):

    def test_get_curriculum_abbr(self):
        section = get_section_by_label('2012,autumn,B BIO,180/A')
        self.assertEqual(_get_curriculum_abbr(section), 'bbio')
        section = get_section_by_label('2013,autumn,T BUS,310/A')
        self.assertEqual(_get_curriculum_abbr(section), 'tbus')
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertEqual(_get_curriculum_abbr(section), 'math')

    def test_is_bot_class_list_available(self):
        section = get_section_by_label('2012,autumn,B BIO,180/A')
        self.assertFalse(exists_section_list(section))
        self.assertTrue(exists('bbio180a_au13'))
        section = get_section_by_label('2013,autumn,B BIO,180/A')
        self.assertTrue(exists_secondary_section_combined_list(section))

    def test_is_tac_class_list_available(self):
        section = get_section_by_label('2013,autumn,T BUS,310/A')
        self.assertFalse(exists_section_list(section))
        section = get_section_by_label('2013,spring,T BUS,310/A')
        self.assertTrue(exists_section_list(section))

    def test_exists_section_list(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertFalse(exists_section_list(section))

    def test_exists_secondary_section_combined_list(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertFalse(exists_secondary_section_combined_list(section))

    def test_exists_instructor_term_combined_list(self):
        section = get_section_by_label('2013,autumn,B BIO,180/A')
        self.assertTrue(
                exists_instructor_term_combined_list('bill',
                                                     section.term))
