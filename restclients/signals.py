import django.dispatch

rest_request = django.dispatch.Signal(providing_args=['url','request_time', 'hostname'])