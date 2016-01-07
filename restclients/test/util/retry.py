from django.test import TestCase
from restclients.exceptions import DataFailureException
from restclients.util.retry import retry


class RetryableError(Exception):
    pass


class AnotherRetryableError(Exception):
    pass


class UnexpectedError(Exception):
    pass


class RetryTest(TestCase):

    def test_bad_args(self):
        self.assertRaises(TypeError, retry, RetryableError, tries=None)
        self.assertRaises(ValueError, retry, RetryableError, delay=None)
        self.assertRaises(ValueError, retry, RetryableError, backoff=None)
        self.assertRaises(ValueError, retry, RetryableError, tries=-1)
        self.assertRaises(ValueError, retry, RetryableError, delay=0)
        self.assertRaises(ValueError, retry, RetryableError, backoff=0)

    def test_no_retry(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def succeeds():
            self.counter += 1
            return 'success'

        r = succeeds()

        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 1)

    def test_retry_once(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def fails_once():
            self.counter += 1
            if self.counter < 2:
                raise RetryableError('failed')
            else:
                return 'success'

        r = fails_once()
        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 2)

    def test_limit_reached(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def always_fails():
            self.counter += 1
            raise RetryableError('failed')

        self.assertRaises(RetryableError, always_fails)
        self.assertEqual(self.counter, 4)

    def test_multiple_exception_types(self):
        self.counter = 0

        @retry((RetryableError, AnotherRetryableError), tries=4, delay=0.1)
        def raise_multiple_exceptions():
            self.counter += 1
            if self.counter == 1:
                raise RetryableError('a retryable error')
            elif self.counter == 2:
                raise AnotherRetryableError('another retryable error')
            else:
                return 'success'

        r = raise_multiple_exceptions()
        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 3)

    def test_unexpected_exception_does_not_retry(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def raise_unexpected_error():
            self.counter += 1
            raise UnexpectedError('unexpected error')

        self.assertRaises(UnexpectedError, raise_unexpected_error)
        self.assertEqual(self.counter, 1)

    def test_no_retry_with_status(self):
        self.counter = 0

        @retry(DataFailureException, status_codes=[500], tries=4, delay=0.1)
        def not_found():
            self.counter += 1
            raise DataFailureException('/', 404, '')

        self.assertRaises(DataFailureException, not_found)
        self.assertEqual(self.counter, 1)

    def test_retry_once_with_status(self):
        self.counter = 0

        @retry(DataFailureException, status_codes=[500], tries=4, delay=0.1)
        def fails_once():
            self.counter += 1
            if self.counter < 2:
                raise DataFailureException('/', 500, '')
            else:
                return 'success'

        r = fails_once()
        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 2)

    def test_limit_reached_with_status(self):
        self.counter = 0

        @retry(DataFailureException, status_codes=[500], tries=4, delay=0.1)
        def always_fails():
            self.counter += 1
            raise DataFailureException('/', 500, '')

        self.assertRaises(DataFailureException, always_fails)
        self.assertEqual(self.counter, 4)

    def test_multiple_status_codes(self):
        self.counter = 0

        @retry(DataFailureException, status_codes=[500, 503, 504], tries=4, delay=0.1)
        def raise_multiple_exceptions():
            self.counter += 1
            if self.counter == 1:
                raise DataFailureException('/', 500, '')
            elif self.counter == 2:
                raise DataFailureException('/', 503, '')
            else:
                return 'success'

        r = raise_multiple_exceptions()
        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 3)

    def test_multiple_exceptions_and_multiple_status_codes(self):
        self.counter = 0

        @retry((DataFailureException, RetryableError), status_codes=[500, 503, 504], tries=4, delay=0.1)
        def raise_multiple_exceptions():
            self.counter += 1
            if self.counter == 1:
                raise DataFailureException('/', 500, '')
            elif self.counter == 2:
                raise DataFailureException('/', 503, '')
            elif self.counter == 3:
                raise RetryableError()
            else:
                return 'success'

        r = raise_multiple_exceptions()
        self.assertEqual(r, 'success')
        self.assertEqual(self.counter, 4)
