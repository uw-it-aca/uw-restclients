from django.test import TestCase
from django.conf import settings
from restclients.sws import get_current_sws_version

class SWSVersionTest(TestCase):
    """
    Tests that our SWS version defaults/settings overrides are correct
    """
    def test_defaults(self):
        with self.settings(RESTCLIENTS_SWS_USE_V5 = None):
            self.assertEquals(get_current_sws_version(), 4)

    def test_override(self):
        with self.settings(RESTCLIENTS_SWS_USE_V5 = True):
            self.assertEquals(get_current_sws_version(), 5)

    def test_false_override(self):
        with self.settings(RESTCLIENTS_SWS_USE_V5 = False):
            self.assertEquals(get_current_sws_version(), 4)
