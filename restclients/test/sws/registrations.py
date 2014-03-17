from django.test import TestCase
from django.conf import settings
import restclients.sws.section as SectionSws
import restclients.sws.registration as RegistrationSws
from restclients.exceptions import DataFailureException

class SWSTestRegistrations(TestCase):

    def test_active_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = SectionSws.get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              RegistrationSws.get_active_registrations_for_section,
                              section)

    def test_all_registrations_for_section(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            # Valid section, missing file resources
            section = SectionSws.get_section_by_label('2013,winter,C LIT,396/A')

            self.assertRaises(DataFailureException,
                              RegistrationSws.get_all_registrations_for_section,
                              section)

    def test_active_registration_status_after_drop(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,winter,DROP_T,100/A')

            registrations = RegistrationSws.get_all_registrations_for_section(section)

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, False)

    def test_active_registration_status_after_drop_and_add(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = SectionSws.get_section_by_label('2013,winter,DROP_T,100/B')

            registrations = RegistrationSws.get_all_registrations_for_section(section)

            self.assertEquals(len(registrations), 1)
            javerage_reg = registrations[0]
            self.assertEquals(javerage_reg.person.uwnetid, 'javerage')
            self.assertEquals(javerage_reg.is_active, True)

