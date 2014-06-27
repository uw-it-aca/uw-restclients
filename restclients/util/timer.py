import datetime


def uctnow():
    return datetime.datetime.utcnow()


class Timer:
    def __init__(self):
        """ 
        Start the timer
        """
        self.start = uctnow()


    def get_elapsed(self):
        """
        Return the time spent in milliseconds
        """
        delta = uctnow - self.start
        return delta.microseconds / 1000.0
