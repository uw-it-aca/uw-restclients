"""
Contains SWS DAO implementations.
"""

import json
import time
from datetime import date, datetime, timedelta
from django.conf import settings
from restclients.mock_http import MockHTTP
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url

from lxml import etree

# XXX - this is arbitrary.  I didn't have a handy multi-threaded sws test
# case that went over 4 concurrent connections.  Just took the PWS number
SWS_MAX_POOL_SIZE = 10

class File(object):
    """
    The File DAO implementation returns generally static content.  Use this
    DAO with this configuration:

    RESTCLIENTS_SWS_DAO_CLASS = 'restclients.dao_implementation.sws.File'
    """

    grade_roster_document = None

    
    def _make_notice_date(self, response):
        """
        Set the date attribte value in the notice mock data
        """
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        past = today - timedelta(days=3)
        week = today + timedelta(days=2)
        future = today + timedelta(weeks=5)

        json_data = json.loads(response.data)
        for notice in json_data["Notices"]:
            if notice["NoticeAttributes"] and len(notice["NoticeAttributes"]) > 0:
                for attr in notice["NoticeAttributes"]:
                    if attr["DataType"] == "date":
                        if attr["Value"] == "yesterday":
                            attr["Value"] = yesterday.strftime("%Y%m%d")
                        elif attr["Value"] == "today":
                            attr["Value"] = today.strftime("%Y%m%d")
                        elif attr["Value"] == "tomorrow":
                            attr["Value"] = tomorrow.strftime("%Y%m%d")
                        elif attr["Value"] == "future":
                            attr["Value"] = future.strftime("%Y%m%d")
                        elif attr["Value"] == "past":
                            attr["Value"] = past.strftime("%Y%m%d")
                        elif attr["Value"] == "week":
                            attr["Value"] = week.strftime("%Y%m%d")
                        else:
                            attr["Value"] = week.strftime("%Y%m%d")

        response.data = json.dumps(json_data)

            
    def getURL(self, url, headers):
        response = get_mockdata_url("sws", "file", url, headers)

        if "/student/v5/notice" in url:
            self._make_notice_date(response)

        # This is to enable mock data grading.
        if "/student/v4/term/current.json" == url or "/student/v4/term/2013,spring.json" == url:
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            yesterday = now - timedelta(days=1)
            json_data = json.loads(response.data)

            json_data["GradeSubmissionDeadline"] = tomorrow.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodClose"] = tomorrow.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodOpen"] = yesterday.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodOpenATerm"] = yesterday.strftime("%Y-%m-%dT17:00:00")

            response.data = json.dumps(json_data)

        # This would come from putURL below - grading workflow
        if url.startswith('/student/v4/graderoster/2013,spring'):
            if File.grade_roster_document:
                response.data = self._make_grade_roster_submitted(File.grade_roster_document)
                File.grade_roster_document = None

        return response

    def putURL(self, url, headers, body):
        # For developing against crashes in grade submission
        if url.startswith('/student/v4/graderoster/2013,spring,ZERROR,101,S1,'):
            response = MockHTTP()
            response.data = "No employee found for ID 1234567890"
            response.status = 500
            return response

        # Submitted too late, sad.
        if url.startswith('/student/v4/graderoster/2013,spring,ZERROR,101,S2,'):
            response = MockHTTP()
            response.data = "grading period not active for year/quarter"
            response.status = 404
            return response


        # To support the grading workflow - there's a GET after the PUT
        # stash the PUT graderoster away, with submitted dates/grader values
        if url.startswith('/student/v4/graderoster/2013,spring'):
            time.sleep(5)
            File.grade_roster_document = body

        response = MockHTTP()
        if body is not None:
            response.status = 200
            response.headers = {"X-Data-Source": "SWS file mock data"}
            response.data = body
        else:
            response.status = 400
            response.data = "Bad Request: no PUT body"

        return response

    def _make_grade_roster_submitted(self, submitted_body):
        root = etree.fromstring(submitted_body)
        item_elements = root.findall('.//*[@class="graderoster_item"]')
        for item in item_elements:
            date_graded = item.find('.//*[@class="date_graded date"]')
            date_graded.text = '2013-06-01'

            grade_submitter_source = item.find('.//*[@class="grade_submitter_source"]')
            grade_submitter_source.text = 'CGB'

        return etree.tostring(root)

class Live(object):
    """
    This DAO provides real data.  It requires further configuration, e.g.

    RESTCLIENTS_SWS_CERT_FILE='/path/to/an/authorized/cert.cert',
    RESTCLIENTS_SWS_KEY_FILE='/path/to/the/certs_key.key',
    RESTCLIENTS_SWS_HOST='https://ucswseval1.cac.washington.edu:443',
    """
    pool = None

    def getURL(self, url, headers):
        if Live.pool is None:
            Live.pool = self._get_pool()

        return get_live_url(Live.pool, 'GET',
                            settings.RESTCLIENTS_SWS_HOST,
                            url, headers=headers,
                            service_name='sws')

    def putURL(self, url, headers, body):
        if Live.pool is None:
            Live.pool = self._get_pool()

        return get_live_url(Live.pool, 'PUT',
                            settings.RESTCLIENTS_SWS_HOST,
                            url, headers=headers, body=body,
                            service_name='sws')

    def _get_pool(self):
        return get_con_pool(settings.RESTCLIENTS_SWS_HOST,
                            settings.RESTCLIENTS_SWS_KEY_FILE,
                            settings.RESTCLIENTS_SWS_CERT_FILE,
                            max_pool_size=SWS_MAX_POOL_SIZE)
