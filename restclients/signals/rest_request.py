try:
    from status_app.dispatch import dispatch
    from status_app.models import RawEvent
except Exception as ex:
    pass
from django.utils import timezone
import django.dispatch


rest_request = django.dispatch.Signal(providing_args=['url', 'request_time', 'hostname', 'service_name'])


def rest_request_receiver(sender, **kwargs):
    url = kwargs.get('url', None)
    request_time = kwargs.get('request_time', None)
    service_name = kwargs.get('service_name', None)
    hostname = kwargs.get('hostname', None)
    dispatch('%s_request_interval' % service_name, RawEvent.INTERVAL, timezone.now(), request_time, url, hostname)

def get_signal():
    return rest_request
