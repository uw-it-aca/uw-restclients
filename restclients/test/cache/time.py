from django.test import TestCase
from django.conf import settings
from restclients.dao import SWS_DAO
from restclients.cache_implementation import TimeSimpleCache
import re

class TimeCacheTest(TestCase):
    def test_simple_time(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                            RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.TimeSimpleCache'):

            # Check initial state
            cache = TimeSimpleCache()
            response = cache.getCache('pws', '/student', {})
            self.assertEquals(response, None)
            response = cache.getCache('sws', '/student', {})
            self.assertEquals(response, None)
            sws = SWS_DAO()
            sws.getURL('/student', {})

            # Make sure there's a response there after the get
            hit = cache.getCache('sws', '/student', {})
            response = hit["response"]

            self.assertEquals(response.status, 200)

            html = response.read()
            if not re.search('student/v4', html):
                self.fail("Doesn't contains a link to v4")


            # Make sure there's nothing for pws there after the get
            response = cache.getCache('pws', '/student', {})
            self.assertEquals(response, None)

    def test_4hour_time(self):
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                            RESTCLIENTS_DAO_CACHE_CLASS='restclients.cache_implementation.FourHourCache'):

            # Check initial state
            cache = TimeSimpleCache()
            response = cache.getCache('pws', '/student', {})
            self.assertEquals(response, None)
            response = cache.getCache('sws', '/student', {})
            self.assertEquals(response, None)
            sws = SWS_DAO()
            response = sws.getURL('/student', {})

            html = response.read()
            if not re.search('student/v4', html):
                self.fail("Doesn't contains a link to v4")

            # Make sure there's a response there after the get
            hit = cache.getCache('sws', '/student', {})
            response = hit["response"]

            self.assertEquals(response.status, 200)

            html = response.read()
            if not re.search('student/v4', html):
                self.fail("Doesn't contains a link to v4")


            # Make sure there's nothing for pws there after the get
            response = cache.getCache('pws', '/student', {})
            self.assertEquals(response, None)
