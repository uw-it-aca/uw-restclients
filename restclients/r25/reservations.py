from restclients.models.r25 import Reservation, Event
from restclients.r25 import nsmap, get_resource
from urllib import urlencode


def get_reservation_by_id(reservation_id):
    url = "/r25ws/servlet/wrd/run/reservation.xml?rsrv_id=%s" % reservation_id
    return reservations_from_xml(get_resource(url))[0]

def get_reservations(params={}):
    """
    Return a list of reservations matching the passed filter. Supported params
    are:
        
        event_id (integer)
        space_id (integer)
        start_dt (datetime)
        end_dt (datetime)
    """
    params["scope"] = "extended"
    url = "/r25ws/servlet/wrd/run/reservations.xml"
    if len(params):
        url += "?%s" % urlencode(params)

    return reservations_from_xml(get_resource(url))

#def get_reservations_by_space_id(space_id):
#    url = "/r25ws/servlet/wrd/run/rm_reservations.xml?space_id=%s" % space_id
#    return reservations_from_xml(get_resource(url))

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
        #TODO: add Event model
        reservations.append(reservation)

    return reservations
