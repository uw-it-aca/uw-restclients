from restclients.pws import PWS
from restclients.sws import encode_section_label
from restclients.dao import SWS_DAO
from restclients.exceptions import DataFailureException
from restclients.models.sws import GradeRoster, GradeRosterItem
from restclients.models.sws import GradeSubmissionDelegate
from lxml import etree
import re


def get_graderoster(section, instructor):
    """
    Returns a restclients.GradeRoster for the passed Section model and
    instructor Person.
    """
    label = GradeRoster(section=section,
                        instructor=instructor).graderoster_label()
    url = "/student/v4/graderoster/%s" % encode_section_label(label)
    headers = {"Accept": "text/xhtml",
               "X-UW-Act-as": instructor.uwnetid}

    response = SWS_DAO().getURL(url, headers)

    if response.status != 200:
        root = etree.fromstring(response.data)
        msg = root.find(".//*[@class='status_description']").text.strip()
        raise DataFailureException(url, response.status, msg)

    return graderoster_from_xhtml(response.data, section, instructor)


def update_graderoster(graderoster):
    """
    Updates the graderoster resource for the passed restclients.GradeRoster
    model. A new restclients.GradeRoster is returned, representing the
    document returned from the update request.
    """
    label = graderoster.graderoster_label()
    url = "/student/v4/graderoster/%s" % encode_section_label(label)
    headers = {"Content-Type": "application/xhtml+xml",
               "X-UW-Act-as": graderoster.instructor.uwnetid}
    body = graderoster.xhtml()

    response = SWS_DAO().putURL(url, headers, body)

    if response.status != 200:
        root = etree.fromstring(response.data)
        msg = root.find(".//*[@class='status_description']").text.strip()
        raise DataFailureException(url, response.status, msg)

    return graderoster_from_xhtml(response.data, graderoster.section,
                                  graderoster.instructor)


def graderoster_from_xhtml(data, section, instructor):
    pws = PWS()
    people = {instructor.uwregid: instructor}

    graderoster = GradeRoster()
    graderoster.section = section
    graderoster.instructor = instructor
    graderoster.authorized_grade_submitters = []
    graderoster.grade_submission_delegates = []
    graderoster.items = []

    tree = etree.fromstring(data.strip())
    nsmap = {"xhtml": "http://www.w3.org/1999/xhtml"}
    root = tree.xpath(".//xhtml:div[@class='graderoster']",
                      namespaces=nsmap)[0]

    default_section_id = None
    el = root.xpath("./xhtml:div/xhtml:a[@rel='section']/*[@class='section_id']",
                    namespaces=nsmap)[0]
    default_section_id = el.text.upper()

    el = root.xpath("./xhtml:div/*[@class='section_credits']",
                    namespaces=nsmap)[0]
    if el.text is not None:
        graderoster.section_credits = el.text.strip()

    el = root.xpath("./xhtml:div/*[@class='writing_credit_display']",
                    namespaces=nsmap)[0]
    if el.get("checked", "") == "checked":
        graderoster.allows_writing_credit = True

    for el in root.xpath("./xhtml:div//*[@rel='authorized_grade_submitter']",
                         namespaces=nsmap):
        reg_id = el.xpath(".//*[@class='reg_id']")[0].text.strip()
        if reg_id not in people:
            people[reg_id] = pws.get_person_by_regid(reg_id)
        graderoster.authorized_grade_submitters.append(people[reg_id])

    for el in root.xpath("./xhtml:div//*[@class='grade_submission_delegate']",
                         namespaces=nsmap):
        reg_id = el.xpath(".//*[@class='reg_id']")[0].text.strip()
        delegate_level = el.xpath(".//*[@class='delegate_level']")[0].text.strip()
        if reg_id not in people:
            people[reg_id] = pws.get_person_by_regid(reg_id)
        delegate = GradeSubmissionDelegate(person=people[reg_id],
                                           delegate_level=delegate_level)
        graderoster.grade_submission_delegates.append(delegate)

    for item in root.xpath("./*[@class='graderoster_items']/*[@class='graderoster_item']"):
        gr_item = GradeRosterItem(section_id=default_section_id)
        gr_item.grade_choices = []

        for el in item.xpath(".//xhtml:a[@rel='student']/*[@class='reg_id']",
                             namespaces=nsmap):
            gr_item.student_uwregid = el.text.strip()
        
        for el in item.xpath(".//xhtml:a[@rel='student']/*[@class='name']",
                             namespaces=nsmap):
            full_name = el.text.strip()
            try:
                (surname, first_name) = full_name.split(",", 1)
                gr_item.student_first_name = first_name
                gr_item.student_surname = surname
            except ValueError:
                pass

        for el in item.xpath(".//*[@class]"):
            classname = el.get("class")
            if classname == "duplicate_code" and el.text is not None:
                duplicate_code = el.text.strip()
                if len(duplicate_code):
                    gr_item.duplicate_code = duplicate_code
            elif classname == "section_id" and el.text is not None:
                gr_item.section_id = el.text.strip()
            elif classname == "student_former_name" and el.text is not None:
                student_former_name = el.text.strip()
                if len(student_former_name):
                    gr_item.student_former_name = student_former_name
            elif classname == "student_number":
                gr_item.student_number = el.text.strip()
            elif classname == "student_credits" and el.text is not None:
                gr_item.student_credits = el.text.strip()
            elif "date_withdrawn" in classname and el.text is not None:
                gr_item.date_withdrawn = el.text.strip()
            elif classname == "incomplete":
                if el.get("checked", "") == "checked":
                    gr_item.has_incomplete = True
                if el.get("disabled", "") != "disabled":
                    gr_item.allows_incomplete = True
            elif classname == "writing_course":
                if el.get("checked", "") == "checked":
                    gr_item.has_writing_credit = True
            elif classname == "auditor":
                if el.get("checked", "") == "checked":
                    gr_item.is_auditor = True
            elif classname == "no_grade_now":
                if el.get("checked", "") == "checked":
                    gr_item.no_grade_now = True
            elif classname == "grades":
                if el.get("disabled", "") != "disabled":
                    gr_item.allows_grade_change = True
            elif classname == "grade":
                grade = el.text.strip() if el.text is not None else ""
                gr_item.grade_choices.append(grade)
                if el.get("selected", "") == "selected":
                    gr_item.grade = grade
            elif classname == "grade_document_id" and el.text is not None:
                gr_item.grade_document_id = el.text.strip()
            elif "date_graded" in classname and el.text is not None:
                gr_item.date_graded = el.text.strip()
            elif classname == "grade_submitter_source" and el.text is not None:
                gr_item.grade_submitter_source = el.text.strip()
            elif classname == "code" and el.text is not None:
                gr_item.status_code = el.text.strip()
            elif classname == "message" and el.text is not None:
                gr_item.status_message = el.text.strip()

        for el in item.xpath(".//xhtml:a[@rel='grade_submitter_person']/*[@class='reg_id']",
                             namespaces=nsmap):
            reg_id = el.text.strip()
            if reg_id not in people:
                people[reg_id] = pws.get_person_by_regid(reg_id)
            gr_item.grade_submitter_person = people[reg_id]

        graderoster.items.append(gr_item)

    return graderoster
