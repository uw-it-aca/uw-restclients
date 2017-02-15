from django.test import TestCase
from restclients.mailman.instructor_term_list import\
    get_instructor_term_list_name, exists_instructor_term_list
from restclients.test import fdao_mailman_override


@fdao_mailman_override
class TestMailmanInstructorList(TestCase):

    def test_exists_instructor_term_list(self):
        self.assertEqual(get_instructor_term_list_name('bill', 2013, 'autumn'),
                         "bill_au13")
        self.assertTrue(exists_instructor_term_list('bill', 2013, 'autumn'))
