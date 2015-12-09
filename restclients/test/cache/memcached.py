from django.test import TestCase
from django.conf import settings
from restclients.dao import SWS_DAO
from restclients.cache_implementation import MemcachedCache
from restclients.mock_http import MockHTTP
from unittest2 import skipIf
import re


class MemcachedCacheTest(TestCase):
    @skipIf(not getattr(settings, 'RESTCLIENTS_TEST_MEMCACHED', False), "Needs configuration to test memcached cache")
    def test_memcached(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                           RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.MemcachedCache'):

            cache = MemcachedCache()
            sws = SWS_DAO()
            sws.getURL('/student/', {})

            hit = cache.getCache('sws', '/student/', {})
            response = hit["response"]

            self.assertEquals(response.status, 200)

            html = response.data

            if not re.search('student/v4', html):
                self.fail("Doesn't contains a link to v4")

            hit = cache.getCache('sws', '/student/', {})
            self.assertEquals(response.status, 200)
            # Make sure there's nothing for pws there after the get
            response = cache.getCache('pws', '/student', {})
            self.assertEquals(response, None)

    @skipIf(not getattr(settings, 'RESTCLIENTS_TEST_MEMCACHED', False), "Needs configuration to test memcached cache")
    def test_longkeys(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                           RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.MemcachedCache'):

            cache = MemcachedCache()
            url = "".join("X" for i in range(300))


            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "valid"
            cache.processResponse('ok', url, ok_response)

            # This makes sure we don't actually cache anything when the url
            # is too long
            response = cache.getCache('ok', url, {})
            self.assertEquals(response, None)

            # But the get doesn't raise the exception w/ the set before it,
            # so this redundant-looking code is testing to make sure that we
            # catch the exception on the get as well.
            url = "".join("Y" for i in range(300))
            response = cache.getCache('ok', url, {})
            self.assertEquals(response, None)
