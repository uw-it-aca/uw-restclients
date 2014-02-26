try:
    from status_app.dispatch import dispatch
    from status_app.models import RawEvent
except Exception as ex:
    pass
from django.utils import timezone
import django.dispatch


rest_request_passfail = django.dispatch.Signal(providing_args=['url', 'success', 'hostname'])


def rest_request_passfail_receiver(sender, **kwargs):
    url = kwargs.get('url', None)
    success = kwargs.get('success', False)
    hostname = kwargs.get('hostname', None)
    dispatch('%s_request_passfail' % sender, RawEvent.PASS_FAIL, timezone.now(), success, url, hostname)

def get_signal():
    return rest_request_passfail
