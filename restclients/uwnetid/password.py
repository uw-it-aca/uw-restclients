"""
Interface for interacting with the UWNetID password resource
"""

from datetime import datetime
import logging
import json
from dateutil.parser import parse
from pytimeparse.timeparse import timeparse
from restclients.models.uwnetid import UwPassword
from restclients.uwnetid import get_resource


logger = logging.getLogger(__name__)
URL = "/nws/v1/uwnetid/%s/password"


def get_uwnetid_password(netid):
    """
    Return a restclients.models.uwnetid.PassWord object
    on the given uwnetid
    """
    return _process_json(get_resource(URL % netid))


def _process_json(response_body):
    """
    Returns a UwPassword objects
    """
    data = json.loads(response_body)
    uwpassword = UwPassword(uwnetid=data["uwNetID"],
                            kerb_status=data["kerbStatus"],
                            last_change=None,
                            last_change_med=None,
                            expires_med=None,
                            interval_med=None,
                            minimum_length=int(data["minimumLength"]),
                            time_stamp=parse(data["timeStamp"]),)
    if "lastChange" in data:
        uwpassword.last_change = parse(data["lastChange"])

    if "lastChangeMed" in data:
        uwpassword.last_change_med = parse(data["lastChangeMed"])

    if "expiresMed" in data:
        uwpassword.expires_med = parse(data["expiresMed"])

    if "intervalMed" in data:
        uwpassword.interval_med = timeparse(data["intervalMed"])

    if "netidStatus" in data:
        netid_status = []
        for status in data["netidStatus"]:
            netid_status.append(status)
        uwpassword.netid_status = netid_status
    return uwpassword
