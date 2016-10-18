import os

version = os.environ.get("DJANGO_VERSION", "1.6")

major, minor = version.split(".")

if major == 1 and minor < 10:
    from django.conf.urls import patterns, include, url
    from django.contrib import admin
    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'project.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),
    #    url(r'^', include('userservice.urls')),
    )
else:
    urlpatterns = []
