"""
Contains SWS DAO implementations.
"""

import json
import time
import re
import random
from datetime import date, datetime, timedelta
from lxml import etree
from django.conf import settings
from os.path import abspath, dirname
import os

from restclients_core.dao import DAO, MockDAO


class SWS_DAO(DAO):
    def service_name(self):
        return 'sws'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "..", "resources"))]

    def _edit_mock_response(self, method, url, headers, body, response):
        if "GET" == method:
            self._update_get(url, response)
        elif "PUT" == method:
            self._update_put(url, body, response)

    def _update_put(self, url, body, response):
        # For developing against crashes in grade submission
        if re.match('/student/v\d/graderoster/2013,spring,ZERROR,101,S1,',
                    url):
            response.data = "No employee found for ID 1234567890"
            response.status = 500

        # Submitted too late, sad.
        if re.match('/student/v\d/graderoster/2013,spring,ZERROR,101,S2,',
                    url):
            response.data = "grading period not active for year/quarter"
            response.status = 404

        if body is not None:
            response.status = 200
            response.headers = {"X-Data-Source": "SWS file mock data"}
            response.data = self._make_grade_roster_submitted(body)
        else:
            response.status = 400
            response.data = "Bad Request: no PUT body"

    def _make_grade_roster_submitted(self, submitted_body):
        root = etree.fromstring(submitted_body)
        item_elements = root.findall('.//*[@class="graderoster_item"]')
        for item in item_elements:
            date_graded = item.find('.//*[@class="date_graded date"]')
            if date_graded.text is None:
                date_graded.text = '2013-06-01'

            grade_submitter_source = item.find(
                './/*[@class="grade_submitter_source"]')
            if grade_submitter_source.text is None:
                grade_submitter_source.text = 'WEBCGB'

            # Set the status code and message for each item, these elements
            # aren't present in graderosters returned from GET
            # Use settings.GRADEROSTER_PARTIAL_SUBMISSIONS to simulate failures
            status_code_text = '200'
            status_message_text = ''
            if (getattr(settings,
                        'GRADEROSTER_PARTIAL_SUBMISSIONS',
                        False) and random.choice([True, False])):

                status_code_text = '500'
                status_message_text = 'Invalid grade'

            status_code = item.find('.//*[@class="code"]')
            if status_code is None:
                status_code = etree.fromstring('<span class="code"/>')
                item.append(status_code)
            status_code.text = status_code_text

            status_message = item.find('.//*[@class="message"]')
            if status_message is None:
                status_message = etree.fromstring('<span class="message"/>')
                item.append(status_message)
            status_message.text = status_message_text

        return etree.tostring(root)

    def _update_get(self, url, response):
        if "/student/v5/notice" in url:
            self._make_notice_date(response)

        # This is to enable mock data grading.
        if (re.match("/student/v\d/term/current.json", url) or
                re.match("/student/v\d/term/2013,spring.json", url)):
            now = datetime.now()
            tomorrow = now + timedelta(days=1)
            yesterday = now - timedelta(days=1)
            json_data = json.loads(response.data)

            json_data["GradeSubmissionDeadline"] =\
                tomorrow.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodClose"] =\
                tomorrow.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodOpen"] =\
                yesterday.strftime("%Y-%m-%dT17:00:00")
            json_data["GradingPeriodOpenATerm"] =\
                yesterday.strftime("%Y-%m-%dT17:00:00")

            response.data = json.dumps(json_data)

    def _make_notice_date(self, response):
        """
        Set the date attribte value in the notice mock data
        """
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        week = today + timedelta(days=2)
        next_week = today + timedelta(weeks=1)
        future = today + timedelta(weeks=3)
        future_end = today + timedelta(weeks=5)

        json_data = json.loads(response.data)
        for notice in json_data["Notices"]:
            if notice["NoticeAttributes"] and\
                    len(notice["NoticeAttributes"]) > 0:
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
                        elif attr["Value"] == "future_end":
                            attr["Value"] = future_end.strftime("%Y%m%d")
                        elif attr["Value"] == "next_week":
                            attr["Value"] = next_week.strftime("%Y%m%d")
                        elif attr["Value"] == "week":
                            attr["Value"] = week.strftime("%Y%m%d")
                        else:
                            pass   # use original

        response.data = json.dumps(json_data)


# For testing MUWM-2411
class TestBadResponse(MockDAO):
    def load(self, method, url, headers, body):
        if url == "/student/v5/course/2012,summer,PHYS,121/AQ.json":
            raise Exception("Uh oh!")
        return super(TestBadResponse, self).load(method, url, headers, body)
