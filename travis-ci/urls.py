from django.conf.urls import include, url

urlpatterns = [
    url(r'^rc/', include('restclients.urls')),
]
