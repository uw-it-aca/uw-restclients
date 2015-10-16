from django.test import TestCase
from restclients.canvas.courses import Courses


class CanvasTestCourses(TestCase):
    def test_course(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            course = canvas.get_course(149650)

            self.assertEquals(course.course_id, 149650, "Has proper course id")
            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(course.sis_course_id, "2013-spring-PHYS-121-A")
            self.assertEquals(course.sws_course_id(), "2013,spring,PHYS,121/A")
            self.assertEquals(course.account_id, 84378, "Has proper account id")
            self.assertEquals(course.term.sis_term_id, "2013-spring", "SIS term id")
            self.assertEquals(course.term.term_id, 810, "Term id")
            self.assertEquals(course.public_syllabus, False, "public_syllabus")
            self.assertEquals(course.workflow_state, "unpublished", "workflow_state")

    def test_course_with_params(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()
            course1 = canvas.get_course(149650, params={"include":["term"]})

            self.assertEquals(course1.term.term_id, 810, "Course contains term data")
            self.assertEquals(course1.syllabus_body, None, "Course doesn't contain syllabus_body")

            course2 = canvas.get_course(149650, params={"include":["syllabus_body"]})

            self.assertEquals(course2.syllabus_body, "Syllabus", "Course contains syllabus_body")
            self.assertEquals(course1.term.term_id, 810, "Course contains term data")

    def test_courses(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            courses = canvas.get_courses_in_account_by_sis_id(
                'uwcourse:seattle:arts-&-sciences:amath:amath',
                {'published': True})

            self.assertEquals(len(courses), 7, "Too few courses")

            course = courses[2]

            self.assertEquals(course.course_id, 141414, "Has proper course id")
            self.assertEquals(course.sis_course_id, "2013-spring-AMATH-403-A")
            self.assertEquals(course.sws_course_id(), "2013,spring,AMATH,403/A")
            self.assertEquals(course.name, "AMATH 403 A: Methods For Partial Differential Equations")
            self.assertEquals(course.account_id, 333333, "Has proper account id")
            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/141414", "Has proper course url")

    def test_published_courses(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            courses = canvas.get_published_courses_in_account_by_sis_id(
                'uwcourse:seattle:arts-&-sciences:amath:amath')

            self.assertEquals(len(courses), 7, "Too few courses")

            course = courses[2]

            self.assertEquals(course.course_id, 141414, "Has proper course id")
            self.assertEquals(course.sis_course_id, "2013-spring-AMATH-403-A")
            self.assertEquals(course.sws_course_id(), "2013,spring,AMATH,403/A")
            self.assertEquals(course.name, "AMATH 403 A: Methods For Partial Differential Equations")
            self.assertEquals(course.account_id, 333333, "Has proper account id")
            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/141414", "Has proper course url")

    def test_courses_by_regid(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            # Javerage's regid
            courses = canvas.get_courses_for_regid("9136CCB8F66711D5BE060004AC494FFE")

            self.assertEquals(len(courses), 1, "Has 1 canvas enrollment")

            course = courses[0]

            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(course.sis_course_id, "2013-spring-PHYS-121-A", "Course doesnt contain SIS ID")
            self.assertEquals(course.sws_course_id(), "2013,spring,PHYS,121/A", "Course doesnt contain SIS ID")
            self.assertEquals(course.account_id, 84378, "Has proper account id")

    def test_create_course(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            account_id = 88888
            name = "Created Course"

            course = canvas.create_course(account_id, name)

            self.assertEquals(course.course_id, 18881, "Correct course ID")
            self.assertEquals(course.name, name, "Correct course name")
            self.assertEquals(course.account_id, account_id, "Correct account ID")

    def test_update_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Courses()

            course = canvas.update_sis_id(149650, "NEW_SIS_ID")

            self.assertEquals(course.course_id, 149650, "Has proper course id")
            self.assertEquals(course.course_url, "https://canvas.uw.edu/courses/149650", "Has proper course url")
            self.assertEquals(course.sis_course_id, "NEW_SIS_ID")
