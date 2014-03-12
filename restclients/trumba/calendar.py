"""
Interfacing with Trumba Calendars' service, this module
provides methods to obtain calendar info and
user calendar permissions in Trumba

The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""

import logging
import json
import re
from restclients.models.trumba import TrumbaCalendar, Permission, is_bot, is_sea, is_tac
from restclients.exceptions import DataFailureException
import restclients.trumba as Trumba
from restclients.trumba.exceptions import CalendarOwnByDiffAccount, CalendarNotExist, NoDataReturned, UnknownError, UnexpectedError

logger = logging.getLogger(__name__)

get_calendarlist_url = "/service/calendars.asmx/GetCalendarList"
get_permissions_url = "/service/calendars.asmx/GetPermissions"

def get_campus_calendars(campus_code):
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             corresponding to the given campus calendars.
             None if error, {} if not exists
    raise DataFailureException if the request failed.
    """
    if is_bot(campus_code):
        return get_bot_calendars()
    elif is_sea(campus_code):
        return get_sea_calendars()
    elif is_tac(campus_code):
        return get_tac_calendars()
    else:
        logger.warn(
            "Calling get_campus_calendars with invalid campus code: %s" 
            % campus_code)
        return None

def get_bot_calendars():
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             corresponding to Bothell calendars. 
             None if error, {} if not exists
    raise DataFailureException if the request failed.
    """
    return _process_get_cal_resp(
        get_calendarlist_url,
        Trumba.post_bot_resource(get_calendarlist_url,"{}"),
        TrumbaCalendar.BOT_CAMPUS_CODE)

def get_sea_calendars():
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             corresponding to Seattle calendars. 
             None if error, {} if not exists
    raise DataFailureException if the request failed.
    """
    return _process_get_cal_resp(
        get_calendarlist_url,
        Trumba.post_sea_resource(get_calendarlist_url,"{}"),
        TrumbaCalendar.SEA_CAMPUS_CODE)

def get_tac_calendars():
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             corresponding to Tacoma calendars. 
             None if error, {} if not exists
    raise DataFailureException if the request failed.
    """
    return _process_get_cal_resp(
        get_calendarlist_url,
        Trumba.post_tac_resource(get_calendarlist_url,"{}"),
        TrumbaCalendar.TAC_CAMPUS_CODE)

def get_campus_permissions(calendar_id, campus_code):
    """
    :return: a list of trumba.Permission objects
             corresponding to the given campus calendar.
             None if error, [] if not exists
    raise DataFailureException if the request failed.
    """
    if is_bot(campus_code):
        return get_bot_permissions(calendar_id)
    elif is_sea(campus_code):
        return get_sea_permissions(calendar_id)
    elif is_tac(campus_code):
        return get_tac_permissions(calendar_id)
    else:
        logger.warn(
            "Calling get_campus_permissions with invalid campus code: %s" 
            % campus_code)
        return None

def _create_get_perm_body(calendar_id):
    return json.dumps({'CalendarID': calendar_id})

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
    return _process_get_perm_resp(
        get_permissions_url,
        Trumba.post_bot_resource(get_permissions_url,
                                 _create_get_perm_body(calendar_id)),
        TrumbaCalendar.BOT_CAMPUS_CODE,
        calendar_id)

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
    return _process_get_perm_resp(
        get_permissions_url,
        Trumba.post_sea_resource(get_permissions_url,
                                 _create_get_perm_body(calendar_id)),
        TrumbaCalendar.SEA_CAMPUS_CODE,
        calendar_id)

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
    return _process_get_perm_resp(
        get_permissions_url,
        Trumba.post_tac_resource(get_permissions_url,
                                 _create_get_perm_body(calendar_id)),
        TrumbaCalendar.TAC_CAMPUS_CODE,
        calendar_id)

re_cal_id = re.compile(r'[1-9]\d*')

def _is_valid_calendarid(calendarid):
    return re_cal_id.match(str(calendarid)) is not None

def _load_calendar(campus, resp_fragment, calendar_dict, parent):
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             None if error, {} if not exists
    """
    for record in resp_fragment:
        if re.match('Internal Event Actions', record['Name']) or re.match('Migrated .*', record['Name']) :
            continue
        trumba_cal = TrumbaCalendar()
        trumba_cal.calendarid = record['ID']
        trumba_cal.campus = campus
        if parent is None:
            trumba_cal.name = record['Name']
        else:
            trumba_cal.name = "%s >> %s" % (parent, record['Name'])

        if not _is_valid_calendarid(record['ID']):
            logger.warn(
                "InvalidCalendarId %s, entry skipped!" % trumba_cal)
            continue

        calendar_dict[trumba_cal.calendarid] = trumba_cal
        if record['ChildCalendars'] is not None and len(record['ChildCalendars']) > 0:
            _load_calendar(campus, 
                           record['ChildCalendars'], 
                           calendar_dict,
                           trumba_cal.name)

def _process_get_cal_resp(url, post_response, campus):
    """
    :return: a dictionary of {calenderid, TrumbaCalendar}
             None if error, {} if not exists
    If the request is successful, process the response data 
    and load the json data into the return object.
    """
    request_id = "%s %s" % (campus, url)
    calendar_dict = {}
    data = _load_json(request_id, post_response)
    if data['d']['Calendars'] is not None and len(data['d']['Calendars']) > 0:
        _load_calendar(campus, data['d']['Calendars'],
                       calendar_dict, None)
    return calendar_dict

re_email = re.compile(r'[a-z][a-z0-9]+@washington.edu')

def _is_valid_email(email):
    return re_email.match(email) is not None

def _extract_uwnetid(email):
    return re.sub("@washington.edu", "", email)

def _load_permissions(campus, calendarid, resp_fragment, permission_list):
    """
    :return: a list of trumba.Permission objects
             None if error, [] if not exists
    """
    for record in resp_fragment:
        if not _is_valid_email(record['Email']):
            # skip the non UW users
            continue
        perm = Permission()
        perm.calendarid = calendarid
        perm.campus = campus
        perm.uwnetid = _extract_uwnetid(record['Email'])
        perm.level = record['Level']
        perm.name = unicode(record['Name'])
        permission_list.append(perm)

def _process_get_perm_resp(url, post_response, campus, calendarid):
    """
    :return: a list of trumba.Permission objects
             None if error, [] if not exists
    If the response is successful, process the response data 
    and load into the return objects 
    otherwise raise DataFailureException
    """
    request_id = "%s %s CalendarID:%s" % (campus, url, calendarid)
    data = _load_json(request_id, post_response)
    permission_list = []
    if data['d']['Users'] is not None and len(data['d']['Users']) > 0:
        _load_permissions(campus, calendarid, 
                          data['d']['Users'], 
                          permission_list)
    return permission_list

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

def _load_json(request_id, post_response):
    if post_response.status != 200:
        raise DataFailureException(request_id,
                                   post_response.status,
                                   post_response.reason)
    if post_response.data is None:
        raise NoDataReturned()
    data = json.loads(post_response.data)
    _check_err(data)
    return data
