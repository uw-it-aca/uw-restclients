from django.db import models


class RestClientsModel(models.Model):
    """Base class containing Meta attributes common to all models."""
    class Meta:
        abstract = True
        app_label = 'restclients'
