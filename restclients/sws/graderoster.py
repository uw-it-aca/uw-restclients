from restclients.sws.v4.graderoster import get_graderoster as v4_get_graderoster
from restclients.sws.v4.graderoster import update_graderoster as v4_update_graderoster
from restclients.sws.v4.graderoster import graderoster_from_xhtml as v4_graderoster_from_xhtml
from restclients.sws.v5.graderoster import get_graderoster as v5_get_graderoster
from restclients.sws.v5.graderoster import update_graderoster as v5_update_graderoster
from restclients.sws.v5.graderoster import graderoster_from_xhtml as v5_graderoster_from_xhtml
from restclients.sws import use_v5_resources

def get_graderoster(*args, **kwargs):
    if use_v5_resources():
        return v5_get_graderoster(*args, **kwargs)
    else:
        return v4_get_graderoster(*args, **kwargs)

def update_graderoster(*args, **kwargs):
    if use_v5_resources():
        return v5_update_graderoster(*args, **kwargs)
    else:
        return v4_update_graderoster(*args, **kwargs)

def graderoster_from_xhtml(*args, **kwargs):
    if use_v5_resources():
        return v5_graderoster_from_xhtml(*args, **kwargs)
    else:
        return v4_graderoster_from_xhtml(*args, **kwargs)

