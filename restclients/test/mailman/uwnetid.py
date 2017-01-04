from datetime import datetime
from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.sws.section import get_section_by_label
from restclients.mailman.uwnetid import is_class_list_available, is_list_available
from restclients.test import fdao_pws_override, fdao_sws_override,\
    fdao_mailman_override

@fdao_pws_override
@fdao_sws_override
@fdao_mailman_override
class TestMailmanUwnetid(TestCase):

    def test_is_bot_class_list_available(self):
        section = get_section_by_label('2012,autumn,B BIO,180/A')
        self.assertTrue(is_class_list_available(section))

        self.assertFalse(is_list_available('bbio180a_au13'))

    def test_is_class_list_available(self):
        section = get_section_by_label('2013,summer,MATH,125/G')
        self.assertTrue(is_class_list_available(section))

    def test_is_tac_class_list_available(self):
        section = get_section_by_label('2013,autumn,T BUS,310/A')
        self.assertTrue(is_class_list_available(section))
