"""
Interfacing Trumba Accounts' Service, the account module provides
functions for adding and deleting editors and set their calendar permissions

The underline http requests and responses will be logged.
Be sure to set the logging configuration if you use the LiveDao!
"""


from functools import partial
import logging
import re
from lxml import etree, objectify
from urllib import quote, unquote
from restclients.exceptions import DataFailureException
from restclients.models.trumba import Permission
from restclients.trumba import get_bot_resource, get_sea_resource,\
    get_tac_resource
from restclients.trumba.exceptions import AccountNameEmpty, AccountNotExist,\
    AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount,\
    InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher,\
    NoAllowedPermission, ErrorCreatingEditor, NoDataReturned,\
    UnexpectedError, UnknownError


add_account_url_prefix = "/service/accounts.asmx/CreateEditor"
del_account_url_prefix = "/service/accounts.asmx/CloseEditor"
set_permission_url_prefix = "/service/calendars.asmx/SetPermissions"


def _make_add_account_url(name, userid):
    """
    :return: the URL string for the GET request call to
    Trumba CreateEditor method
    """
    return "%s?Name=%s&Email=%s@washington.edu&Password=" % (
        add_account_url_prefix, re.sub(' ', '%20', name), userid)


def add_editor(name, userid):
    """
    :param name: a string representing the user's name
    :param userid: a string representing the user's UW NetID
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_add_account_url(name, userid)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_editor_added
                         )


def _make_del_account_url(userid):
    """
    :return: the URL string for GET request call to
    Trumba CloseEditor method
    """
    return "%s?Email=%s@washington.edu" % (del_account_url_prefix, userid)


def delete_editor(userid):
    """
    :param userid: a string representing the user's UW NetID
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_del_account_url(userid)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_editor_deleted
                         )


def _make_set_permissions_url(calendar_id, userid, level):
    """
    :return: the URL string for GET request call
    to Trumba SetPermissions method
    """
    return "%s?CalendarID=%s&Email=%s@washington.edu&Level=%s" % (
        set_permission_url_prefix, calendar_id, userid, level)


def set_bot_editor(calendar_id, userid):
    return set_bot_permissions(calendar_id, userid, Permission.EDIT)


def set_bot_showon(calendar_id, userid):
    return set_bot_permissions(calendar_id, userid, Permission.SHOWON)


def set_bot_none(calendar_id, userid):
    return set_bot_permissions(calendar_id, userid, Permission.NONE)


def set_bot_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_bot_resource(url),
                         _is_permission_set
                         )


def set_sea_editor(calendar_id, userid):
    return set_sea_permissions(calendar_id, userid, Permission.EDIT)


def set_sea_showon(calendar_id, userid):
    return set_sea_permissions(calendar_id, userid, Permission.SHOWON)


def set_sea_none(calendar_id, userid):
    return set_sea_permissions(calendar_id, userid, Permission.NONE)


def set_sea_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_sea_resource(url),
                         _is_permission_set
                         )


def set_tac_editor(calendar_id, userid):
    return set_tac_permissions(calendar_id, userid, Permission.EDIT)


def set_tac_showon(calendar_id, userid):
    return set_tac_permissions(calendar_id, userid, Permission.SHOWON)


def set_tac_none(calendar_id, userid):
    return set_tac_permissions(calendar_id, userid, Permission.NONE)


def set_tac_permissions(calendar_id, userid, level):
    """
    :param calendar_id: an integer representing calendar ID
    :param userid: a string representing the user's UW NetID
    :param level: a string representing the permission level
    :return: True if request is successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    url = _make_set_permissions_url(
        calendar_id, userid, level)
    return _process_resp(url,
                         get_tac_resource(url),
                         _is_permission_set
                         )


def _process_resp(request_id, response, is_success_func):
    """
    :param request_id: campus url identifying the request
    :param response: the GET method response object
    :param is_success_func: the name of the function for
        verifying a success code
    :return: True if successful, False otherwise.
    raise DataFailureException or a corresponding TrumbaException
    if the request failed or an error code has been returned.
    """
    if response.status != 200:
        raise DataFailureException(request_id,
                                   response.status,
                                   response.reason
                                   )
    if response.data is None:
        raise NoDataReturned()
    root = objectify.fromstring(response.data)
    if root.ResponseMessage is None or\
            root.ResponseMessage.attrib['Code'] is None:
        raise UnknownError()
    resp_code = int(root.ResponseMessage.attrib['Code'])
    func = partial(is_success_func)
    if func(resp_code):
        return True
    _check_err(resp_code, request_id)


def _is_editor_added(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1001 or code == 3012


def _is_editor_deleted(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1002


def _is_permission_set(code):
    """
    :param code: an integer value
    :return: True if the code means successful, False otherwise.
    """
    return code == 1003


def _check_err(code, request_id):
    """
    :param code: an integer value
    :param request_id: campus url identifying the request
    Check possible error code returned in the response body
    raise the corresponding TrumbaException
    """
    if code == 3006:
        raise CalendarNotExist()
    elif code == 3007:
        raise CalendarOwnByDiffAccount()
    elif code == 3008:
        raise AccountNotExist()
    elif code == 3009 or code == 3013:
        raise AccountUsedByDiffUser()
    elif code == 3010:
        raise InvalidPermissionLevel()
    elif code == 3011:
        raise FailedToClosePublisher()
    elif code == 3014:
        raise InvalidEmail()
    elif code == 3015:
        raise NoAllowedPermission()
    elif code == 3016:
        raise AccountNameEmpty()
    elif code == 3017 or code == 3018:
        raise ErrorCreatingEditor()
    else:
        logging.getLogger(__name__).warn(
            "Unexpected Error Code: %s with %s" % (
                code, request_id))
        raise UnexpectedError()
