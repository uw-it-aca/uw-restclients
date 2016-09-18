import json
from datetime import datetime
from django.db import models


class BridgeCustomField(models.Model):
    REGID_FIELD_ID = "5"
    REGID_NAME = "REGID"

    value_id = models.CharField(max_length=10, null=True, default=None)
    field_id = models.CharField(max_length=10)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def is_regid(self):
        return self.field_id == BridgeCustomField.REGID_FIELD_ID and\
            self.name == BridgeCustomField.REGID_NAME

    def __str__(self):
        return "{%s: %s, %s: %s, %s: %s, %s: %s}" % (
            'value_id', self.value_id,
            'id', self.field_id,
            'name', self.name,
            'value', self.value
            )

    def to_json(self):
        value = {"custom_field_id": self.field_id,
                 "value": self.value
                 }
        if self.value_id is not None:
            value["id"] = self.value_id
        return value

    class Meta:
        db_table = "restclients_bridge_custom_field"


class BridgeUser(models.Model):
    bridge_id = models.IntegerField()
    uwnetid = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    full_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    sortable_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    avatar_url = models.CharField(max_length=512, null=True, default=None)
    locale = models.CharField(max_length=2)
    logged_in_at = models.DateTimeField(null=True, default=None)
    updated_at = models.DateTimeField()
    unsubscribed = models.CharField(max_length=128, null=True, default=None)
    next_due_date = models.DateTimeField(null=True, default=None)
    completed_courses_count = models.IntegerField()

    def get_uid(self):
        return "%s@uw.edu" % self.uwnetid

    def to_json_post(self):
        custom_fields_json = []
        for field in self.custom_fields:
            custom_fields_json.append(field.to_json())

        return {"users": [
                {"uid": self.get_uid(),
                 "first_name": self.first_name,
                 "last_name": self.last_name,
                 "full_name": self.full_name,
                 "email": self.email,
                 "custom_fields": custom_fields_json
                 }]
                }

    def to_json(self):
        custom_fields_json = []
        for field in self.custom_fields:
            custom_fields_json.append(field.to_json())

        roles_json = []
        for role in self.roles:
            roles_json.append(role.to_json())

        return {"users": [
                {"uid": self.get_uid(),
                 "first_name": self.first_name,
                 "last_name": self.last_name,
                 "full_name": self.full_name,
                 "email": self.email,
                 "custom_fields": custom_fields_json,
                 "roles": roles_json
                 }]
                }

    def __str__(self):
        return ("{%s: %s, %s: %s, %s: %s, %s: %s, %s: %s, %s: %s," +
                " %s: %s, %s: %s, %s: %s, %s: %s, %s: %d}") % (
                "id", self.bridge_id if self.bridge_id else None,
                "uwnetid", self.uwnetid,
                "first_name", self.first_name,
                "last_name", self.last_name,
                "full_name", self.full_name,
                "sortable_name", self.sortable_name,
                "name", self.name,
                "email", self.email,
                "updated_at", self.updated_at,
                "logged_in_at", self.logged_in_at,
                "completed_courses_count", self.completed_courses_count)

    def __init__(self):
        self.roles = []
        self.custom_fields = []

    class Meta:
        db_table = "restclients_bridge_user"


class BridgeUserRole(models.Model):
    role_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)

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
