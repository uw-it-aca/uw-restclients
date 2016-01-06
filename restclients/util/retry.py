import math
import time


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """
    Decorator function for retrying the decorated function,
    using an exponential or fixed backoff.

    Original: https://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    Modified to check for a passed exception.
    """
    if backoff <= 0:
        raise ValueError("backoff must be greater than 0")

    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")

    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as err:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry
