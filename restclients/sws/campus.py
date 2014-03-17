"""
Interfacing with the Student Web Service, Campus Search.
"""
import logging
from restclients.sws import get_resource
from restclients.models.sws import Campus

logger = logging.getLogger(__name__)
campus_search_url = "/student/v4/campus.json"

def get_all_campuses():
    """
    Returns a list of restclients.Campus models, representing all
    campuses.
    """
    return _json_to_campuses(get_resource(campus_search_url))

def _json_to_campuses(data):
    campuses = []
    for campus_data in data.get("Campuses", []):
        campus = Campus()
        campus.label = campus_data["CampusShortName"]
        campus.name = campus_data["CampusName"]
        campus.full_name = campus_data["CampusFullName"]
        campus.clean_fields()
        campuses.append(campus)

    return campuses
