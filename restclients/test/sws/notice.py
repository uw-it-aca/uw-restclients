from django.test import TestCase
from django.conf import settings
from restclients.sws.notice import get_notices_by_regid
from datetime import date, datetime, timedelta

class SWSNotice(TestCase):
    def test_notice_resource(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File',
            RESTCLIENTS_PWS_DAO_CLASS='restclients.dao_implementation.pws.File'):

            notices = get_notices_by_regid("9136CCB8F66711D5BE060004AC494FFE")
            self.assertEquals(len(notices), 17)

            today = date.today()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)
            week = today + timedelta(days=2)
            next_week = today + timedelta(weeks=1)
            future = today + timedelta(weeks=3)
            future_end = today + timedelta(weeks=5)

            notice = notices[0]
            self.assertEquals(notice.notice_category, "StudentALR")
            self.assertEquals(notice.notice_type, "IntlStuCheckIn")
            attribute = notice.attributes[1]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), yesterday.strftime("%Y-%m-%d"))


            notice = notices[1]
            self.assertEquals(notice.notice_category, "StudentDAD")
            self.assertEquals(notice.notice_type, "QtrBegin")
            self.assertEquals(notice.notice_content,
                              "Summer quarter begins <b>June 23, 2014</b>")

            #Date Attribute
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), future_end.strftime("%Y-%m-%d"))

            #String Attribute
            attribute = notice.attributes[3]
            self.assertEquals(attribute.name, "Quarter")
            self.assertEquals(attribute.data_type, "string")
            self.assertEquals(attribute.get_value(), "Summer")

            #URL Attribute
            attribute = notice.attributes[4]
            self.assertEquals(attribute.name, "Link")
            self.assertEquals(attribute.data_type, "url")
            self.assertEquals(attribute.get_value(), "http://www.uw.edu")

            #Ensure unknown attributes aren't included
            self.assertEquals(len(notice.attributes), 5)

            #Default custom category
            self.assertEquals(notice.custom_category, "Uncategorized")


            notice = notices[2]
            self.assertEquals(notice.notice_category, "StudentDAD")
            self.assertEquals(notice.notice_type, "EstPd1RegDate")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), next_week.strftime("%Y-%m-%d"))

            notice = notices[3]
            self.assertEquals(notice.notice_category, "StudentALR")
            self.assertEquals(notice.notice_type, "PreRegNow")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), week.strftime("%Y-%m-%d"))

            notice = notices[4]
            self.assertEquals(notice.notice_category, "StudentALR")
            self.assertEquals(notice.notice_type, "PreRegNow")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), week.strftime("%Y-%m-%d"))

            notice = notices[4]
            self.assertEquals(notice.notice_category, "StudentALR")
            self.assertEquals(notice.notice_type, "PreRegNow")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), week.strftime("%Y-%m-%d"))

            notice = notices[5]
            self.assertEquals(notice.notice_category, "StudentALR")
            self.assertEquals(notice.notice_type, "IntlStuCheckIn")
            self.assertEquals(len(notice.attributes), 0)

            notice = notices[7]
            self.assertEquals(notice.notice_category, "StudentGEN")
            self.assertEquals(notice.notice_type, "AcctBalance")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), next_week.strftime("%Y-%m-%d"))

            notice = notices[8]
            self.assertEquals(notice.notice_category, "StudentDAD")
            self.assertEquals(notice.notice_type, "TuitDue")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), next_week.strftime("%Y-%m-%d"))

            notice = notices[12]
            self.assertEquals(notice.notice_category, "StudentDAD")
            self.assertEquals(notice.notice_type, "QtrEnd")
            attribute = notice.attributes[0]
            self.assertEquals(attribute.name, "Date")
            self.assertEquals(attribute.data_type, "date")
            self.assertEquals(attribute.get_value(), future_end.strftime("%Y-%m-%d"))

            notice = notices[13]
            self.assertEquals(notice.notice_category, "StudentFinAid")
            self.assertEquals(notice.notice_type, "DirectDeposit")

            notice = notices[14]
            self.assertEquals(notice.notice_category, "StudentFinAid")
            self.assertEquals(notice.notice_type, "DirectDepositShort")
            self.assertEquals(notice.long_notice.notice_type, "DirectDeposit")

            notice = notices[15]
            self.assertEquals(notice.notice_category, "StudentFinAid")
            self.assertEquals(notice.notice_type, "AidPriorityDate")

            notice = notices[16]
            self.assertEquals(notice.notice_category, "StudentFinAid")
            self.assertEquals(notice.notice_type, "AidPriorityDateShort")
            self.assertEquals(notice.long_notice.notice_type, "AidPriorityDate")
