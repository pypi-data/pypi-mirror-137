from functools import wraps
import time


class MaxRetriesExceededError(Exception):
    pass


def retry(max_retries=3):
    """Decorator that automatically retries the decorated function

    @retry(max_retries=2)
    def unpredictable():
        if random.choice([True, False]):
            return 42
        else:
            raise RuntimeError('KA-BOOM!!')


    def test_retry():
        for _ in range(5):
            try:
                print(unpredictable())
            except MaxRetriesExceededError as e:
                print(e)
    """

    def retry_dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    attempt += 1
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_retries:
                        time.sleep(attempt)
                    else:
                        errmsg = "{}() failed after {} retries".format(
                            func.__name__, max_retries
                        )
                        raise MaxRetriesExceededError(errmsg) from e

        return wrapper

    return retry_dec
