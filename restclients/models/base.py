from restclients_core.models import Model as RCModel
from django.db.models import Model as DJModel


class RestClientsModel(RCModel):
    """Base class containing Meta attributes common to all models."""
    class Meta:
        abstract = True
        app_label = 'restclients'

class RestClientsDjangoModel(DJModel):
    """Base class containing Meta attributes common to all models."""
    def __init__(self, *args, **kwargs):
        super(RestClientsDjangoModel, self).__init__(*args, **kwargs)
    class Meta:
        abstract = True
        app_label = 'restclients'
