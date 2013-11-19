"""
The interface for interacting with Trumba web services.
"""

from restclients.dao import TrumbaBot_DAO, TrumbaSea_DAO, TrumbaTac_DAO
from restclients.util.timer import Timer
from restclients.util.log import log_info, log_err
from lxml import etree
import logging
import json

class Trumba(object):
    """
    The Trumba object has methods for getting resources about calendar
    """
    logger = logging.getLogger(__name__)

    @staticmethod
    def _log_xml_resp(campus, url, response, timer):
        if response.status == 200 and response.data is not None:
            root = etree.fromstring(response.data)
            resp_msg = ''
            for el in root.iterchildren():
                resp_msg = resp_msg + str(el.attrib)

            log_info(Trumba.logger,
                     "%s %s ==RETURNS==> %s %s" % (
                    campus, url, response.status, resp_msg),
                     timer)
        else:
            log_err(Trumba.logger,
                    "%s %s ==RETURNS==> %s %s" % (
                    campus, url, response.status, response.reason),
                    timer)

    @staticmethod
    def _log_json_resp(campus, url, body, response, timer):
        if response.status == 200 and response.data is not None:
            log_info(Trumba.logger,
                     "%s %s %s ==RETURNS==> %s %s" % (
                    campus, url, body, response.status, response.data),
                     timer)
        else:
            log_err(Trumba.logger,
                    "%s %s %s ==RETURNS==> %s %s" % (
                    campus, url, body, response.status, response.reason),
                    timer)

    @staticmethod
    def get_bot_resource(url):
        """
        Get the requested resource or update resource using Bothell account
        :returns: http response with content in xml
        """
        timer = Timer()
        response = TrumbaBot_DAO().getURL(url, 
                                          {"Content-Type":"application/xml"})
        Trumba._log_xml_resp("Bothell", url, response, timer)
        return response

    @staticmethod
    def get_sea_resource(url):
        """
        Get the requested resource or update resource using Seattle account
        :returns: http response with content in xml
        """
        timer = Timer()
        response = TrumbaSea_DAO().getURL(url,
                                          {"Accept": "application/xml"})
        Trumba._log_xml_resp("Seattle", url, response, timer)
        return response
    
    @staticmethod
    def get_tac_resource(url):
        """
        Get the requested resource or update resource using Tacoma account
        :returns: http response with content in xml
        """
        timer = Timer()
        response = TrumbaTac_DAO().getURL(url,
                                          {"Accept": "application/xml"})
        Trumba._log_xml_resp("Tacoma", url, response, timer)
        return response


    @staticmethod
    def post_bot_resource(url, body):
        """
        Get the requested resource of Bothell calendars
        :returns: http response with content in json
        """
        timer = Timer()
        response = TrumbaBot_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Bothell", url, body, response, timer)
        return response
    
    @staticmethod
    def post_sea_resource(url, body):
        """
        Get the requested resource using the Seattle account
        :returns: http response with content in json
        """
        timer = Timer()
        response = TrumbaSea_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Seattle", url, body, response, timer)
        return response

    @staticmethod
    def post_tac_resource(url, body):
        """
        Get the requested resource of Tacoma calendars
        :returns: http response with content in json
        """
        timer = Timer()
        response = TrumbaTac_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Tacoma", url, body, response, timer)
        return response

