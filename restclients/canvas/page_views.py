from restclients.canvas import Canvas

class PageViews(Canvas):
    def get_pageviews_for_sis_login_id_from_start_date(self, sis_login_id, start_date):
        url = "/api/v1/users/sis_login_id:%s/page_views?start_time=%s" % (sis_login_id, start_date)
        data = self._get_resource(url)

        return data
