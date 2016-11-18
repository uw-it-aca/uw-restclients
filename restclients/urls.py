from django.conf.urls import include, url
from restclients.views import proxy

urlpatterns = [
    url(r'view/(\w+)/(.*)$',
        proxy,
        name="restclients_proxy"),
]
