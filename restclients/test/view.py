# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from restclients.views import clean_self_closing_divs
from restclients.views import proxy
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from userservice.user import UserServiceMiddleware
from django.contrib.auth.models import User
import os


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
