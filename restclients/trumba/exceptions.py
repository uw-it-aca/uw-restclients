"""
Exceptions when Trumba's Web services returns an error in
a successful request.
"""

class TrumbaException(Exception):
    def __str__(self):
        return self.__class__.__name__


class AccountNameEmpty(TrumbaException):
    """
    Exception when creating an account with an empty name
    """
    pass

class AccountNotExist(TrumbaException):
    """
    Exception when the account has not been created
    """
    pass

class AccountUsedByDiffUser(TrumbaException):
    """
    Exception when the account already been used for another user
    """
    pass

class CalendarNotExist(TrumbaException):
    """
    Exception when the given calendar ID doesn't exist.
    Coresponding to Trumba error code: 3006
    """
    pass

class CalendarOwnByDiffAccount(TrumbaException):
    """
    Exception when the given calendar ID beongs to a different account.
    Coresponding to Trumba error code: 3007
    """
    pass

class ErrorCreatingEditor(TrumbaException):
    """
    Exception when other errors occur on a creating editor request 
    """
    pass

class FailedToClosePublisher(TrumbaException):
    """
    Exception when the account to close is a publisher account
    """
    pass

class InvalidEmail(TrumbaException):
    """
    Exception when creating an account with an invalid email address
    """
    pass

class InvalidPermissionLevel(TrumbaException):
    """
    Exception when the permission level is not valid
    """
    pass

class NoAllowedPermission(TrumbaException):
    """
    Exception when the permission level is not allowed for this account
    """
    pass

class NoDataReturned(TrumbaException):
    """
    Exception when there is empty data in the response
    """
    pass

class UnknownError(TrumbaException):
    """
    Exception when there is Messages in the response but no error code presents
    """
    pass

