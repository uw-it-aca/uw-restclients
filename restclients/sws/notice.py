"""
Interfaceing with the Student Web Service,
 for notice resource
"""
import logging
from restclients.models.sws import Notice, NoticeAttribute
from restclients.sws import get_resource
from dateutil import parser
import pytz
 

notice_res_url_prefix = "/student/v5/notice/"
logger = logging.getLogger(__name__)


def get_notices_by_regid(regid):
    """
    Returns a list of restclients.models.sws.Notice objects
    for the passed regid.
    """
    url = notice_res_url_prefix + regid + ".json"

    return _notices_from_json(get_resource(url))


def _notices_from_json(notice_data):
    notices = []
    notices_list = notice_data.get("Notices")
    if notices_list is not None:
        for notice in notices_list:
            notice_obj = Notice()
            notice_obj.notice_category = notice.get("NoticeCategory")
            notice_obj.notice_content = notice.get("NoticeContent")
            notice_obj.notice_type = notice.get("NoticeType")

            notice_attribs = []
            try:
                for notice_attrib in notice.get("NoticeAttributes"):
                    attribute = NoticeAttribute()
                    attribute.data_type = notice_attrib.get("DataType")
                    attribute.name = notice_attrib.get("Name")

                    #Currently known data types
                    if attribute.data_type == "url":
                        attribute._url_value = notice_attrib.get("Value")
                    elif attribute.data_type == "date":
                        #Convert to UTC datetime
                        date = parser.parse(notice_attrib.get("Value"))
                        localtz = pytz.timezone('America/Los_Angeles')
                        local_dt = localtz.localize(date)
                        utc_dt = local_dt.astimezone(pytz.utc)

                        attribute._date_value = utc_dt
                    elif attribute.data_type == "string":
                        attribute._string_value = notice_attrib.get("Value")
                    else:
                        logger.warn("Unkown attribute type: %s\nWith Value:%s" %
                                    (attribute.data_type,
                                    notice_attrib.get("value")))
                        continue
                    notice_attribs.append(attribute)
            except TypeError:
                pass
            notice_obj.attributes = notice_attribs
            notices.append(notice_obj)
        return notices

