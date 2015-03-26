import json
from restclients.dao import IASYSTEM_DAO
from restclients.exceptions import DataFailureException


def get_resource(url):
    """
    Issue a GET request to IASystem with the given url
    and return a response in Collection+json format.
    :returns: http response with content in json
    """
    headers = {"Accept": "application/vnd.collection+json"}
    response = IASYSTEM_DAO().getURL(url, headers)
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)
    return json.loads(response.data)
