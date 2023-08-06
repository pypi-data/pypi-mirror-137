from pathlib import Path

from brython import list_modules
from brython.list_modules import ModulesFinder
from django.apps import apps
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        stdlib_path = Path(apps.get_app_config('django_brython').path) / 'static/django_brython/js/brython_stdlib.js'
        brython_stdlib = list_modules.parse_stdlib(stdlib_dir=stdlib_path.parent, js_name='brython_stdlib.js')
        finder = ModulesFinder(str(Path.cwd() / 'proba'), stdlib=brython_stdlib)
        finder.inspect()

        # finder.modules.add('_warnings')
        # print('_warnings' in finder.modules)
        finder.make_brython_modules('static/django_brython/js/brython_modules.js')
