from restclients.exceptions import DataFailureException
import math
import time


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, status_codes=[],
          logger=None):
    """
    Decorator function for retrying the decorated function,
    using an exponential or fixed backoff.

    Original: https://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    ExceptionToCheck: the exception to check. Can be a tuple of
        exceptions to check
    tries: number of times to try (not retry) before giving up
    delay: initial delay between tries in seconds
    backoff: backoff multiplier
    status_codes: list of http status codes to check for retrying, only applies
         when ExceptionToCheck is a DataFailureException
    logger: logging.Logger instance
    """
    if backoff is None or backoff <= 0:
        raise ValueError("backoff must be a number greater than 0")

    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be a number 0 or greater")

    if delay is None or delay <= 0:
        raise ValueError("delay must be a number greater than 0")

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)

                except ExceptionToCheck as err:
                    if (type(err) is DataFailureException and
                            len(status_codes) and
                            err.status not in status_codes):
                        raise

                    if logger:
                        logger.warning('%s: %s, Retrying in %s seconds.' % (
                            f.__name__, err, mdelay))

                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

            return f(*args, **kwargs)

        return f_retry

    return deco_retry
