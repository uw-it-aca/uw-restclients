from restclients.sws.v4.graderoster import get_graderoster as v4_get_graderoster
from restclients.sws.v4.graderoster import update_graderoster as v4_update_graderoster
from restclients.sws.v4.graderoster import graderoster_from_xhtml as v4_graderoster_from_xhtml

def get_graderoster(*args, **kwargs):
    return v4_get_graderoster(*args, **kwargs)

def update_graderoster(*args, **kwargs):
    return v4_update_graderoster(*args, **kwargs)

def graderoster_from_xhtml(*args, **kwargs):
    return v4_graderoster_from_xhtml(*args, **kwargs)

