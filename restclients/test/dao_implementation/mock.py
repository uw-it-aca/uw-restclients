from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.dao_implementation.mock import convert_to_platform_safe

class TestMock(TestCase):

    def test_convert_to_platform_safe(self):
        name = "service/accounts.asmx/CreateEditor?Name=Margaret%20Murray&Email=murray4@washington.edu&Password="
        self.assertEqual(convert_to_platform_safe(name),
                         "service/accounts.asmx/CreateEditor_Name_Margaret%20Murray_Email_murray4_washington.edu_Password_")

        name = "registration/2013,spring,T%20BUS,310,A,12345678901234567890123456789012,1.json"
        self.assertEqual(convert_to_platform_safe(name),
                         "registration/2013_spring_T%20BUS_310_A_12345678901234567890123456789012_1.json")

        name = "sections?per_page=50&include=students@"
        self.assertEqual(convert_to_platform_safe(name),
                         "sections_per_page_50_include_students_")

        name = "admins?page=2&per_page=10"
        self.assertEqual(convert_to_platform_safe(name),
                         "admins_page_2_per_page_10")

        name = "enrollments?role=student"
        self.assertEqual(convert_to_platform_safe(name),
                         "enrollments_role_student")

        name = "2012,autumn,MATH,120/"
        self.assertEqual(convert_to_platform_safe(name),
                         "2012_autumn_MATH_120/")

        name = "sws/file/student/v4/course/2013,spring,PHIL,600/A"
        self.assertEqual(convert_to_platform_safe(name),
                         "sws/file/student/v4/course/2013_spring_PHIL_600/A")

