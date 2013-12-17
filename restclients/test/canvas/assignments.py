from django.test import TestCase
from django.conf import settings
from restclients.canvas.assignments import Assignments
from restclients.exceptions import DataFailureException

class CanvasTestAssignments(TestCase):
    def test_submissions_by_course_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Assignments()
            assignments = canvas.get_assignments("862539")
            assignment = assignments[0]
            self.assertEquals(assignment.name, "Assignment 1", "Assignment name")
            self.assertEquals(assignment.muted, False, "Assignment isn't muted")
            self.assertEquals(assignment.due_at.day, 1, "Due date")

    def test_submission_by_course_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Assignments()
            assignments = canvas.get_assignments_by_sis_id("2013-autumn-PHYS-248-A")
            self.assertEquals(len(assignments), 2, "Assignment Count")

#    def test_submission_by_sis_id(self):
#        with self.settings(
#                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
#            canvas = Submissions()
#            submissions = canvas.get_submissions_multiple_assignments_by_sis_id(False, "2013-autumn-PHYS-248-A", "all")
#            self.assertEquals(len(submissions), 3, "Submission Count")