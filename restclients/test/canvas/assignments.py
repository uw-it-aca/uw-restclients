from django.test import TestCase
from django.conf import settings
from restclients.canvas.assignments import Assignments
from restclients.exceptions import DataFailureException

class CanvasTestAssignments(TestCase):
    def test_assignments_by_course_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Assignments()
            assignments = canvas.get_assignments("862539")
            assignment = assignments[0]
            self.assertEquals(assignment.name, "Assignment 1", "Assignment name")
            self.assertEquals(assignment.muted, False, "Assignment isn't muted")
            self.assertEquals(assignment.due_at.day, 1, "Due date")
            self.assertEquals(assignment.grading_type, "points", "Grading type")
            self.assertEquals(assignment.grading_standard_id, None, "Grading Standard ID")

    def test_assignment_by_course_sis_id(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Assignments()
            assignments = canvas.get_assignments_by_sis_id("2013-autumn-PHYS-248-A")
            self.assertEquals(len(assignments), 2, "Assignment Count")

    def test_assignment_act_as(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Assignments(as_user="730FA4DCAE3411D689DA0004AC494FFE")
            assignments = canvas.get_assignments_by_sis_id("2013-autumn-PHYS-248-A")
            self.assertEquals(len(assignments), 2, "Assignment Count")
