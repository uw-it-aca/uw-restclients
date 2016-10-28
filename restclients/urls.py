from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'view/(\w+)/(.*)$',
        'restclients.views.proxy',
        name="restclients_proxy"),
    )
