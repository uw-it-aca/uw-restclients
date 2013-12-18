from restclients.canvas import Canvas
from restclients.models.canvas import Quiz
import dateutil.parser


class Quizzes(Canvas):
    def get_quizzes_by_sis_id(self, sis_id):
        """
        List quizzes for a given course sis id

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """
        return self.get_quizzes(self._sis_id(sis_id, "course"))


    def get_quizzes(self, course_id):
        """
        List quizzes for a given course

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """

        url = "/api/v1/courses/%s/quizzes" % course_id
        data = self._get_resource(url)
        quizzes = []
        for quiz in data:
            quiz = self._quiz_from_json(quiz)
            quizzes.append(quiz)
        return quizzes

    def _quiz_from_json(self, data):
        quiz = Quiz()
        quiz.quiz_id = data['id']
        quiz.due_at = dateutil.parser.parse(data['due_at'])
        quiz.title = data['title']
        quiz.html_url = data['html_url']
        quiz.published = data['published']

        return quiz
