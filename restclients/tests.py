from restclients.test.uwnetid.subscription import EmailForwardingTest
from restclients.test.uwnetid.subscription_60 import KerberosSubsTest
from restclients.test.uwnetid.subscription_233 import Office365EduSubsTest
from restclients.test.uwnetid.subscription import NetidSubscriptionTest
from restclients.test.uwnetid.subscription import NetidPostSubscriptionTest
from restclients.test.util.date_formator import FormatorTest
from restclients.test.util.datetime_convertor import DatetimeConvertorTest
from restclients.test.util.retry import RetryTest
from restclients.test.bridge.models import TestBridgeModel
from restclients.test.bridge.user import TestBridgeUser
from restclients.test.bridge.custom_field import TestBridgeCustomFields
from restclients.test.hfs.idcard import HfsTest
from restclients.test.hrpws.appointee import AppointeeTest
from restclients.test.library.mylibinfo import MyLibInfoTest
from restclients.test.library.currics import CurricsTest
from restclients.test.grad.committee import CommitteeTest
from restclients.test.grad.degree import DegreeTest
from restclients.test.grad.leave import LeaveTest
from restclients.test.grad.petition import PetitionTest
from restclients.test.sws.compatible import SWSTest
from restclients.test.sws.financial import SWSFinance
from restclients.test.sws.notice import SWSNotice
from restclients.test.sws.term import SWSTestTerm
from restclients.test.sws.err404.dao import SWSTestDAO404
from restclients.test.sws.err500.dao import SWSTestDAO500
from restclients.test.sws.invalid_dao import SWSTestInvalidDAO
from restclients.test.sws.file_implementation.dao import SWSTestFileDAO

from restclients.test.sws.schedule_data import SWSTestScheduleData
from restclients.test.sws.enrollment import SWSTestEnrollments
from restclients.test.sws.section import SWSTestSectionData
from restclients.test.sws.section_status import SWSTestSectionStatusData
from restclients.test.sws.independent_study import SWSIndependentStudy
from restclients.test.sws.instructor_no_regid import SWSMissingRegid
from restclients.test.sws.registrations import SWSTestRegistrations

from restclients.test.sws.campus import SWSTestCampus
from restclients.test.sws.college import SWSTestCollege
from restclients.test.sws.department import SWSTestDepartment
from restclients.test.sws.curriculum import SWSTestCurriculum

from restclients.test.sws.graderoster import SWSTestGradeRoster

from restclients.test.sws.dates import SWSTestDates

from restclients.test.pws.person import PWSTestPersonData
from restclients.test.pws.entity import PWSTestEntityData
from restclients.test.pws.idcard import TestIdCardPhoto
from restclients.test.pws.err404.dao import PWSTestDAO404
from restclients.test.pws.err404.pws import PWSTest404
from restclients.test.pws.err500.dao import PWSTestDAO500
from restclients.test.pws.err500.pws import PWSTest500
from restclients.test.pws.invalid_dao import PWSTestInvalidDAO
from restclients.test.pws.file_implementation.dao import PWSTestFileDAO

from restclients.test.kws.key import KWSTestKeyData

from restclients.test.gws.group import GWSGroupBasics
from restclients.test.gws.course_group import GWSCourseGroupBasics
from restclients.test.gws.search import GWSGroupSearch

from restclients.test.cache.none import NoCacheTest
from restclients.test.cache.time import TimeCacheTest
from restclients.test.cache.etag import ETagCacheTest
from restclients.test.cache.memcached import MemcachedCacheTest

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
from restclients.test.canvas.accounts import CanvasTestAccounts
from restclients.test.canvas.admins import CanvasTestAdmins
from restclients.test.canvas.roles import CanvasTestRoles
from restclients.test.canvas.courses import CanvasTestCourses
from restclients.test.canvas.sections import CanvasTestSections
from restclients.test.canvas.bad_sis_ids import CanvasBadSISIDs
from restclients.test.canvas.terms import CanvasTestTerms
from restclients.test.canvas.users import CanvasTestUsers
from restclients.test.canvas.submissions import CanvasTestSubmissions
from restclients.test.canvas.assignments import CanvasTestAssignments
from restclients.test.canvas.quizzes import CanvasTestQuizzes
from restclients.test.canvas.external_tools import CanvasTestExternalTools

from restclients.test.catalyst.gradebook import CatalystTestGradebook

from restclients.test.trumba.accounts import TrumbaTestAccounts
from restclients.test.trumba.calendar import TestCalendarParse
from restclients.test.trumba.calendars import TrumbaTestCalendars
from restclients.test.gws.trumba_group import TestGwsTrumbaGroup

from restclients.test.r25.events import R25TestEvents
from restclients.test.r25.spaces import R25TestSpaces

from restclients.test.myplan import MyPlanTestData

from restclients.test.o365.user import O365TestUser
from restclients.test.o365.license import O365TestLicense

from restclients.test.thread import ThreadsTest
from restclients.test.view import ViewTest
from restclients.test.dao_implementation.mock import TestMock

from restclients.test.iasystem.evaluation import IASystemTest
