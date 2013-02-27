from django.utils import unittest

from restclients.test.sws.term import SWSTestTerm

from restclients.test.sws.err404.dao import SWSTestDAO404
from restclients.test.sws.err500.dao import SWSTestDAO500
from restclients.test.sws.invalid_dao import SWSTestInvalidDAO
from restclients.test.sws.file_implementation.dao import SWSTestFileDAO

from restclients.test.sws.schedule_data import SWSTestScheduleData
from restclients.test.sws.section import SWSTestSectionData
from restclients.test.sws.section_status import SWSTestSectionStatusData
from restclients.test.sws.independent_study import SWSIndependentStudy
from restclients.test.sws.instructor_no_regid import SWSMissingRegid
from restclients.test.sws.registrations import SWSTestRegistrations

from restclients.test.sws.campus import SWSTestCampus
from restclients.test.sws.college import SWSTestCollege
from restclients.test.sws.department import SWSTestDepartment
from restclients.test.sws.curriculum import SWSTestCurriculum

from restclients.test.pws.person import PWSTestPersonData
from restclients.test.pws.entity import PWSTestEntityData

from restclients.test.pws.err404.dao import PWSTestDAO404
from restclients.test.pws.err404.pws import PWSTest404
from restclients.test.pws.err500.dao import PWSTestDAO500
from restclients.test.pws.err500.pws import PWSTest500
from restclients.test.pws.invalid_dao import PWSTestInvalidDAO
from restclients.test.pws.file_implementation.dao import PWSTestFileDAO

from restclients.test.gws.group import GWSGroupBasics
from restclients.test.gws.course_group import GWSCourseGroupBasics
from restclients.test.gws.search import GWSGroupSearch

from restclients.test.cache.none import NoCacheTest
from restclients.test.cache.time import TimeCacheTest
from restclients.test.cache.etag import ETagCacheTest

from restclients.test.book.by_schedule import BookstoreScheduleTest

from restclients.test.amazon_sqs.queues import SQSQueue

from restclients.test.sms.send import SMS
from restclients.test.sms.invalid_phone_number import SMSInvalidNumbers

from restclients.test.nws.subscription import NWSTestSubscription
from restclients.test.nws.channel import NWSTestChannel
from restclients.test.nws.endpoint import NWSTestEndpoint
from restclients.test.nws.message import NWSTestMessage
from restclients.test.nws.person import NWSTestPerson

from restclients.test.canvas.enrollments import CanvasTestEnrollment
from restclients.test.canvas.bad_sis_ids import CanvasBadSISIDs

