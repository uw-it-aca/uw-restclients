try:
    from status_app.dispatch import dispatch
    from status_app.models import RawEvent
except Exception as ex:
    pass
from django.utils import timezone
import django.dispatch


rest_request_passfail = django.dispatch.Signal(providing_args=['url', 'success', 'hostname', 'service_name'])


def rest_request_passfail_receiver(sender, **kwargs):
    url = kwargs.get('url', None)
    success = kwargs.get('success', False)
    service_name = kwargs.get('service_name', None)
    hostname = kwargs.get('hostname', None)
    dispatch('%s_request_passfail' % service_name, RawEvent.PASS_FAIL, timezone.now(), success, url, hostname)

def get_signal():
    return rest_request_passfail
