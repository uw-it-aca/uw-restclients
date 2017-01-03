from django.conf import settings

OLD_DEFAULT_TIMEOUT = 15


def get_timeout(service):
    """ Returns either a custom timeout for the given service, or a default
    """
    custom_timeout_key = "RESTCLIENTS_%s_TIMEOUT" % service.upper()
    if hasattr(settings, custom_timeout_key):
        return getattr(settings, custom_timeout_key)

    default_key = "RESTCLIENTS_DEFAULT_TIMEOUT"
    if hasattr(settings, default_key):
        return getattr(settings, default_key)

    return OLD_DEFAULT_TIMEOUT
