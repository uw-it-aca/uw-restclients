from status_app.dispatch import dispatch
from status_app.models import RawEvent
from django.utils import timezone
import django.dispatch


rest_request = django.dispatch.Signal(providing_args=['url', 'request_time', 'hostname', 'sender'])


def rest_request_receiver(sender, **kwargs):
    url = kwargs.get('url', None)
    request_time = kwargs.get('request_time', None)
    service = kwargs.get('sender', None)
    hostname = kwargs.get('hostname', None)
    dispatch('%s_request_interval' % sender, RawEvent.INTERVAL, timezone.now(), request_time, url, hostname)

def get_signal():
    return rest_request