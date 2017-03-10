"""
This is the interface for interacting with the Student Web Service.
"""
from uw_sws import (parse_sws_date, encode_section_label, get_resource,
                    QUARTER_SEQ)
from uw_sws.thread import SWSThread
from uw_sws.compat import (SWS, use_v5_resources, get_current_sws_version,
                           deprecation)













