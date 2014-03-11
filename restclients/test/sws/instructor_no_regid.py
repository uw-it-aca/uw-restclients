from django.test import TestCase
from django.conf import settings
from restclients.sws import SWS
import restclients.sws.term as TermSws


class SWSMissingRegid(TestCase):
    def test_instructor_list(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):
            sws = SWS()

            term = TermSws.get_current()
            schedule = sws.schedule_for_regid_and_term("BB000000000000000000000000009994", term)

            self.assertEquals(len(schedule.sections), 1, "Has 1 section")

            instructors = schedule.sections[0].meetings[0].instructors

