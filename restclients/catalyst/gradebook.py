"""
Interface for interacting with Catalyst GradeBook
"""

from restclients.sws import encode_section_label
from restclients.models.catalyst import GradebookParticipant
from restclients.catalyst import get_resource
from restclients.exceptions import InvalidGradebookID
import re


def get_participants_for_gradebook(gradebook_id, person=None):
    """
    Returns a list of gradebook participants for the passed gradebook_id and
    person.
    """
    if not valid_gradebook_id(gradebook_id):
        raise InvalidGradebookID(regid)

    url = "/rest/gradebook/v1/book/%s/participants" % gradebook_id
    headers = {}

    if person is not None:
        headers["X-UW-Act-as"] = person.uwnetid

    data = get_resource(url, headers)

    participants = []
    for pt in data["participants"]:
        participants.append(_participant_from_json(pt))

    return participants


def get_participants_for_section(section, person=None):
    """
    Returns a list of gradebook participants for the passed section and person.
    """
    section_label = encode_section_label(section.section_label())
    url = "/rest/gradebook/v1/section/%s/participants" % section_label
    headers = {}

    if person is not None:
        headers["X-UW-Act-as"] = person.uwnetid

    data = get_resource(url, headers)

    participants = []
    for pt in data["participants"]:
        participants.append(_participant_from_json(pt))

    return participants


def valid_gradebook_id(gradebook_id):
    return True if re.match(r"^[1-9][0-9]{,9}$", str(gradebook_id)) else False


def _participant_from_json(data):
    participant = GradebookParticipant()
    participant.participant_id = data["participant_id"]
    participant.class_grade = data["class_grade"]
    participant.notes = data["notes"]
    participant.person_id = data["person_id"]
    return participant
