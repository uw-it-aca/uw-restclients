try:
    from importlib import import_module
except:
    # python 2.6
    from django.utils.importlib import import_module
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.shortcuts import render
from restclients.dao import SWS_DAO, PWS_DAO, GWS_DAO, NWS_DAO, Hfs_DAO,\
    Book_DAO, Canvas_DAO, Uwnetid_DAO, MyLibInfo_DAO, LibCurrics_DAO,\
    TrumbaCalendar_DAO, MyPlan_DAO, IASYSTEM_DAO, Grad_DAO
from restclients.mock_http import MockHTTP
from restclients.models.degrade_performance import DegradePerformance
from authz_group import Group
from userservice.user import UserService
from time import time
from urllib import quote, unquote, urlencode
from urlparse import urlparse, parse_qs
import simplejson as json
import re


def require_admin(view_func):
    def wrapper(*args, **kwargs):
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

        return view_func(*args, **kwargs)

    return wrapper


def set_wrapper_template(context):
    try:
        loader.get_template("restclients/proxy_wrapper.html")
        context["wrapper_template"] = "restclients/proxy_wrapper.html"
    except TemplateDoesNotExist:
        context["wrapper_template"] = "proxy_wrapper.html"


@login_required
@csrf_protect
@require_admin
def proxy(request, service, url):
    user_service = UserService()
    actual_user = user_service.get_original_user()

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
        dao = MyLibInfo_DAO()
    elif service == "libcurrics":
        dao = LibCurrics_DAO()
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
            if service == "libcurrics":
                if "?campus=" in url:
                    url = url.replace("?campus=", "/")
                elif "course?" in url:
                    url_prefix = re.sub(r'\?.*$', "", url)
                    url = "%s/%s/%s/%s/%s/%s" % (
                        url_prefix,
                        request.GET["year"],
                        request.GET["quarter"],
                        request.GET["curriculum_abbr"].replace(" ", "%20"),
                        request.GET["course_number"],
                        request.GET["section_id"])

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

    set_wrapper_template(context)

    try:
        search_template_path = re.sub(r"\..*$", "", url)
        search_template = "proxy/%s%s.html" % (service, search_template_path)
        loader.get_template(search_template)
        context["search_template"] = search_template
        context["search"] = format_search_params(url)
    except TemplateDoesNotExist:
        context["search_template"] = None

    return render(request, "proxy.html", context)


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

    base_url = reverse("restclients_proxy", args=["xx", "xx"])
    base_url = base_url.replace('/xx/xx', '')

    formatted = re.sub(r"\"/(.*?)\"",
                       r'"<a href="%s/%s/\1">/\1</a>"' % (base_url, service),
                       formatted)

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


@login_required
@csrf_protect
@require_admin
def errors(request):
    context = {}
    context["errors"] = []
    problem_str = request.session.get("RESTCLIENTS_ERRORS", None)
    problems = DegradePerformance(serialized=problem_str)

    drop_keys = []
    if request.method == "POST":
        for key in problems.services():
            keepit = "keep_%s" % key
            if keepit not in request.POST:
                problems.remove_service(key)
            else:
                problems.set_status(key,
                                    request.POST.get("%s_status" % key, None))
                problems.set_content(key,
                                     request.POST.get("%s_content" % key,
                                                      None))
                problems.set_load_time(key,
                                       request.POST.get("%s_load_time" % key,
                                                        None))

        new_service = request.POST.get("new_service_name", None)
        if new_service:
            key = request.POST["new_service_name"]
            problems.set_status(key,
                                request.POST.get("new_service_status", None))
            problems.set_content(key,
                                 request.POST.get("new_service_content", None))
            problems.set_load_time(key,
                                   request.POST.get("new_service_load_time",
                                                    None))

        request.session["RESTCLIENTS_ERRORS"] = problems.serialize()

    for service in problems.services():
        context["errors"].append({
            "name": service,
            "status": problems.get_status(service),
            "content": problems.get_content(service),
            "load_time": problems.get_load_time(service),
        })

    set_wrapper_template(context)

    return render(request, "restclients/cause_errors.html", context)
