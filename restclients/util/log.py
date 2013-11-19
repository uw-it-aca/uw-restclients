import logging
from restclients.util.timer import Timer

class NullHandler(logging.Handler):
    def emit(self, record):
        pass

null_handler = NullHandler()

def log_info(logger, action_desc, timer):
    """
    :param action_desc: the string description of the action
    :param timer: the Timer object representing the time spent in ms
    """
    logger.info("%s Time=%.3f milliseconds" %
                (action_desc, timer.get_elapsed()))


def log_err(logger, action_desc, timer):
    """
    :param action_desc: the string description of the action
    :param timer: the Timer object representing the time spent in ms
    """
    logger.error("%s Time=%.3f milliseconds" %
                 (action_desc, timer.get_elapsed()))

