import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'restclients/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/uw-restclients"
setup(
    name='UW-RestClients',
    version=VERSION,
    packages=['restclients'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=['Django',
                      'lxml==3.7.1',
                      'urllib3==1.10.2',
                      'twilio==3.4.1',
                      'boto',
                      'simplejson>=2.1',
                      'djangorestframework>=2.0',
                      'jsonpickle>=0.4.0',
                      'ordereddict>=1.1',
                      'python-dateutil>=2.1',
                      'unittest2>=0.5.1',
                      'mock',
                      'pytz',
                      'pytimeparse',
                      'icalendar',
                      'AuthZ-Group>=1.1.4',
                      'Django-UserService',
                      'python-binary-memcached',
                      'UW-RestClients-Core>=0.8.2,<1.0',
                      'UW-RestClients-SWS>=0.5.1,<1.0',
                      'UW-RestClients-PWS>=0.5,<1.0',
                      'UW-RestClients-HFS>=0.5,<1.0',
                      'UW-RestClients-NWS>=0.5,<1.0',
                      ],
    license='Apache License, Version 2.0',
    description=('Clients for a variety of RESTful web services '
                 'at the University of Washington'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

