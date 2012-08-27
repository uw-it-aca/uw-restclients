"""
Contains DAO Cache implementations
"""
from restclients.mock_http import MockHTTP
from restclients.models import CacheEntry, CacheEntryTimed
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


class ETagCache(object):
    """
    This caches objects just based on ETags.
    """
    def getCache(self, service, url, headers):
        now = make_aware(datetime.now(), get_current_timezone())
        time_limit = now - timedelta(seconds=60)

        query = CacheEntry.objects.filter(
                                            service=service,
                                            url=url,
                                         )

        if len(query):
            hit = query[0]

            response = MockHTTP()
            response.status = hit.status
            response.data = hit.content

            hit_headers = hit.getHeaders()

            if "ETag" in hit_headers:
                headers["If-None-Match"] = hit_headers["ETag"]

        return None

    def processResponse(self, service, url, response):
        query = CacheEntryTimed.objects.filter(
                                                service=service,
                                                url=url,
                                              )

        cache_entry = CacheEntryTimed()
        if len(query):
            cache_entry = query[0]

        if response.status == 304:
            if cache_entry == None:
                raise Exception("304, but no content??")

            response = MockHTTP()
            response.status = cache_entry.status
            response.data = cache_entry.content
            response.headers = cache_entry.headers
            return {"response": response}
        else:
            now = make_aware(datetime.now(), get_current_timezone())
            cache_entry.service = service
            cache_entry.url = url
            cache_entry.status = response.status
            cache_entry.content = response.read()

            cache_entry.headers = response.headers
            cache_entry.time_saved = now
            cache_entry.save()

        return
