"""
Contains UW HFS DAO implementations.
"""
from restclients_core.dao import DAO
from os.path import abspath, dirname
import os


class Hfs_DAO(DAO):
    def service_name(self):
        return 'hfs'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "..", "resources"))]
