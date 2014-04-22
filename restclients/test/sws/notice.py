from django.test import TestCase
from django.conf import settings
from restclients.sws.notice import get_notices_by_regid
import datetime

class SWSNotice(TestCase):
    def test_notice_resource(self):
        with self.settings(
                RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
                RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            notices = get_notices_by_regid("9136CCB8F66711D5BE060004AC494FFE")
            self.assertEquals(len(notices), 6)

            notice = notices[1]
            self.assertEquals(notice.notice_type, "QtrBegin")
            self.assertEquals(notice.notice_category, "StudentDAD")
            self.assertEquals(notice.notice_content, "Summer quarter begins <b>June 23, 2014<b>")

            #Date Attribute
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), "2014-06-23")

            #String Attribute
            attribute = notice.attributes[1]
            self.assertEquals(attribute.name, "Quarter")
            self.assertEquals(attribute.data_type, "string")
            self.assertEquals(attribute.get_value(), "Summer")

            #URL Attribute
            attribute = notice.attributes[2]
            self.assertEquals(attribute.name, "Link")
            self.assertEquals(attribute.data_type, "url")
            self.assertEquals(attribute.get_value(), "http://www.uw.edu")

            #Ensure unknown attributes aren't included
            self.assertEquals(len(notice.attributes), 3)

            #Default custom category
            self.assertEquals(notice.custom_category, "Uncategorized")

