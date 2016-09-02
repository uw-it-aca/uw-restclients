import json
from datetime import datetime
from django.db import models


class BridgeCustomField(models.Model):
    value_id = models.CharField(max_length=10)
    field_id = models.CharField(max_length=10)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return "{%s: %s, %s: %s, %s: %s, %s: %s}" % (
            'value_id', self.value_id,
            'id', self.field_id,
            'name', self.name,
            'value', self.value
            )

    def to_json(self):
        return {
            "custom_field_id": self.field_id,
            "value": self.value
            }

    class Meta:
        db_table = "restclients_bridge_custom_field"


class BridgeUser(models.Model):
    bridge_id = models.IntegerField()
    uwnetid = models.CharField(max_length=100)
    hris_id = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    sortable_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=500, null=True)
    locale = models.CharField(max_length=2, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    unsubscribed = models.CharField(max_length=100, null=True)

    def get_uid(self):
        return "%s@uw.edu" % self.uwnetid

    def to_json_post(self):
        custom_fields_json = []
        for field in self.custom_fields:
            custom_fields_json.append(field.to_json())

        roles_json = []
        for role in self.roles:
            roles_json.append(role.to_json())

        return {"uid": self.get_uid(),
                "first_name": self.first_name,
                "last_name": self.last_name,
                "full_name": self.full_name,
                "email": self.email,
                "custom_fields": custom_fields_json,
                "roles": roles_json
                }

    def __str__(self):
        return ("{%s: %s, %s: %s, %s: %s, %s: %s, %s: %s," +
                " %s: %s, %s: %s, %s: %s, %s: %s, %s: %s}") % (
            "id", self.bridge_id,
            "uwnetid", self.uwnetid,
            "first_name", self.first_name,
            "last_name", self.last_name,
            "full_name", self.full_name,
            "sortable_name", self.sortable_name,
            "name", self.name,
            "updated_at", self.updated_at,
            "deleted_at", '',
            # self.deleted_at,
            # 'BridgeUser' object has no attribute 'deleted_at'
            "email", self.email)

    def __init__(self):
        self.roles = []
        self.custom_fields = []

    class Meta:
        db_table = "restclients_bridge_user"


class BridgeUserRole(models.Model):
    role_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)

    def __init__(self):
        self.permissions = []

    def to_json(self):
        return {
            'id': self.role_id,
            'name': self.name,
            'permissions': self.permissions  # unknown
            }

    class Meta:
        db_table = "restclients_bridge_user_role"
