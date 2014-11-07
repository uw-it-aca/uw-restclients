from django.test import TestCase
from django.conf import settings
from restclients.sws import section as sws_section
from restclients.catalyst.gradebook import get_participants_for_section
from restclients.exceptions import DataFailureException

class CatalystTestGradebook(TestCase):
    def test_participants_for_section(self):
        with self.settings(
                RESTCLIENTS_CATALYST_DAO_CLASS='restclients.dao_implementation.catalyst.File',
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            section = sws_section.get_section_by_label('2013,summer,CSS,161/A')
            instructor = section.meetings[0].instructors[0]

            participants = get_participants_for_section(section, instructor)

            self.assertEquals(len(participants), 3, "Correct participant count")
