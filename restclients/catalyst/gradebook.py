"""
Interface for interacting with Catalyst GradeBook
"""

from restclients.sws import encode_section_label
from restclients.exceptions import DataFailureException
from restclients.models.catalyst import GradebookParticipant
from restclients.dao import Catalyst_DAO
import json


def get_participants_for_section(section, person=None):
    """
    Returns a list of gradebook participants for the passed section and person.
    """
    section_label = encode_section_label(section.section_label())
    url = "/rest/gradebook/v1/section/%s/participants" % section_label

    headers = { "Accept": "application/json" }
    if person is not None:
        headers["X-UW-Act-as"] = person.uwnetid

    response = Catalyst_DAO().getURL(url, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    try:
        data = json.loads(response.data)
    except ValueError as ex:
        raise DataFailureException(url, response.status, response.data)

    participants = []
    for pt in data["participants"]:
        participant = GradebookParticipant()
        participant.participant_id = pt["participant_id"]
        participant.class_grade = pt["class_grade"]
        participant.notes = pt["notes"]
        participant.person_id = pt["person_id"]

        participants.append(participant)

    return participants
