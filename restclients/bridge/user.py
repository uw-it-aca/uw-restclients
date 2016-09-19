from datetime import datetime
import logging
import re
from django.utils.dateparse import parse_datetime
import simplejson as json
from restclients.exceptions import InvalidNetID
from restclients.pws import PWS
from restclients.models.bridge import BridgeUser, BridgeUserRole,\
    BridgeCustomField
from restclients.bridge import get_resource, patch_resource, post_resource,\
    delete_resource


logger = logging.getLogger(__name__)
ADMIN_URL_PREFIX = "/api/admin/users"
AUTHOR_URL_PREFIX = "/api/author/users"
CUSTOM_FIELD = "includes%5B%5D=custom_fields"
COURSE_SUMMARY = "includes%5B%5D=course_summary"
PAGE_MAX_ENTRY = "limit=1000"
RESTORE_SUFFIX = "/restore"


def admin_id_url(bridge_id):
    url = ADMIN_URL_PREFIX
    if bridge_id is not None:
        url = url + '/' + bridge_id
    return url


def admin_uid_url(uwnetid):
    url = ADMIN_URL_PREFIX
    if uwnetid is not None:
        url = url + '/uid%3A' + uwnetid + '%40uw%2Eedu'
    return url


def author_id_url(bridge_id):
    url = AUTHOR_URL_PREFIX
    if bridge_id is not None:
        url = url + '/' + bridge_id
    return url


def author_uid_url(uwnetid):
    url = AUTHOR_URL_PREFIX
    if uwnetid is not None:
        url = url + '/uid%3A' + uwnetid + '%40uw%2Eedu'
    return url


def add_user(bridge_user):
    """
    Add the bridge_user given
    Return a list of BridgeUser objects with custom fields
    """
    resp = post_resource(admin_uid_url(None) +
                         ("?%s" % CUSTOM_FIELD),
                         json.dumps(bridge_user.to_json_post(),
                                    separators=(',', ':')))
    return _process_json_resp_data(resp)


def change_uid(bridge_id, new_uwnetid):
    """
    Return a list of BridgeUser objects without custom fields
    """
    resp = patch_resource(author_id_url(bridge_id),
                          '{"user":{"uid":"%s@uw.edu"}}' % new_uwnetid)
    return _process_json_resp_data(resp, no_custom_fields=True)


def replace_uid(old_uwnetid, new_uwnetid):
    """
    Return a list of BridgeUser objects without custom fields
    """
    resp = patch_resource(author_uid_url(old_uwnetid),
                          '{"user":{"uid":"%s@uw.edu"}}' % new_uwnetid)
    return _process_json_resp_data(resp, no_custom_fields=True)


def delete_user(uwnetid):
    """
    Return True when the HTTP repsonse status is 204 -
    the user is deleted successfully
    """
    resp = delete_resource(admin_uid_url(uwnetid))
    return resp.status == 204


def delete_user_by_id(bridge_id):
    """
    Return True when the HTTP repsonse status is 204 -
    the user is deleted successfully
    """
    resp = delete_resource(admin_id_url(bridge_id))
    return resp.status == 204


def get_user(uwnetid, include_course_summary=False):
    """
    Return a list of BridgeUsers objects with custom fields
    """
    resp = get_resource(author_uid_url(uwnetid) +
                        "?%s&%s" % (CUSTOM_FIELD, COURSE_SUMMARY))
    return _process_json_resp_data(resp)


def get_all_users(include_course_summary=False):
    """
    Return a list of BridgeUser objects with custom fields
    """
    resp = get_resource(
        author_uid_url(None) +
        "?%s&%s&%s" % (CUSTOM_FIELD, COURSE_SUMMARY, PAGE_MAX_ENTRY))
    return _process_json_resp_data(resp)


def restore_user(uwnetid):
    """
    Return a list of BridgeUsers objects without custom fields
    """
    resp = post_resource(author_uid_url(uwnetid) + RESTORE_SUFFIX,
                         '{}')
    return _process_json_resp_data(resp, no_custom_fields=True)


def restore_user_by_id(bridge_id):
    """
    Return a list of BridgeUsers objects without custom fields
    """
    resp = post_resource(author_id_url(bridge_id) + RESTORE_SUFFIX,
                         '{}')
    return _process_json_resp_data(resp, no_custom_fields=True)


def update_user(bridge_user):
    """
    Return a list of BridgeUsers objects with custom fields
    """
    resp = patch_resource(author_uid_url(bridge_user.uwnetid) +
                          ("?%s" % CUSTOM_FIELD),
                          json.dumps(bridge_user.to_json_post(),
                                     separators=(',', ':')))
    return _process_json_resp_data(resp)


def update_user_by_id(bridge_user):
    """
    Return a list of BridgeUsers objects with custom fields
    """
    resp = patch_resource(author_id_url(bridge_user.bridge_id) +
                          ("?%s" % CUSTOM_FIELD),
                          json.dumps(bridge_user.to_json_post(),
                                     separators=(',', ':')))
    return _process_json_resp_data(resp)


def _process_json_resp_data(resp, no_custom_fields=False):
    """
    process the response and return a list of BridgeUser
    """
    bridge_users = []
    while True:
        resp_data = json.loads(resp)
        link_url = None
        if "meta" in resp_data and\
                "next" in resp_data["meta"]:
            link_url = resp_data["meta"]["next"]

        bridge_users = _process_apage(resp_data, bridge_users,
                                      no_custom_fields)

        if link_url is None:
            break
        resp = get_resource(link_url)

    return bridge_users


def _process_apage(resp_data, bridge_users, no_custom_fields):
    if "linked" not in resp_data:
        logger.error("Invalid response body (missing 'linked') %s", resp_data)
        return bridge_users

    if not no_custom_fields:
        if "custom_fields" not in resp_data["linked"] or\
                "custom_field_values" not in resp_data["linked"]:
            logger.error(
                "Invalid response body (missing 'custom_fields') %s",
                resp_data)
            return bridge_users

        custom_fields_value_dict = _get_custom_fields_dict(resp_data["linked"])
        # a dict of {custom_field_value_id: BridgeCustomField}

    if "users" not in resp_data:
        logger.error("Invalid response body (missing 'users') %s", resp_data)
        return bridge_users

    for user_data in resp_data["users"]:
        if "deleted_at" in user_data and\
                user_data["deleted_at"] is not None:
            # skip deleted entry
            continue

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

        if "loggedInAt" in user_data:
            user.logged_in_at = user_data["loggedInAt"]
            if user_data["loggedInAt"] is not None:
                user.logged_in_at = parse_datetime(user_data["loggedInAt"])

        if "updated_at" in user_data:
            user.updated_at = user_data["updated_at"]
            if user_data["updated_at"] is not None:
                user.updated_at = parse_datetime(user_data["updated_at"])

        if "unsubscribed" in user_data:
            user.unsubscribed = user_data["unsubscribed"]

        if "next_due_date" in user_data:
            user.next_due_date = user_data["next_due_date"]
            if user_data["next_due_date"] is not None:
                user.next_due_date = parse_datetime(user_data["next_due_date"])

        if "completed_courses_count" in user_data:
            user.completed_courses_count = user_data["completed_courses_count"]

        if "links" in user_data and len(user_data["links"]) > 0 and\
                "custom_field_values" in user_data["links"]:
            values = user_data["links"]["custom_field_values"]
            for custom_field_value in values:
                user.custom_fields.append(
                    custom_fields_value_dict[custom_field_value])

        if "roles" in user_data and len(user_data["roles"]) > 0:
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
