from django.test import TestCase
from django.conf import settings
from restclients.gws import GWS
from restclients.models import CourseGroup, GroupUser, GroupMember

class GWSCourseGroupBasics(TestCase):

    def test_get_group(self):
        with self.settings(
                RESTCLIENTS_GWS_DAO_CLASS='restclients.dao_implementation.gws.File'):
                    gws = GWS()
                    group = gws.get_group_by_id("course_2012aut-train102a")
                    self.assertEquals(group.name, "course_2012aut-train102a")
                    self.assertEquals(group.curriculum_abbr, "TRAIN")
                    self.assertEquals(group.course_number, "102")
                    self.assertEquals(group.section_id, "A")
                    self.assertEquals(group.year, "2012")
                    self.assertEquals(group.quarter, "autumn")
