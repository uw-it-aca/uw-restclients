from django.test import TestCase
from restclients.canvas import Canvas


class CanvasTestTerms(TestCase):
    def test_term(self):
        with self.settings(
                RESTCLIENTS_CANVAS_DAO_CLASS='restclients.dao_implementation.canvas.File'):
            canvas = Canvas()

            sis_term_id = "2012-summer"

            term = canvas.get_term_by_sis_id(sis_term_id)

            self.assertEquals(term.term_id, 810, "Has proper term id")
            self.assertEquals(term.name, "Summer 2012", "Has proper name")
            self.assertEquals(term.sis_term_id, sis_term_id, "Has proper sis id")
