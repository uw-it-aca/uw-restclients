"""
utilites for catalyst clients
"""

import json
from restclients.sws import SWS
from restclients.models.catalyst import CourseGradeData, CourseGradeItem

class Catalyst(object):
    def parse_grade_data(self, app, content):
        data = json.loads(content)

        grading_by_section = {}

        for section_id in data[app]:
            if not section_id in grading_by_section:
                grading_by_section[section_id] = []

            section = SWS().get_section_by_label(section_id)
            for gradebook in data[app][section_id]:
                grade_data = CourseGradeData()
                grade_data.section = section
                grade_data.name = gradebook["name"]
                if "class_grade" in gradebook:
                    grade_data.class_grade = gradebook["class_grade"]["score"]

                if "total_score" in gradebook:
                    grade_data.total_score = gradebook["total_score"]["score"]

                if "url" in gradebook:
                    grade_data.url = gradebook["url"]

                grade_data.items = []

                for item in gradebook["items"]:
                    grade_item = CourseGradeItem()
                    grade_item.name = item["name"]
                    grade_item.score = item["score"]

                    if "url" in item:
                        grade_item.url = item["url"]

                    if "max_points" in item:
                        grade_item.max_points = item["max_points"]

                    grade_data.items.append(grade_item)

                grading_by_section[section_id].append(grade_data)

        return grading_by_section

