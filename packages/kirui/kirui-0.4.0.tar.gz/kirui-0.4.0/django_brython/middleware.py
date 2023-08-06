from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.module_loading import import_string


class BrythonUnittestMiddleware(MiddlewareMixin):
    TEST_CODE_TEMPLATE = """
    <script type="text/python">
        import traceback, sys
        from importlib import reload
        from browser import document, window

        def run_test(event=None):
            import {module}
            reload({module})
            from {module} import {klass}
            test = {klass}()
            func = getattr(test, '{func_name}')
            func()
            print("test finished")

        run_test()

        document.bind('reload_brython_module@after', run_test)
    </script>
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_template_response(request, response)

        return response

    def process_template_response(self, request, response):
        unittest = request.GET.get('__BRYTHON_UNITTEST__', None)

        if unittest is None:
            return response

        try:
            klass, function = unittest.rsplit('.', 1)
        except ValueError as e:
            raise ImportError(f'Please specify the full path of the test method') from e

        klass = import_string(klass)

        test_html = self.TEST_CODE_TEMPLATE.format(
            module=klass.__module__,
            klass=klass.__name__,
            func_name=function
        ).encode('utf-8')

        response.content += test_html
        return response
