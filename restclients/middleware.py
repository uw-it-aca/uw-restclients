from restclients.dao import PerformanceDegradation
from restclients.models.degrade_performance import DegradePerformance


class EnableServiceDegradationMiddleware(object):
    """
    Makes it so an admin tool can set specific services to either be slower,
    have an error response code, or custom content.
    """
    # Django 1.10 MIDDLEWARE compat
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_request(self, request):
        PerformanceDegradation.clear_problems()
        if "RESTCLIENTS_ERRORS" not in request.session:
            return

        problem_str = request.session["RESTCLIENTS_ERRORS"]
        problems = DegradePerformance(problem_str)
        PerformanceDegradation.set_problems(problems)

    def process_response(self, request, response):
        PerformanceDegradation.clear_problems()

        return response
