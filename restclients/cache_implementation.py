"""
Contains DAO Cache implementations
"""
from restclients.mock_http import MockHTTP
from restclients.models import CacheEntryTimed
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, get_current_timezone


class NoCache(object):
    """
    This never caches anything.
    """
    def getCache(self, service, url, headers):
        return None

    def processResponse(self, service, url, response):
        pass


class TimeSimpleCache(object):
    """
    This caches all URLs for 60 seconds.  Used for testing.
    """
    def getCache(self, service, url, headers):
        now = make_aware(datetime.now(), get_current_timezone())
        time_limit = now - timedelta(seconds=60)

        query = CacheEntryTimed.objects.filter(
                                                service=service,
                                                url=url,
                                                time_saved__gte=time_limit,
                                              )

        if len(query):
            hit = query[0]

            response = MockHTTP()
            response.status = hit.status
            response.data = hit.content

            return {
                "response": response,
            }
        return None

    def processResponse(self, service, url, response):
        query = CacheEntryTimed.objects.filter(
                                                service=service,
                                                url=url,
                                              )

        cache_entry = CacheEntryTimed()
        if len(query):
            cache_entry = query[0]

        now = make_aware(datetime.now(), get_current_timezone())
        cache_entry.service = service
        cache_entry.url = url
        cache_entry.status = response.status
        cache_entry.content = response.read()
        cache_entry.headers = []
        cache_entry.time_saved = now
        cache_entry.save()

        return
