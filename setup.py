#!/usr/bin/env python

from distutils.core import setup

setup(name='RestClients',
      version='1.0',
      description='UW RestClients',
      install_requires=['Django==1.4', 'lxml==2.3.5', 'urllib3>=1.4', 'twilio==3.4.1'],
     )
