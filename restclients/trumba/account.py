from urllib import quote, unquote
from restclients.trumba import Trumba
from restclients.trumba.exceptions import AccountNameEmpty, AccountNotExist, AccountUsedByDiffUser, CalendarNotExist, CalendarOwnByDiffAccount, InvalidEmail, InvalidPermissionLevel, FailedToClosePublisher, NoAllowedPermission, ErrorCreatingEditor, NoDataReturned, UnexpectedError, UnknownError
from restclients.exceptions import DataFailureException
from restclients.util.log import null_handler
import logging
import re
from lxml import etree, objectify
from functools import partial

class Account:
    """
    Access editors of the calendar, viewer and showon permission 
    holders of the calendar
    """

    logger = logging.getLogger(__name__)
    logger.addHandler(null_handler)

    @staticmethod
    def _make_add_editor_url(name, userid):
        """
        :return: the URL string for the GET request call to 
        Trumba CreateEditor method
        """
        return "/service/accounts.asmx/CreateEditor?Name=%s&Email=%s@washington.edu&Password=" % (re.sub(' ', '%20', name), userid) 

    @staticmethod
    def add_editor(name, userid):
        """
        :param name: a string representing the user's name
        :param userid: a string representing the user's UW NetID
        :return: Ture if request is successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        url = Account._make_add_editor_url(name, userid)
        return Account._process_resp(
            url,
            Trumba.get_sea_resource(url),
            Account._is_editor_added)

    @staticmethod
    def _make_del_editor_url(userid):
        """
        :return: the URL string for GET request call to 
        Trumba CloseEditor method
        """
        return "/service/accounts.asmx/CloseEditor?Email=%s@washington.edu" % userid

    @staticmethod
    def delete_editor(userid):
        """
        :param userid: a string representing the user's UW NetID
        :return: Ture if request is successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        url = Account._make_del_editor_url(userid)
        return Account._process_resp(
            url,
            Trumba.get_sea_resource(url),
            Account._is_editor_deleted)

    @staticmethod    
    def _make_set_permissions_url(calendar_id, userid, level):
        """
        :return: the URL string for GET request call 
        to Trumba SetPermissions method
        """
        return "/service/calendars.asmx/SetPermissions?CalendarID=%s&Email=%s@washington.edu&Level=%s" % (calendar_id, userid, level) 

    @staticmethod
    def set_bot_permissions(calendar_id, userid, level):
        """
        :param calendar_id: an integer representing calendar ID
        :param userid: a string representing the user's UW NetID
        :param level: a string representing the permission level
        :return: Ture if request is successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        url = Account._make_set_permissions_url(
            calendar_id, userid, level)
        return Account._process_resp(
            url,
            Trumba.get_bot_resource(url),
            Account._is_permission_set)

    @staticmethod
    def set_sea_permissions(calendar_id, userid, level):
        """
        :param calendar_id: an integer representing calendar ID
        :param userid: a string representing the user's UW NetID
        :param level: a string representing the permission level
        :return: Ture if request is successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        url = Account._make_set_permissions_url(
            calendar_id, userid, level)
        return Account._process_resp(
            url,
            Trumba.get_sea_resource(url),
            Account._is_permission_set)

    @staticmethod
    def set_tac_permissions(calendar_id, userid, level):
        """
        :param calendar_id: an integer representing calendar ID
        :param userid: a string representing the user's UW NetID
        :param level: a string representing the permission level
        :return: Ture if request is successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        url = Account._make_set_permissions_url(
            calendar_id, userid, level)
        return Account._process_resp(
            url,
            Trumba.get_tac_resource(url),
            Account._is_permission_set)

    @staticmethod
    def _process_resp(request_id, response, is_success_func):
        """
        :param request_id: campus url identifying the request
        :param response: the GET method response object
        :param is_success_func: the name of the function for verifying a success code
        :return: Ture if successful, False otherwise.
        raise DataFailureException or a corresponding TrumbaException 
        if the request failed or an error code has been returned.
        """
        if response.status != 200:
            Account.logger.error("DataFailureException (%s, %s) when %s" % (
                    post_response.status, post_response.reason, request_id))
            raise DataFailureException(request_id,
                                       response.status,
                                       response.reason)
        if response.data is None:
            raise NoDataReturned()
        root = objectify.fromstring(response.data)
        if root.ResponseMessage is None or root.ResponseMessage.attrib['Code'] is None:
            raise UnknownError()
        resp_code = int(root.ResponseMessage.attrib['Code'])
        func = partial(is_success_func)
        if func(resp_code):
            return True
        Account._check_err(resp_code)


    @staticmethod
    def _is_editor_added(code):
        """
        :param code: an integer value  
        :return: Ture if the code means successful, False otherwise.
        """
        return (code == 1001 or code == 3012)

    @staticmethod
    def _is_editor_deleted(code):
        """
        :param code: an integer value  
        :return: Ture if the code means successful, False otherwise.
        """
        return code == 1002

    @staticmethod
    def _is_permission_set(code):
        """
        :param code: an integer value  
        :return: Ture if the code means successful, False otherwise.
        """
        return code == 1003

    @staticmethod
    def _check_err(code):
        """
        :param code: an integer value  
        Check possible error code returned in the response body
        raise the coresponding TrumbaException
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
            raise UnexpectedError()
