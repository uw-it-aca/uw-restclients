from django.conf.urls import include, url
from restclients.views import proxy, errors

urlpatterns = [
    url(r'errors', errors, name="restclients_errors"),
    url(r'view/(\w+)/(.*)$',
        proxy,
        name="restclients_proxy"),
]
