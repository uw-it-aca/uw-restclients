from django.test import TestCase
from django.conf import settings
from restclients.dao import SWS_DAO
from restclients.cache_implementation import NoCache

class NoCacheTest(TestCase):
    def test_no_cache(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                            RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.NoCache'):

            # Check initial state
            cache = NoCache()
            response = cache.getCache('sws', '/', {})
            self.assertEquals(response, None)
            sws = SWS_DAO()
            sws.getURL('/student/', {})

            # Make sure there's nothing there after the get
            response = cache.getCache('sws', '/', {})
            self.assertEquals(response, None)
