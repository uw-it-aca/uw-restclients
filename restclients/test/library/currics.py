from datetime import date
from django.test import TestCase
from django.conf import settings
from restclients.library.currics import get_subject_guide_for_section_params,\
    get_subject_guide_for_section, get_subject_guide_for_canvas_course_sis_id
from restclients.exceptions import DataFailureException

class CurricsTest(TestCase):

    def test_subject_guide_for_section_params(self):
        with self.settings(
            RESTCLIENTS_LIBCURRICS_DAO_CLASS =
            'restclients.dao_implementation.library.currics.File'):

            guide = get_subject_guide_for_section_params(
                year=2015, quarter='aut', curriculum_abbr='MATH',
                course_number='309', section_id='A')

            self.assertEquals(guide.discipline, 'Mathematics')
            self.assertEquals(guide.contact_url, 'http://www.lib.washington.edu/about/contact')
            self.assertEquals(guide.librarian_url, 'http://guides.lib.uw.edu/research/subject-librarians')
            self.assertEquals(guide.guide_url, 'http://guides.lib.uw.edu/friendly.php?s=research/math')
            self.assertEquals(guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
            self.assertEquals(len(guide.libraries), 1)
            self.assertEquals(guide.libraries[0].name, 'Mathematics Research Library')
            self.assertEquals(guide.libraries[0].url, 'http://www.lib.washington.edu/math')
            self.assertEquals(len(guide.librarians), 2)
            self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
            self.assertEquals(guide.librarians[0].name, 'J Average')
            self.assertEquals(guide.librarians[0].url, 'http://guides.lib.washington.edu/Javerage')
            self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
            self.assertEquals(guide.librarians[1].name, 'B Average')
            self.assertEquals(guide.librarians[1].url, 'http://guides.lib.washington.edu/Baverage')

    def get_subject_guide_for_section(self):
        with self.settings(
            RESTCLIENTS_LIBCURRICS_DAO_CLASS =
            'restclients.dao_implementation.library.currics.File'):

            section = Section(year=2015, quarter='autumn',
                curriculum_abbr='MATH', course_number='309', section_id='A')

            guide = get_subject_guide_for_section(section)

            self.assertEquals(guide.discipline, 'Mathematics')
            self.assertEquals(guide.contact_url, 'http://www.lib.washington.edu/about/contact')
            self.assertEquals(guide.librarian_url, 'http://guides.lib.uw.edu/research/subject-librarians')
            self.assertEquals(guide.guide_url, 'http://guides.lib.uw.edu/friendly.php?s=research/math')
            self.assertEquals(guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
            self.assertEquals(len(guide.libraries), 1)
            self.assertEquals(guide.libraries[0].name, 'Mathematics Research Library')
            self.assertEquals(guide.libraries[0].url, 'http://www.lib.washington.edu/math')
            self.assertEquals(len(guide.librarians), 2)
            self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
            self.assertEquals(guide.librarians[0].name, 'J Average')
            self.assertEquals(guide.librarians[0].url, 'http://guides.lib.washington.edu/Javerage')
            self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
            self.assertEquals(guide.librarians[1].name, 'B Average')
            self.assertEquals(guide.librarians[1].url, 'http://guides.lib.washington.edu/Baverage')

    def get_subject_guide_for_canvas_course_sis_id(self):
        with self.settings(
            RESTCLIENTS_LIBCURRICS_DAO_CLASS =
            'restclients.dao_implementation.library.currics.File'):

            sis_id = '2015-autumn-MATH-309-A'
            guide = get_subject_guide_for_canvas_course_sis_id(sis_id)

            self.assertEquals(guide.discipline, 'Mathematics')
            self.assertEquals(guide.contact_url, 'http://www.lib.washington.edu/about/contact')
            self.assertEquals(guide.librarian_url, 'http://guides.lib.uw.edu/research/subject-librarians')
            self.assertEquals(guide.guide_url, 'http://guides.lib.uw.edu/friendly.php?s=research/math')
            self.assertEquals(guide.faq_url, 'http://guides.lib.uw.edu/research/faq')
            self.assertEquals(len(guide.libraries), 1)
            self.assertEquals(guide.libraries[0].name, 'Mathematics Research Library')
            self.assertEquals(guide.libraries[0].url, 'http://www.lib.washington.edu/math')
            self.assertEquals(len(guide.librarians), 2)
            self.assertEquals(guide.librarians[0].email, 'javerage@uw.edu')
            self.assertEquals(guide.librarians[0].name, 'J Average')
            self.assertEquals(guide.librarians[0].url, 'http://guides.lib.washington.edu/Javerage')
            self.assertEquals(guide.librarians[1].email, 'baverage@uw.edu')
            self.assertEquals(guide.librarians[1].name, 'B Average')
            self.assertEquals(guide.librarians[1].url, 'http://guides.lib.washington.edu/Baverage')
