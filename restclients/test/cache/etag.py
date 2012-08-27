from django.test import TestCase
from django.conf import settings
from restclients.dao import PWS_DAO
from restclients.mock_http import MockHTTP
from restclients.cache_implementation import ETagCache
import re

class ETagCacheTest(TestCase):
    def test_etags(self):
        with self.settings(RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.ETag',
                            RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.ETagCache'):

            # Check initial state
            cache = ETagCache()
            response = cache.getCache('pws', '/same', {})
            self.assertEquals(response, None)
            response = cache.getCache('sws', '/same', {})
            self.assertEquals(response, None)

            pws = PWS_DAO()
            initial_response = pws.getURL('/same', {})

            content = initial_response.read()

            # Make sure there's a response there after the get
            headers = {}
            hit = cache.getCache('pws', '/same', headers)

            self.assertEquals(hit, None)

            if_match = headers["If-None-Match"]

            self.assertEquals(if_match, "A123BBB")


            mock_304 = MockHTTP()
            mock_304.status = 304
            hit = cache.processResponse('pws', '/same', mock_304)
            response = hit["response"]

            self.assertEquals(response.status, 200)
            self.assertEquals(response.read(), content)

            # Make sure there's nothing for pws there after the get
            response = cache.getCache('sws', '/same', {})
            self.assertEquals(response, None)
