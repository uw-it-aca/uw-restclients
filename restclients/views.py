from django.http import HttpResponse, HttpResponseRedirect
from restclients.dao import SWS_DAO, PWS_DAO, GWS_DAO
from restclients.gws import GWS
from django.conf import settings

def proxy(request, service, url):

    if not hasattr(settings, "RESTCLIENTS_ADMIN_GROUP"):
        print "You must have a group in GWS defined as your admin group."
        print 'Configure that using RESTCLIENTS_ADMIN_GROUP="u_foo_bar"'
        raise Exception("Missing RESTCLIENTS_ADMIN_GROUP in settings")

    gws = GWS()
    members = gws.get_effective_members(settings.MYUW_ADMIN_GROUP)

    if settings.DEBUG:
        actual_user = 'javerage'
    else:
        actual_user = request.user.username

    is_admin = False

    # XXX - use a new GWS method for is effective member :(
    for member in members:
        if member.uwnetid == actual_user:
            is_admin = True
            break

    if is_admin == False:
        return HttpResponseRedirect("/")

    if service == "sws":
        dao = SWS_DAO()
    elif service == "pws":
        dao = PWS_DAO()
    elif service == "gws":
        dao = GWS_DAO()
    else:
        raise Exception("Unknown service: %s" % service)

    url = "/%s" % url
    response = dao.getURL(url, {"Accept":"application/json"})

    return HttpResponse(response.data)

