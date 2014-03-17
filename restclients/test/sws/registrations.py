from django.test import TestCase
from django.conf import settings
from restclients.sws.section import get_section_by_label
from restclients.sws.registration import get_active_registrations_by_section
from restclients.sws.registration import get_all_registrations_by_section
from restclients.exceptions import DataFailureException

class SWSTestRegistrations(TestCase):

    def test_active_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              get_active_registrations_by_section,
                              section)

    def test_all_registrations_by_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              get_all_registrations_by_section,
                              section)

    def test_active_registration_status_after_drop(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/A')

            registrations = get_all_registrations_by_section(section)

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, False)

    def test_active_registration_status_after_drop_and_add(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = get_section_by_label('2013,winter,DROP_T,100/B')
            registrations = get_all_registrations_by_section(section)

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, True)

