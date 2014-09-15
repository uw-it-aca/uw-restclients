from django.test import TestCase
from django.conf import settings
from restclients.r25.spaces import get_space_by_id, get_spaces
from restclients.exceptions import DataFailureException

class R25TestSpaces(TestCase):
    
    def test_space_by_id(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):
            
            space = get_space_by_id("1000")
            self.assertEquals(space.space_id, "1000", "space_id") 
            self.assertEquals(space.name, "ACC 120", "name")
            self.assertEquals(space.formal_name, "Smith Hall", "formal_name")


    def test_all_spaces(self):
        with self.settings(
                RESTCLIENTS_R25_DAO_CLASS='restclients.dao_implementation.r25.File'):

            spaces = get_spaces()
            self.assertEquals(len(spaces), 3, "space count")
