from django.utils import unittest

from restclients.test.sws.term import SWSTestTerm

from restclients.test.sws.err404.dao import SWSTestDAO404
from restclients.test.sws.err500.dao import SWSTestDAO500
from restclients.test.sws.invalid_dao import SWSTestInvalidDAO
from restclients.test.sws.file_implementation.dao import SWSTestFileDAO

from restclients.test.sws.bad_schedule_data import SWSTestBadScheduleData

from restclients.test.pws.javerage import PWSTestJAverage

from restclients.test.pws.bad_data import PWSTestBadData
from restclients.test.pws.err404.dao import PWSTestDAO404
from restclients.test.pws.err404.pws import PWSTest404
from restclients.test.pws.err500.dao import PWSTestDAO500
from restclients.test.pws.err500.pws import PWSTest500
from restclients.test.pws.invalid_dao import PWSTestInvalidDAO
from restclients.test.pws.file_implementation.dao import PWSTestFileDAO

if __name__ == '__main__':
    unittest.main()
