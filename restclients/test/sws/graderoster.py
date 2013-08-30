from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
from restclients.models.sws import Section
from restclients.exceptions import DataFailureException


class SWSTestGradeRoster(TestCase):
    def test_get_graderoster(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):
            sws = SWS()

            section = sws.get_section_by_label('2013,summer,CSS,161/A')
            instructor = section.meetings[0].instructors[0]

            graderoster = sws.get_graderoster(section, instructor)

            new_graderoster = sws.update_graderoster(graderoster)

            #TODO: write some actual tests!

