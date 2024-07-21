import time
import logging
from functools import wraps

def retry(max_retries=3, delay=1, exceptions=(Exception,)):
    """
    A decorator to retry a function if it raises an exception.

    :param max_retries: Maximum number of retries before giving up.
    :param delay:       Delay between retries in seconds.
    :param exceptions:  A tuple of exception types to catch and retry.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    logging.info(f"Function: {func.__name__}. Error: {e}. Retrying {retries}/{max_retries}...")
                    time.sleep(delay)
            # Final attempt
            return func(*args, **kwargs)
        return wrapper
    return decorator