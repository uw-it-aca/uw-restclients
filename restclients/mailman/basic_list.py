"""
Interface for interacting with the mailman uwnetid resource
"""

import json
from django.conf import settings
from restclients.mailman import get_resource


URL = "/%s/admin/v1.0/uwnetid/available/?uwnetid=%s"
MAILMAN_ADMIN_URL = "https://mailman.u.washington.edu/mailman/admin/%s"


def _get_url_path(list_name):
    """
    Live Dao requires RESTCLIENTS_MAILMAN_KEY in the settings.py
    """
    access_key = getattr(settings,
                         "RESTCLIENTS_MAILMAN_KEY",
                         "__mock_key__")
    return URL % (access_key, list_name)


def exists(list_name):
    """
    Return True if the corresponding mailman list is avaliable
    for the given list name string
    @param list_name: a non_empty string
    """
    return _process_json(get_resource(_get_url_path(list_name)))


def _process_json(response_body):
    """
    Returns True the list already exists
    """
    data = json.loads(response_body)
    return "Available" in data and data["Available"] == "False"


def get_admin_url(list_name):
    return MAILMAN_ADMIN_URL % list_name
