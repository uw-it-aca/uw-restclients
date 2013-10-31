"""
The interface for accessing Trumba's Calendars Service 
"""

from restclients.models.trumba import CalendarGroup, Permission
from restclients.exceptions import DataFailureException
from restclients.trumba.exceptions import CalendarOwnByDiffAccount, CalendarNotExist
from restclients.trumba.exceptions import NoDataReturned, UnknownError
from restclients.trumba import Trumba
import json
import logging
import re

class Calendar:
    """
    This object access calendar info and user permissions in Trumba
    """

    logger = logging.getLogger('restclients.trumba.Calendar')
    bot_campus_code = 'bot'
    sea_campus_code = 'sea'
    tac_campus_code = 'tac'
    get_calendarlist_url = "/service/calendars.asmx/GetCalendarList"
    get_permissions_url = "/service/calendars.asmx/GetPermissions?CalendarID="

    @staticmethod
    def get_bot_calendars():
        """
        :return: CalendarGroup[] or None if not exists
        Return a list of CalendarGroup objects corresponding to
        Bothell calendars. 
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_bot_resource(Calendar.get_calendarlist_url,"{}"),
            Calendar.bot_campus_code)

    @staticmethod
    def get_sea_calendars():
        """
        :return: CalendarGroup[] or None if not exists
        Return a list of CalendarGroup objects corresponding to
        Seattle calendars. 
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_sea_resource(Calendar.get_calendarlist_url,"{}"),
            Calendar.sea_campus_code)

    @staticmethod
    def get_tac_calendars():
        """
        :return: CalendarGroup[] or None if not exists
        Return a list of CalendarGroup objects corresponding to
        Tacoma calendars. 
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_tac_resource(Calendar.get_calendarlist_url,"{}"),
            Calendar.tac_campus_code)

    @staticmethod
    def _make_get_permissions_url(calendar_id):
        return "%s%s" % (Calendar.get_permissions_url,
                         calendar_id)

    @staticmethod
    def get_bot_permissions(calendar_id):
        """
        :param calendar_id: an integer representing calendar ID
        :return: Permission[] or None if not exists
        Return a list of Permission objects representing
        the user permissions of a given Bothell calendar. 
        raise DataFailureException or a corresponding TrumbaException
        if the request failed or an error code has been returned.
        """
        url = Calendar._make_get_permissions_url(calendar_id)
        body = json.dumps({'CalendarID': calendar_id})
        return Calendar._process_get_perm_resp(
            url,
            Trumba.post_bot_resource(url, body),
            Calendar.bot_campus_code,
            calendar_id)

    @staticmethod
    def get_sea_permissions(calendar_id):
        """
        Return a list of Permission objects representing
        the user permissions of a given Seattle calendar. 
        If request failed, return None.
        :return: Permission[]
        """
        url = Calendar._make_get_permissions_url(calendar_id)
        body = json.dumps({'CalendarID': calendar_id})
        return Calendar._process_get_perm_resp(
            url,
            Trumba.post_sea_resource(url, body),
            Calendar.sea_campus_code,
            calendar_id)

    @staticmethod
    def get_tac_permissions(calendar_id):
        """
        Return a list of Permission objects representing
        the user permissions of a given Tacoma calendar. 
        If request failed, return None.
        :return: Permission[]
        """
        url = Calendar._make_get_permissions_url(calendar_id)
        body = json.dumps({'CalendarID': calendar_id})
        return Calendar._process_get_perm_resp(
            url,
            Trumba.post_tac_resource(url, body),
            Calendar.tac_campus_code,
            calendar_id)

    re_cal_id = re.compile(r'[1-9]\d+')

    @staticmethod
    def _is_valid_calendarid(calendarid):
        return Calendar.re_cal_id.match(str(calendarid)) is not None

    @staticmethod
    def _load_calendar(campus, resp_fragment, calendars):
        """
        :return: CalendarGroup[]
        """
        for record in resp_fragment:
            cal_grp = CalendarGroup()
            cal_grp.campus = campus
            cal_grp.calendarid = record['ID']
            cal_grp.name = record['Name']
            #print "%s %s_%s" % (cal.name, cal.campus, cal.calendarid)
            if not Calendar._is_valid_calendarid(record['ID']):
                logger.error("%s InvalidCalendarId, entry skipped!" % cal_grp)
                continue
            calendars.append(cal_grp)
            if record['ChildCalendars'] is not None and len(record['ChildCalendars']) > 0:
                Calendar._load_calendar(campus, record['ChildCalendars'], calendars)

    @staticmethod
    def _process_get_cal_resp(url, post_response, campus):
        """
        If the request is successful, process the response data 
        and load the json data into a list of CalendarGroup objects; 
        otherwise return None.
        :return: CalendarGroup[]
        """
        request_id = "%s %s" % (campus, url)
        if post_response.status != 200 or post_response.data is None:
            raise DataFailureException(request_id,
                                       post_response.status,
                                       post_response.reason)
        
        data = json.loads(post_response.data)
        Calendar._check_err(data)

        if data['d']['Calendars'] is None or len(data['d']['Calendars']) == 0:
            return None
        calendar_groups = []
        Calendar._load_calendar(campus, data['d']['Calendars'],
                                calendar_groups)
        return calendar_groups

    re_email = re.compile(r'\S+@washington.edu')

    @staticmethod
    def _is_valid_email(email):
        return Calendar.re_email.match(email) is not None

    @staticmethod
    def _extract_uwnetid(email):
        return re.sub("@washington.edu", "", email)

    @staticmethod
    def _load_permissions(campus, calendarid, resp_fragment, permissions):
        """
        :return: Permissions[]
        """
        for record in resp_fragment:
            if not Calendar._is_valid_email(record['Email']):
                # skip the non UW users
                continue
            perm = Permission()
            perm.calendarid = calendarid
            perm.campus = campus
            perm.uwnetid = Calendar._extract_uwnetid(record['Email'])
            perm.level = record['Level']
            perm.name = record['Name']
            permissions.append(perm)

    @staticmethod
    def _process_get_perm_resp(url, post_response, campus, calendarid):
        """
        If the response is successful, process the response data 
        and load into a list of Permission objects; 
        otherwise raise DataFailureException
        :return: Permissions[]
        """
        request_id = "%s %s CalendarID:%s" % (campus, url, calendarid)
        if post_response.status != 200 or post_response.data is None:
            raise DataFailureException(request_id,
                                       post_response.status,
                                       post_response.data)
        data = json.loads(post_response.data)
        Calendar._check_err(data)
        if data['d']['Users'] is None or len(data['d']['Users']) == 0:
            return None
        permissions = []
        Calendar._load_permissions(campus, calendarid, 
                                   data['d']['Users'], permissions)
        return permissions

    @staticmethod
    def _check_err(data):
        """
        Check possible error code returned in the response body
        raise the coresponding exceptions
        """
        if data['d'] is None:
            raise NoDataReturned()
        if data['d']['Messages'] is None:
            return

        msg = data['d']['Messages']
        if len(msg) == 0 or msg[0]['Code'] is None:
            raise UnknownError()

        code = int(msg[0]['Code'])
        if code == 3006:
            raise CalendarNotExist()
        elif code == 3007:
            raise CalendarOwnByDiffAccount()
        else:
            logger.error(
                "Invalid Error Code: %s %s" % (
                    code, msg[0]['Description']))


