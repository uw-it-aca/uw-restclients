"""
Interfacing with the Student Web Service, Personal Financial resource
"""
import logging
from restclients.models.sws import Finance
from restclients.sws import get_resource


logger = logging.getLogger(__name__)
sws_url_prefix = "/student/v5/person/"
sws_url_suffix = "/financial.json"


def get_account_balances_by_regid(regid):
    """
    Returns a restclients.models.sws.Finance object
    """
    url = sws_url_prefix + regid + sws_url_suffix
    return _process_json_data(get_resource(url))


def _process_json_data(jdata):
    fina = Finance()
    fina.tuition_accbalance = jdata["AccountBalance"]
    if "PCEAccountBalance" in jdata:
        fina.pce_accbalance = jdata["PCEAccountBalance"]
    return fina

