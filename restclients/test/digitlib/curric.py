from django.test import TestCase
from django.conf import settings
from restclients.exceptions import DataFailureException
from restclients.digitlib.curric import get_subject_guide

class DigitLibTest(TestCase):

    def test_subject_guide(self):
        with self.settings(
            RESTCLIENTS_DIGITLIB_DAO_CLASS='restclients.dao_implementation.digitlib.File'):
            location = get_subject_guide('TRAIN', 13833, 'spring', 2013)
            self.assertEquals(location,
                              "http://www.lib.washington.edu/subject/")

            location = get_subject_guide('PHYS', 18529, 'spring', 2013)
            self.assertEquals(location,
                              "http://guides.lib.washington.edu/physics_astronomy")

            location = get_subject_guide('MATH', 17571, 'autumn', 2013)
            self.assertEquals(location,
                              "http://guides.lib.washington.edu/math")

            location = get_subject_guide('B BUS', 10728, 'spring', 2015)
            self.assertEquals(location,
                              "http://libguides.uwb.edu/cat.php?cid=13469")
