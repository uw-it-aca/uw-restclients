from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import render_to_response
from restclients.dao import SWS_DAO, PWS_DAO, GWS_DAO, NWS_DAO
from authz_group import Group
from userservice.user import UserService
from time import time
from urllib import quote, unquote, urlencode
import json
import re


@login_required
@csrf_protect
def proxy(request, service, url):

    if not hasattr(settings, "RESTCLIENTS_ADMIN_GROUP"):
        print "You must have a group defined as your admin group."
        print 'Configure that using RESTCLIENTS_ADMIN_GROUP="u_foo_bar"'
        raise Exception("Missing RESTCLIENTS_ADMIN_GROUP in settings")

    user_service = UserService()
    actual_user = user_service.get_original_user()
    g = Group()
    is_admin = g.is_member_of_group(actual_user, settings.RESTCLIENTS_ADMIN_GROUP)

    if is_admin == False:
        return HttpResponseRedirect("/")

    headers = {}
    if service == "sws":
        dao = SWS_DAO()
        headers["X-UW-Act-as"] = actual_user
    elif service == "pws":
        dao = PWS_DAO()
    elif service == "gws":
        dao = GWS_DAO()
    elif service == "nws":
        dao = NWS_DAO()
    else:
        return HttpResponseNotFound("Unknown service: %s" % service)

    url = "/%s" % quote(url)

    if request.GET:
        url = "%s?%s" % (url, urlencode(request.GET))

    start = time()
    response = dao.getURL(url, headers)
    end = time()

    # Assume json, and try to format it.
    try:
        content = format_json(service, response.data)
    except Exception as e:
        content = format_html(service, response.data)

    context = {
        "url": unquote(url),
        "content": content,
        "response_code": response.status,
        "time_taken": "%f seconds" % (end - start),
        "headers": response.headers,
        "override_user": user_service.get_override_user(),
    }

    try:
        loader.get_template("restclients/extra_info.html")
        context["has_extra_template"] = True
        context["extra_template"] = "restclients/extra_info.html"
    except TemplateDoesNotExist:
        pass

    try:
        loader.get_template("restclients/proxy_wrapper.html")
        context["wrapper_template"] = "restclients/proxy_wrapper.html"
    except TemplateDoesNotExist:
        context["wrapper_template"] = "proxy_wrapper.html"

    return render_to_response("proxy.html",
                              context,
                              context_instance=RequestContext(request))

def format_json(service, content):
    json_data = json.loads(content)
    formatted = json.dumps(json_data, sort_keys=True, indent=4)
    formatted = formatted.replace("&", "&amp;")
    formatted = formatted.replace("<", "&lt;")
    formatted = formatted.replace(">", "&gt;")
    formatted = formatted.replace(" ", "&nbsp;")
    formatted = formatted.replace("\n", "<br/>\n")

    formatted = re.sub(r"\"/(.*?)\"", r"<a href='/restclients/view/%s/\1'>/\1</a>" % service, formatted)

    return formatted

def format_html(service, content):
    formatted = re.sub(r"href\s*=\s*\"/(.*?)\"", r"href='/restclients/view/%s/\1'" % service, content)
    formatted = re.sub(re.compile(r"<style.*/style>", re.S), "", formatted)
    formatted = clean_self_closing_divs(formatted)
    return formatted

def clean_self_closing_divs(content):
    cleaned = re.sub("((<div[^>]*?)/>)", "<!-- \g<1> -->\g<2>></div>", content)
    return cleaned

