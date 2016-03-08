try:
    from importlib import import_module
except:
    # python 2.6
    from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import render_to_response
from restclients.dao import SWS_DAO, PWS_DAO, GWS_DAO, NWS_DAO, Hfs_DAO, \
    Book_DAO, Canvas_DAO, Uwnetid_DAO, Libraries_DAO, TrumbaCalendar_DAO, \
    MyPlan_DAO, IASYSTEM_DAO, Grad_DAO
from restclients.mock_http import MockHTTP
from authz_group import Group
from userservice.user import UserService
from time import time
from urllib import quote, unquote, urlencode
from urlparse import urlparse, parse_qs
import simplejson as json
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
    is_admin = g.is_member_of_group(actual_user,
                                    settings.RESTCLIENTS_ADMIN_GROUP)

    if not is_admin:
        return HttpResponseRedirect("/")

    use_pre = False
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
    elif service == "hfs":
        dao = Hfs_DAO()
    elif service == "book":
        dao = Book_DAO()
    elif service == "canvas":
        dao = Canvas_DAO()
    elif service == "grad":
        dao = Grad_DAO()
    elif service == "uwnetid":
        dao = Uwnetid_DAO()
    elif service == "libraries":
        dao = Libraries_DAO()
    elif service == "myplan":
        dao = MyPlan_DAO()
    elif service == "iasystem":
        dao = IASYSTEM_DAO()
        headers = {"Accept": "application/vnd.collection+json"}
        subdomain = None
        if url.endswith('/evaluation'):
            if url.startswith('uwb/') or url.startswith('uwt/'):
                subdomain = url[:3]
                url = url[4:]
            else:
                subdomain = url[:2]
                url = url[3:]
    elif service == "calendar":
        dao = TrumbaCalendar_DAO()
        use_pre = True
    else:
        return HttpResponseNotFound("Unknown service: %s" % service)

    url = "/%s" % quote(url)

    if request.GET:
        try:
            url = "%s?%s" % (url, urlencode(request.GET))
        except UnicodeEncodeError:
            err = "Bad URL param given to the restclients browser"
            return HttpResponse(err)

    start = time()
    try:
        if service == "iasystem" and subdomain is not None:
            response = dao.getURL(url, headers, subdomain)
        else:
            response = dao.getURL(url, headers)
    except Exception as ex:
        response = MockHTTP()
        response.status = 500
        response.data = str(ex)

    end = time()

    # Assume json, and try to format it.
    try:
        if not use_pre:
            content = format_json(service, response.data)
            json_data = response.data
        else:
            content = response.data
            json_data = None
    except Exception as e:
        content = format_html(service, response.data)
        json_data = None

    context = {
        "url": unquote(url),
        "content": content,
        "json_data": json_data,
        "response_code": response.status,
        "time_taken": "%f seconds" % (end - start),
        "headers": response.headers,
        "override_user": user_service.get_override_user(),
        "use_pre": use_pre,
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

    try:
        search_template_path = re.sub(r"\..*$", "", url)
        search_template = "proxy/%s%s.html" % (service, search_template_path)
        loader.get_template(search_template)
        context["search_template"] = search_template
        context["search"] = format_search_params(url)
    except TemplateDoesNotExist:
        context["search_template"] = None

    return render_to_response("proxy.html",
                              context,
                              context_instance=RequestContext(request))


def format_search_params(url):
    params = {}
    query_params = parse_qs(urlparse(url).query)
    for param in query_params:
        params[param] = ",".join(query_params[param])
    return params


def format_json(service, content):
    json_data = json.loads(content, use_decimal=True)
    formatted = json.dumps(json_data, sort_keys=True, indent=4)
    formatted = formatted.replace("&", "&amp;")
    formatted = formatted.replace("<", "&lt;")
    formatted = formatted.replace(">", "&gt;")
    formatted = formatted.replace(" ", "&nbsp;")
    formatted = formatted.replace("\n", "<br/>\n")

    formatted = re.sub(r"\"/(.*?)\"",
                       r'"<a href="/restclients/view/%s/\1">/\1</a>"' %
                       service, formatted)

    return formatted


def format_html(service, content):
    formatted = re.sub(r"href\s*=\s*\"/(.*?)\"",
                       r"href='/restclients/view/%s/\1'" % service, content)
    formatted = re.sub(re.compile(r"<style.*/style>", re.S), "", formatted)
    formatted = clean_self_closing_divs(formatted)
    return formatted


def clean_self_closing_divs(content):
    cleaned = re.sub("((<div[^>]*?)/>)", "<!-- \g<1> -->\g<2>></div>", content)
    return cleaned
