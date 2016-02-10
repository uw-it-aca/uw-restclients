#!/usr/bin/env python

# Taken from django's setup.py:

import os

from distutils.core import setup
import setuptools

setup(name='UW-RestClients',
      version='1.0.5',
      license = "Apache 2.0",
      author = "UW-IT ACA",
      author_email = "pmichaud@uw.edu",
      packages=setuptools.find_packages(exclude=["project"]),
      include_package_data=True,  # use MANIFEST.in during install
      url='https://github.com/uw-it-aca/uw-restclients',
      description='Clients for a variety of RESTful web services at the University of Washington',
      install_requires=['Django<1.8', 'lxml==2.3.5', 'urllib3==1.10.2', 'twilio==3.4.1', 'boto', 'simplejson>=2.1', 'djangorestframework>=2.0', 'jsonpickle>=0.4.0', 'ordereddict>=1.1', 'python-dateutil>=2.1', 'unittest2>=0.5.1', 'pytz', 'icalendar', 'AuthZ-Group>=1.1.4', 'Django-UserService', 'python-binary-memcached',],
     )
