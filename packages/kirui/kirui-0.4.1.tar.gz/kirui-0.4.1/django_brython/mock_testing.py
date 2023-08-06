import sys
import traceback

from browser import timer, window


def location(url, driver='driver', wait_for=None, function=None, instance=None):
    if function is None and instance is None:
        def dec(func):
            return location(url, driver=driver, wait_for=wait_for, function=func)

        return dec

    if function is not None and instance is None:
        def dec(inst):
            if wait_for:
                def wait_for_condition():
                    result = wait_for()
                    if result is True:
                        timer.clear_interval(test_timer)
                        try:
                            return function(inst)
                        except:
                            exc = traceback.format_exc()
                            window.__BRYTHON_UNITTEST_RESULTS__ = {
                                'exception': exc
                            }
                    else:
                        print("'wait_for' condition is not fulfilled, wait for one second")

                test_timer = timer.set_interval(wait_for_condition, 1000)

            else:
                try:
                    return function(inst)
                except:
                    exc = traceback.format_exc()
                    print(exc, file=sys.stderr)
                    window.__BRYTHON_UNITTEST_RESULTS__ = {
                        'exception': exc
                    }

        return dec


def reverse(*args, **kwargs):
    pass


def reverse_lazy(*args, **kwargs):
    pass
