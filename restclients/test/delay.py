from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from userservice.user import UserServiceMiddleware
from django.contrib.auth.models import User
from restclients.test.view import missing_url
from restclients.views import errors
from restclients.dao import SWS_DAO
from restclients.middleware import EnableServiceDegradationMiddleware
import time


class DegradedTestCase(TestCase):
    def test_degraded(self):
        r1  = RequestFactory().post(reverse("restclients_errors"),
                                    { "new_service_name": "sws",
                                      "new_service_status": 500,
                                      "new_service_content": "[oops",
                                      "new_service_load_time": 0.1, })
        r2  = RequestFactory().get("/")

        SessionMiddleware().process_request(r1)
        SessionMiddleware().process_request(r2)

        AuthenticationMiddleware().process_request(r1)
        UserServiceMiddleware().process_request(r1)

        AuthenticationMiddleware().process_request(r2)
        UserServiceMiddleware().process_request(r2)

        user = User.objects.create_user(username='delay_user',
                                        email='fake2@fake',
                                        password='top_secret')

        r1.user = user
        r2.user = user

        r1._dont_enforce_csrf_checks = True

        errors(r1)

        r1.session.save()

        EnableServiceDegradationMiddleware().process_request(r1)

        sws = SWS_DAO()
        t1 = time.time()
        sws_response = sws.getURL("/student/v5/term/current.json", {})
        t2 = time.time()
        self.assertEquals(sws_response.status, 500)
        self.assertEquals(sws_response.data, "[oops")

        self.assertGreater(t2-t1, 0.09)

        EnableServiceDegradationMiddleware().process_request(r2)

        sws_response = sws.getURL("/student/v5/term/current.json", {})
        self.assertEquals(sws_response.status, 200)



