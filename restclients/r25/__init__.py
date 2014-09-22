from restclients.dao import R25_DAO
from restclients.exceptions import DataFailureException
from lxml import etree


nsmap = {"r25": "http://www.collegenet.com/r25",
         "xhtml": "http://www.w3.org/1999/xhtml"}


def get_resource(url):
    """
    Issue a GET request to R25 with the given url
    and return a response as an etree element.
    """
    response = R25_DAO().getURL(url, {"Accept": "text/xml"})
    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    tree = etree.fromstring(response.data.strip())

    # XHTML response is an error response
    xhtml = tree.xpath("//xhtml:html", namespaces=nsmap)
    if len(xhtml):
        raise DataFailureException(url, 500, response.data)

    return tree
