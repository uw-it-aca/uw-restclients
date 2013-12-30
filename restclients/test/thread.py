from django.test import TestCase
from django.conf import settings
from restclients.thread import Thread

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

