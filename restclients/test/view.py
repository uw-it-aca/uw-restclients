# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from restclients.views import clean_self_closing_divs
from restclients.views import proxy
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from userservice.user import UserServiceMiddleware
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from unittest2 import skipIf
import os


def missing_url(name, *args, **kwargs):
    try:
        url = reverse(name, *args, **kwargs)
    except Exception as ex:
        print "Ex: ", ex
        if getattr(settings, "RESTCLIENTS_REQUIRE_VIEW_TESTS", False):
            raise
        return True

    return False


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as ex:
        user = User.objects.create_user(username, password='pass')
        return user


def get_user_pass(username):
    return 'pass'


class ViewTest(TestCase):
    def test_simple(self):
        self_closed = "<div/>"
        valid = "<!-- <div/> --><div></div>"

        self.assertEquals(valid, clean_self_closing_divs(self_closed))

    def test_2_simple(self):
        self_closed = "<div/><div/>"
        valid = "<!-- <div/> --><div></div><!-- <div/> --><div></div>"

        self.assertEquals(valid, clean_self_closing_divs(self_closed))

    def test_valid_div(self):
        valid = "<div id='test id'></div>"
        self.assertEquals(valid, clean_self_closing_divs(valid))

    def test_div_then_valid_self_closing(self):
        valid = "<div id='test id'></div><br/>"
        self.assertEquals(valid, clean_self_closing_divs(valid))

    def test_bad_url(self):
        # Something was sending urls that should have been
        # ...=&reg_id=... into ...=®_id=A
        # That should be fixed, but in the mean time we shouldn't crash
        request = RequestFactory().get("/", { "i": "u\xae_id=A" })
        SessionMiddleware().process_request(request)
        AuthenticationMiddleware().process_request(request)
        UserServiceMiddleware().process_request(request)

        request.user = User.objects.create_user(username='tbu_user',
                                                email='fake@fake',
                                                password='top_secret')

        backend = "authz_group.authz_implementation.all_ok.AllOK"
        with self.settings(RESTCLIENTS_ADMIN_GROUP="ok",
                           AUTHZ_GROUP_BACKEND=backend):
            res = proxy(request, "sws", "/fake/")
            self.assertEquals(res.content,
                              "Bad URL param given to the restclients browser")
            self.assertEquals(res.status_code, 200)

    @skipIf(missing_url("restclients_proxy", args=["test", "/ok"]), "restclients urls not configured")
    def test_support_links(self):
        url = reverse("restclients_proxy", args=["pws", "/identity/v1/person.json?student_number=1234567"])
        get_user('test_view')
        self.client.login(username='test_view',
                          password=get_user_pass('test_view'))

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
