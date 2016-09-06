from datetime import datetime
import logging
import re
from django.utils.dateparse import parse_datetime
import simplejson as json
from restclients.exceptions import InvalidNetID
from restclients.pws import PWS
from restclients.models.bridge import BridgeUser, BridgeUserRole,\
    BridgeCustomField
from restclients.bridge import get_resource


logger = logging.getLogger(__name__)
ADMIN_URL_PREFIX = "/api/admin/users"
AUTHOR_URL_PREFIX = "/api/author/users"


def admin_users_url(uwnetid):
    return "%s/uid%s%s%s" % (ADMIN_URL_PREFIX, '%3A', uwnetid, '%40uw.edu')


def author_users_url(uwnetid, suffix):
    return "%s%s?%s" % (
        AUTHOR_URL_PREFIX,
        '/uid%3A' + uwnetid + '%40uw.edu' if uwnetid is not None else '',
        suffix)


def add_auser(bridge_user):
    return post_resource(ADMIN_URL_PREFIX,
                         json.dumps(bridge_user.to_json()))


def delete_user(uwnetid):
    return delete_resource(admin_users_url(uwnetid))


def change_uid(old_uwnetid, new_uwnetid):
    """
    Return a BridgeUsers object
    """
    return post_resource(author_users_url(old_uwnetid),
                         '{"user":{"uid":"%s@uw.edu"}}' % new_uwnetid)


def get_user(uwnetid):
    """
    Return a BridgeUsers object
    """
    resp = get_resource(
        author_users_url(uwnetid, "includes=custom_fields"))
    return process_json_get_users(resp)


def get_all_users():
    """
    Return a list of BridgeUser objects
    """
    resp = get_resource(
        author_users_url(None, "includes=custom_fields&limit=1000"))
    return process_json_get_users(resp)


def restore_auser(bridge_user):
    return post_resource(author_users_url(uwnetid) + "/restore")


def update_auser(bridge_user):
    return put_resource(author_users_url(uwnetid),
                        json.dumps(bridge_user.to_json()))


def process_json_get_users(resp):
    bridge_users = []
    while True:
        resp_data = json.loads(resp)
        link_url = None
        if "meta" in resp_data and\
                "next" in resp_data["meta"]:
            link_url = resp_data["meta"]["next"]

        bridge_users = _process_apage_of_users(resp_data, bridge_users)

        if link_url is None:
            break
        resp = get_resource(link_url)

    return bridge_users


def _process_apage_of_users(resp_data, bridge_users):
    if "linked" not in resp_data:
        logger.error("Invalid response body (missing 'linked') %s", resp_data)
        return bridge_users

    if "custom_fields" not in resp_data["linked"] or\
            "custom_field_values" not in resp_data["linked"]:
        logger.error(
            "Invalid response body (missing 'custom_fields') %s", resp_data)
        return bridge_users

    custom_fields_value_dict = _get_custom_fields_dict(resp_data["linked"])
    # a dict of {custom_field_value_id: BridgeCustomField}

    if "users" not in resp_data:
        logger.error("Invalid response body (missing 'users') %s", resp_data)
        return bridge_users

    for user_data in resp_data["users"]:
        user = BridgeUser()
        user.bridge_id = user_data["id"]
        user.uwnetid = re.sub('@uw.edu', '', user_data["uid"])

        if "name" in user_data:
            user.name = user_data["name"]

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]

        if "last_name" in user_data:
            user.last_name = user_data["last_name"]

        if "full_name" in user_data:
            user.full_name = user_data["full_name"]

        if "sortable_name" in user_data:
            user.sortable_name = user_data["sortable_name"]

        if "email" in user_data:
            user.email = user_data["email"]

        if "locale" in user_data:
            user.locale = user_data["locale"]

        if "avatar_url" in user_data:
            user.avatar_url = user_data["avatar_url"]

        if "deleted_at" in user_data and\
                user_data["deleted_at"] is not None:
            user.deleted_at = parse_datetime(user_data["deleted_at"])

        if "loggedInAt" in user_data and\
                user_data["loggedInAt"] is not None:
            user.logged_in_at = parse_datetime(user_data["loggedInAt"])

        if "updated_at" in user_data and\
                user_data["updated_at"] is not None:
            user.updated_at = parse_datetime(user_data["updated_at"])

        if "unsubscribed" in user_data:
            user.unsubscribed = user_data["unsubscribed"]

        if "links" in user_data and\
                "custom_field_values" in user_data["links"]:
            values = user_data["links"]["custom_field_values"]
            for custom_field_value in values:
                user.custom_fields.append(
                    custom_fields_value_dict[custom_field_value])

        if "roles" in user_data:
            for role_data in user_data["roles"]:
                user.roles.append(_get_roles_from_json(role_data))

        bridge_users.append(user)

    return bridge_users


def _get_custom_fields_dict(linked_data):
    custom_fields_name_dict = {}
    # a dict of {custom_field_id: name}

    for id_name_pair in linked_data["custom_fields"]:
        custom_fields_name_dict[id_name_pair["id"]] = id_name_pair["name"]

    custom_fields_value_dict = {}
    # a dict of {value_id: BridgeCustomField}

    fields_values = linked_data["custom_field_values"]
    for value in fields_values:
        custom_field = BridgeCustomField()
        custom_field.value_id = value["id"]
        custom_field.value = value["value"]
        custom_field.field_id = value["links"]["custom_field"]["id"]
        custom_field.name = custom_fields_name_dict[custom_field.field_id]

        custom_fields_value_dict[custom_field.value_id] = custom_field

    return custom_fields_value_dict


def _get_roles_from_json(role_data):
    # roles in data is a list of strings currently.
    role = BridgeUserRole()
    role.role_id = role_data
    role.name = role_data
    return role
