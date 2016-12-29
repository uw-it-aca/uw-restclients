from datetime import datetime
import json
import logging
import re
from dateutil.parser import parse
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
    if bridge_id:
        url = url + ("/%d" % bridge_id)
    return url


def admin_uid_url(uwnetid):
    url = ADMIN_URL_PREFIX
    if uwnetid is not None:
        url = url + '/uid%3A' + uwnetid + '%40uw%2Eedu'
    return url


def author_id_url(bridge_id):
    url = AUTHOR_URL_PREFIX
    if bridge_id:
        url = url + ("/%d" % bridge_id)
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


def get_user(uwnetid, include_course_summary=True):
    """
    Return a list of BridgeUsers objects with custom fields
    """
    url = author_uid_url(uwnetid) + "?%s" % CUSTOM_FIELD
    if include_course_summary:
        url = "%s&%s" % (url, COURSE_SUMMARY)
    resp = get_resource(url)
    return _process_json_resp_data(resp)


def get_user_by_id(bridge_id, include_course_summary=True):
    """
    Return a list of BridgeUsers objects with custom fields
    """
    url = author_id_url(bridge_id) + "?%s" % CUSTOM_FIELD
    if include_course_summary:
        url = "%s&%s" % (url, COURSE_SUMMARY)
    resp = get_resource(url)
    return _process_json_resp_data(resp)


def get_all_users(include_course_summary=True):
    """
    Return a list of BridgeUser objects with custom fields.
    """
    url = author_uid_url(None) + "?%s" % CUSTOM_FIELD

    if include_course_summary:
        url = "%s&%s" % (url, COURSE_SUMMARY)

    url = "%s&%s" % (url, PAGE_MAX_ENTRY)

    resp = get_resource(url)

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
    Update only the user attributes provided.
    Return a list of BridgeUsers objects with custom fields.
    """
    if bridge_user.bridge_id:
        url = author_id_url(bridge_user.bridge_id)
    else:
        url = author_uid_url(bridge_user.uwnetid)
    resp = patch_resource(url + ("?%s" % CUSTOM_FIELD),
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

        user = BridgeUser(
            bridge_id=int(user_data["id"]),
            netid=re.sub('@uw.edu', '', user_data["uid"]),
            full_name=user_data.get("full_name", ""),
            email=user_data.get("email", ""),
            locale=user_data.get("locale", "en"),
            completed_courses_count=user_data.get("completed_courses_count",
                                                  -1)
            )

        if "name" in user_data:
            user.name = user_data["name"]

        if "first_name" in user_data:
            user.first_name = user_data["first_name"]

        if "last_name" in user_data:
            user.last_name = user_data["last_name"]

        if "sortable_name" in user_data:
            user.sortable_name = user_data["sortable_name"]

        if "avatar_url" in user_data:
            user.avatar_url = user_data["avatar_url"]

        if "loggedInAt" in user_data and user_data["loggedInAt"] is not None:
            user.logged_in_at = parse(user_data["loggedInAt"])

        if "updated_at" in user_data and user_data["updated_at"] is not None:
            user.updated_at = parse(user_data["updated_at"])

        if "unsubscribed" in user_data:
            user.unsubscribed = user_data["unsubscribed"]

        if "next_due_date" in user_data and\
                user_data["next_due_date"] is not None:
            user.next_due_date = parse(user_data["next_due_date"])

        if not no_custom_fields and\
                "links" in user_data and len(user_data["links"]) > 0 and\
                "custom_field_values" in user_data["links"]:
            values = user_data["links"]["custom_field_values"]
            for custom_field_value in values:
                if custom_field_value in custom_fields_value_dict:
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
        custom_field = BridgeCustomField(
            value_id=value["id"],
            value=value["value"],
            field_id=value["links"]["custom_field"]["id"]
            )
        custom_field.name = custom_fields_name_dict[custom_field.field_id]
        custom_fields_value_dict[custom_field.value_id] = custom_field

    return custom_fields_value_dict


def get_regid_from_custom_fields(custom_fields):
    if custom_fields is not None and\
            len(custom_fields) > 0:
        for custom_field in custom_fields:
            if custom_field.is_regid():
                return custom_field.value
    return None


def _get_roles_from_json(role_data):
    # roles in data is a list of strings currently.
    return BridgeUserRole(role_id=role_data,
                          name=role_data)
