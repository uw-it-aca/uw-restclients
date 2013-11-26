"""
The interface for accessing Trumba Calendars' Service 
"""

from restclients.models.trumba import TrumbaCalendar, Permission, is_bot, is_sea, is_tac
from restclients.exceptions import DataFailureException
from restclients.trumba.exceptions import CalendarOwnByDiffAccount, CalendarNotExist, NoDataReturned, UnknownError, UnexpectedError
from restclients.trumba import Trumba
import json
import logging
import re

class Calendar:
    """
    This class provides methods to obtain calendar info 
    and user calendar permissions in Trumba

    The underline http requests and responses will be logged.
    Be sure to set the logging configuration if you use the LiveDao!
    """

    get_calendarlist_url = "/service/calendars.asmx/GetCalendarList"
    get_permissions_url = "/service/calendars.asmx/GetPermissions"

    @staticmethod
    def get_campus_calendars(campus_code):
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 corresponding to the given campus calendars.
                 None if error, {} if not exists
        raise DataFailureException if the request failed.
        """
        if is_bot(campus_code):
            return Calendar.get_bot_calendars()
        elif is_sea(campus_code):
            return Calendar.get_sea_calendars()
        elif is_tac(campus_code):
            return Calendar.get_tac_calendars()
        else:
            None

    @staticmethod
    def get_bot_calendars():
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 corresponding to Bothell calendars. 
                 None if error, {} if not exists
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_bot_resource(Calendar.get_calendarlist_url,"{}"),
            TrumbaCalendar.BOT_CAMPUS_CODE)

    @staticmethod
    def get_sea_calendars():
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 corresponding to Seattle calendars. 
                 None if error, {} if not exists
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_sea_resource(Calendar.get_calendarlist_url,"{}"),
            TrumbaCalendar.SEA_CAMPUS_CODE)

    @staticmethod
    def get_tac_calendars():
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 corresponding to Tacoma calendars. 
                 None if error, {} if not exists
        raise DataFailureException if the request failed.
        """
        return Calendar._process_get_cal_resp(
            Calendar.get_calendarlist_url,
            Trumba.post_tac_resource(Calendar.get_calendarlist_url,"{}"),
            TrumbaCalendar.TAC_CAMPUS_CODE)

    @staticmethod
    def get_campus_permissions(calendar_id, campus_code):
        """
        :return: a list of trumba.Permission objects
                 corresponding to the given campus calendar.
                 None if error, [] if not exists
        raise DataFailureException if the request failed.
        """
        if is_bot(campus_code):
            return Calendar.get_bot_permissions(calendar_id)
        elif is_sea(campus_code):
            return Calendar.get_sea_permissions(calendar_id)
        elif is_tac(campus_code):
            return Calendar.get_tac_permissions(calendar_id)
        else:
            None

    @staticmethod
    def _create_get_perm_body(calendar_id):
        return json.dumps({'CalendarID': calendar_id})

    @staticmethod
    def get_bot_permissions(calendar_id):
        """
        :param calendar_id: an integer representing calendar ID
        :return: a list of trumba.Permission objects
                 corresponding to the given campus calendar.
                 None if error, [] if not exists
        Return a list of Permission objects representing
        the user permissions of a given Bothell calendar. 
        raise DataFailureException or a corresponding TrumbaException
        if the request failed or an error code has been returned.
        """
        return Calendar._process_get_perm_resp(
            Calendar.get_permissions_url,
            Trumba.post_bot_resource(Calendar.get_permissions_url,
                                     Calendar._create_get_perm_body(calendar_id)),
            TrumbaCalendar.BOT_CAMPUS_CODE,
            calendar_id)

    @staticmethod
    def get_sea_permissions(calendar_id):
        """
        Return a list of Permission objects representing
        the user permissions of a given Seattle calendar. 
        :return: a list of trumba.Permission objects
                 corresponding to the given campus calendar.
                 None if error, [] if not exists
        raise DataFailureException or a corresponding TrumbaException
        if the request failed or an error code has been returned.
        """
        return Calendar._process_get_perm_resp(
            Calendar.get_permissions_url,
            Trumba.post_sea_resource(Calendar.get_permissions_url,
                                     Calendar._create_get_perm_body(calendar_id)),
            TrumbaCalendar.SEA_CAMPUS_CODE,
            calendar_id)

    @staticmethod
    def get_tac_permissions(calendar_id):
        """
        Return a list of Permission objects representing
        the user permissions of a given Tacoma calendar. 
        :return: a list of trumba.Permission objects
                 corresponding to the given campus calendar.
                 None if error, [] if not exists
        raise DataFailureException or a corresponding TrumbaException
        if the request failed or an error code has been returned.
        """
        return Calendar._process_get_perm_resp(
            Calendar.get_permissions_url,
            Trumba.post_tac_resource(Calendar.get_permissions_url,
                                     Calendar._create_get_perm_body(calendar_id)),
            TrumbaCalendar.TAC_CAMPUS_CODE,
            calendar_id)

    re_cal_id = re.compile(r'[1-9]\d*')

    @staticmethod
    def _is_valid_calendarid(calendarid):
        return Calendar.re_cal_id.match(str(calendarid)) is not None

    @staticmethod
    def _load_calendar(campus, resp_fragment, calendar_dict):
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 None if error, {} if not exists
        """
        logger = logging.getLogger(__name__)
        for record in resp_fragment:
            if re.match('Internal Event Actions', record['Name']) or re.match('Migrated events', record['Name']) :
                continue
            trumba_cal = TrumbaCalendar()
            trumba_cal.calendarid = record['ID']
            trumba_cal.campus = campus
            trumba_cal.name = record['Name']
            if not Calendar._is_valid_calendarid(record['ID']):
                logger.warn(
                    "%s InvalidCalendarId, entry skipped!" % trumba_cal)
                continue
            calendar_dict[trumba_cal.calendarid] = trumba_cal
            if record['ChildCalendars'] is not None and len(record['ChildCalendars']) > 0:
                Calendar._load_calendar(campus, 
                                        record['ChildCalendars'], 
                                        calendar_dict)

    @staticmethod
    def _process_get_cal_resp(url, post_response, campus):
        """
        :return: a dictionary of {calenderid, TrumbaCalendar}
                 None if error, {} if not exists
        If the request is successful, process the response data 
        and load the json data into the return object.
        """
        request_id = "%s %s" % (campus, url)
        calendar_dict = {}
        data = Calendar._load_json(request_id, post_response)
        if data['d']['Calendars'] is not None and len(data['d']['Calendars']) > 0:
            Calendar._load_calendar(campus, data['d']['Calendars'],
                                    calendar_dict)
        return calendar_dict

    re_email = re.compile(r'[a-z][a-z0-9]+@washington.edu')

    @staticmethod
    def _is_valid_email(email):
        return Calendar.re_email.match(email) is not None

    @staticmethod
    def _extract_uwnetid(email):
        return re.sub("@washington.edu", "", email)

    @staticmethod
    def _load_permissions(campus, calendarid, resp_fragment, permission_list):
        """
        :return: a list of trumba.Permission objects
                 None if error, [] if not exists
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
            perm.name = unicode(record['Name'])
            permission_list.append(perm)

    @staticmethod
    def _process_get_perm_resp(url, post_response, campus, calendarid):
        """
        :return: a list of trumba.Permission objects
                 None if error, [] if not exists
        If the response is successful, process the response data 
        and load into the return objects 
        otherwise raise DataFailureException
        """
        request_id = "%s %s CalendarID:%s" % (campus, url, calendarid)
        data = Calendar._load_json(request_id, post_response)
        permission_list = []
        if data['d']['Users'] is not None and len(data['d']['Users']) > 0:
            Calendar._load_permissions(campus, calendarid, 
                                       data['d']['Users'], 
                                       permission_list)
        return permission_list

    @staticmethod
    def _check_err(data):
        """
        :param data: response json data object (must be not None).
        Check possible error code returned in the response body
        raise the coresponding exceptions
        """
        logger = logging.getLogger(__name__)
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
            logger.warn(
                "Unexpected Error Code: %s %s" % (
                    code, msg[0]['Description']))
            raise UnexpectedError()


    @staticmethod
    def _load_json(request_id, post_response):
        if post_response.status != 200:
            raise DataFailureException(request_id,
                                       post_response.status,
                                       post_response.reason)
        if post_response.data is None:
            raise NoDataReturned()
        data = json.loads(post_response.data)
        Calendar._check_err(data)
        return data
