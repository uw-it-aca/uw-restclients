from restclients.models.r25 import Space
from restclients.r25 import get_resource
from restclients.exceptions import DataFailureException
from lxml import etree


def get_space(space_id):
    url = "/r25ws/servlet/wrd/run/space.xml?space_id=%s" % space_id
    return space_from_xml(get_resource(url))


def get_spaces():
    url = "/r25ws/servlet/wrd/run/spaces.xml"
    #TODO: filter params


def space_from_xml(data):
    tree = etree.fromstring(data.strip())

    #TODO
    space = Space()
    return space
