from restclients.models.r25 import Reservation
from restclients.r25 import nsmap, get_resource
from restclients.r25.spaces import space_reservation_from_xml
from urllib import urlencode


def get_reservation_by_id(reservation_id):
    url = "/r25ws/servlet/wrd/run/reservation.xml?rsrv_id=%s" % reservation_id
    return reservations_from_xml(get_resource(url))[0]


def get_reservations(**kwargs):
    """
    Return a list of reservations matching the passed filter.
    Supported kwargs are listed at
    http://knowledge25.collegenet.com/display/WSW/reservations.xml
    """
    kwargs["scope"] = "extended"
    url = "/r25ws/servlet/wrd/run/reservations.xml"
    if len(kwargs):
        url += "?%s" % urlencode(kwargs)

    return reservations_from_xml(get_resource(url))


def reservations_from_xml(tree):
    reservations = []
    for node in tree.xpath("//r25:reservation", namespaces=nsmap):
        reservation = Reservation()
        reservation.reservation_id = node.xpath("r25:reservation_id",
                                                namespaces=nsmap)[0].text
        reservation.start_datetime = node.xpath("r25:reservation_start_dt",
                                                namespaces=nsmap)[0].text
        reservation.end_datetime = node.xpath("r25:reservation_end_dt",
                                              namespaces=nsmap)[0].text
        reservation.state = node.xpath("r25:reservation_state",
                                       namespaces=nsmap)[0].text

        try:
            pnode = node.xpath("r25:space_reservation", namespaces=nsmap)[0]
            reservation.space_reservation = space_reservation_from_xml(pnode)
        except IndexError:
            reservation.space_reservation = None

        try:
            enode = node.xpath("r25:event", namespaces=nsmap)[0]
            reservation.event_id = enode.xpath("r25:event_id",
                                               namespaces=nsmap)[0].text
        except IndexError:
            enode = tree.getparent()
            reservation.event_id = enode.xpath("r25:event_id",
                                               namespaces=nsmap)[0].text

        reservations.append(reservation)

    return reservations
