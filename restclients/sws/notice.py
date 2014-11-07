from restclients.sws.v4.notice import get_notices_by_regid as v4_get_notices_by_regid
from restclients.sws.v5.notice import get_notices_by_regid as v5_get_notices_by_regid
from restclients.sws import use_v5_resources

def get_notices_by_regid(*args, **kwargs):
    if use_v5_resources():
        return v5_get_notices_by_regid(*args, **kwargs)
    else:
        return v4_get_notices_by_regid(*args, **kwargs)
