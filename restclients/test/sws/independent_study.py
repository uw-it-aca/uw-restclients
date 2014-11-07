from django.test import TestCase
from django.conf import settings
from restclients.sws.registration import get_schedule_by_regid_and_term
from restclients.sws.term import get_current_term

class SWSIndependentStudy(TestCase):
    def test_instructor_list(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            term = get_current_term()
            schedule = get_schedule_by_regid_and_term("BB000000000000000000000000000004", term)

            self.assertEquals(len(schedule.sections), 1, "Has 1 section")

            instructors = schedule.sections[0].meetings[0].instructors

            self.assertEquals(len(instructors), 1, "Only has the 1 instructor for independent study?")
            self.assertEquals(instructors[0].uwregid, 'FBB38FE46A7C11D5A4AE0004AC494FFE', "Only has the 1 instructor for independent study?")
