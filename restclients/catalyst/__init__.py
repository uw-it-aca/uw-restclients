from restclients.dao import Catalyst_DAO
from restclients.exceptions import DataFailureException
import json


def get_resource(url, headers):
    """
    Issue a GET request with the given url and headers,
    and return a response in json format.
    :returns: http response with content in json
    """
    headers["Accept"] = "application/json"
    response = Catalyst_DAO().getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    try:
        return json.loads(response.data)
    except ValueError as ex:
        raise DataFailureException(url, response.status, response.data)
