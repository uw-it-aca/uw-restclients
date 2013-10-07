from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.exceptions import DataFailureException

class SWSTestRegistrations(TestCase):

    def test_active_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()

            # Valid section, missing file resources
            section = sws.get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              sws.get_active_registrations_for_section,
                              section)

    def test_all_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()

            # Valid section, missing file resources
            section = sws.get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              sws.get_all_registrations_for_section,
                              section)
