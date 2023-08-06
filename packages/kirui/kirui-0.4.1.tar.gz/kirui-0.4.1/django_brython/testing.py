from urllib.parse import urlparse

from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import JavascriptException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait


class TestFunctionRunner:
    driver: webdriver.Chrome
    UNITTEST_RESULT_VARNAME = '__BRYTHON_UNITTEST_RESULTS__'
    UNITTEST_RESULT_TIMEOUT = 60

    def __init__(self, test_obj, test_func, url, driver):
        self.test_obj = test_obj
        self.test_func = test_func

        parsed = urlparse(url)
        prefix = '?' if len(parsed.query) == 0 else '&'
        self.url = url + f'{prefix}__BRYTHON_UNITTEST__={test_func.__module__}.{test_func.__qualname__}'
        self.driver = getattr(self.test_obj, driver)
        # if driver not found raise error

    def unittest_globals_exists(self, driver):
        try:
            result = driver.execute_script(f"return __BRYTHON_UNITTEST_RESULTS__;")
            return result
        except JavascriptException:
            return False

    def __call__(self, *args, **kwargs):
        try:
            settings.BRYTHON_UNITTEST_RUNNING = True

            if not self.url.startswith('/'):
                self.url = '/' + self.url

            self.driver.get(f"{getattr(self.test_obj, 'live_server_url')}{self.url}")

            wait = WebDriverWait(self.driver, self.UNITTEST_RESULT_TIMEOUT, poll_frequency=0.1)

            try:
                test_result = wait.until(self.unittest_globals_exists)
            except TimeoutException as e:
                raise TimeoutException(f"Javascript global {self.UNITTEST_RESULT_VARNAME} isn't peresented in {self.UNITTEST_RESULT_TIMEOUT} seconds") from e

            if test_result['exception']:
                raise Exception(test_result['exception'])
        finally:
            settings.BRYTHON_UNITTEST_RUNNING = False


def location(url, driver='driver', wait_for=None, function=None, instance=None):
    if function is None and instance is None:
        def dec(func):
            return location(str(url), driver=driver, function=func, wait_for=wait_for)

        return dec

    if function is not None and instance is None:
        def dec(inst):
            runner = TestFunctionRunner(test_obj=inst, test_func=function, url=url, driver=driver)
            return runner()

        return dec


def reverse(*args, **kwargs):
    from django.urls import reverse

    return reverse(*args, **kwargs)


def reverse_lazy(*args, **kwargs):
    from django.urls import reverse_lazy

    return reverse_lazy(*args, **kwargs)
