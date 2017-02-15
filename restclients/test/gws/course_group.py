from django.test import TestCase
from restclients.gws import GWS
from restclients.models.gws import CourseGroup, GroupUser, GroupMember
from restclients.test import fdao_gws_override


@fdao_gws_override
class GWSCourseGroupBasics(TestCase):

    def test_get_group(self):
        gws = GWS()
        group = gws.get_group_by_id("course_2012aut-train102a")
        self.assertEquals(group.name, "course_2012aut-train102a")
        self.assertEquals(group.curriculum_abbr, "TRAIN")
        self.assertEquals(group.course_number, "102")
        self.assertEquals(group.section_id, "A")
        self.assertEquals(group.year, "2012")
        self.assertEquals(group.quarter, "autumn")
