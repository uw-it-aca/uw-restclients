from restclients.dao import R25_DAO
from restclients.exceptions import DataFailureException
from lxml import etree


nsmap = {"r25": "http://www.collegenet.com/r25"}


def get_resource(url):
    """
    Issue a GET request to R25 with the given url
    and return a response in xml format.
    :returns: http response with content in xml
    """
    response = R25_DAO().getURL(url, {"Accept": "text/xml"})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    return etree.fromstring(response.data.strip())
