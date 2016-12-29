from django.test import TestCase
from django.conf import settings
from restclients.thread import Thread, GenericPrefetchThread
from restclients.dao import PerformanceDegradation

class ThreadsTest(TestCase):
    def test_defaults(self):
        with self.settings(DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3' } }):
            thread = Thread()
            self.assertEquals(thread._use_thread, False)

    def test_force_threading(self):
        with self.settings(
                DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3' } },
                RESTCLIENTS_USE_THREADING=True):
            thread = Thread()
            self.assertEquals(thread._use_thread, True)

    def test_mysql_defaults(self):
        with self.settings(DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql' } }):
            thread = Thread()
            self.assertEquals(thread._use_thread, True)

    def test_force_mysql_disable_threading(self):
        with self.settings(
                DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql' } },
                RESTCLIENTS_DISABLE_THREADING=True):
            thread = Thread()
            self.assertEquals(thread._use_thread, False)

    def test_bad_dupe_config(self):
        with self.settings(
                DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql' } },
                RESTCLIENTS_DISABLE_THREADING=True,
                RESTCLIENTS_USE_THREADING=True):

            thread = Thread()
            self.assertEquals(thread._use_thread, False)

    def test_performance_degradation(self):
        with self.settings(RESTCLIENTS_USE_THREADING=True):
            PerformanceDegradation.set_problems("fake data")

            def test_method():
                from threading import currentThread
                currentThread().method = PerformanceDegradation.get_problems()

            thread = GenericPrefetchThread()
            thread.method = test_method

            thread.start()
            thread.join()

            self.assertEquals(thread.method, "fake data")

            def test_method():
                from threading import currentThread
                current = currentThread()
                test = current not in PerformanceDegradation._problem_data
                current.method = test

            thread = GenericPrefetchThread()
            thread.method = test_method

            thread.start()
            thread.join()

            self.assertEquals(thread.method, True)
            PerformanceDegradation.clear_problems()
