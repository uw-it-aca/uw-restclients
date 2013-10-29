"""
The interface for interacting with Trumba web services.
"""

from restclients.dao import TrumbaBot_DAO, TrumbaSea_DAO, TrumbaTac_DAO
from lxml import etree
import logging
import json

class Trumba(object):
    """
    The Trumba object has methods for getting resources about calendar
    """
    logger = logging.getLogger('restclients.trumba.Trumba')

    @staticmethod
    def _log_xml_resp(campus, url, response):
        Trumba.logger.info(response.data)
        if response.status == 200:
            root = etree.fromstring(response.data)
            resp_msg = ''
            for el in root.iterchildren():
                resp_msg = resp_msg + str(el.attrib)

            Trumba.logger.info("%s %s ==RETURNS==> %s %s",
                               campus, url, response.status, resp_msg)
        else:
            Trumba.logger.error("%s %s ==RETURNS==> %s %s",
                                campus, url, response.status, response.reason)

    @staticmethod
    def _log_json_resp(campus, url, body, response):
        Trumba.logger.info(response.data)
        if response.status == 200:
            Trumba.logger.info("%s %s %s ==RETURNS==> %s %s",
                               campus, url, body, 
                               response.status, response.data)
        else:
            Trumba.logger.error("%s %s %s ==RETURNS==> %s %s",
                                campus, url, body,
                                response.status, response.reason)

    @staticmethod
    def get_bot_resource(url):
        """
        Get the requested resource or update resource using Bothell account
        :returns: http response with content in xml
        """
        response = TrumbaBot_DAO().getURL(url, 
                                          {"Content-Type":"application/xml"})
        Trumba._log_xml_resp("Bothell", url, response)
        return response

    @staticmethod
    def get_sea_resource(url):
        """
        Get the requested resource or update resource using Seattle account
        :returns: http response with content in xml
        """
        response = TrumbaSea_DAO().getURL(url,
                                          {"Accept": "application/xml"})
        Trumba._log_xml_resp("Seattle", url, response)
        return response
    
    @staticmethod
    def get_tac_resource(url):
        """
        Get the requested resource or update resource using Tacoma account
        :returns: http response with content in xml
        """
        response = TrumbaTac_DAO().getURL(url,
                                          {"Accept": "application/xml"})
        Trumba._log_xml_resp("Tacoma", url, response)
        return response


    @staticmethod
    def post_bot_resource(url, body):
        """
        Get the requested resource of Bothell calendars
        :returns: http response with content in json
        """
        response = TrumbaBot_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Bothell", url, body, response)
        return response
    
    @staticmethod
    def post_sea_resource(url, body):
        """
        Get the requested resource using the Seattle account
        :returns: http response with content in json
        """
        response = TrumbaSea_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Seattle", url, body, response)
        return response

    @staticmethod
    def post_tac_resource(url, body):
        """
        Get the requested resource of Tacoma calendars
        :returns: http response with content in json
        """
        response = TrumbaTac_DAO().postURL(url,
                                           {"Content-Type": "application/json"},
                                           body)
        Trumba._log_json_resp("Tacoma", url, body, response)
        return response

