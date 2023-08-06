import itertools
import sys
from pathlib import Path

from django.apps import apps
from django.conf import settings

from livesync.asyncserver import dispatcher
from livesync.core.event import ClientEvent
from livesync.core.handler import BaseEventHandler
from livesync.core.signals import livesync_event


class DjangoBrythonEventHandler(BaseEventHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.static_dirs = set()
        self.template_dirs = set()

    @property
    def watched_paths(self):
        paths = {Path(settings.BASE_DIR)}
        for app in apps.get_app_configs():
            paths.add(Path(app.path))
            if tmpl_dir := (Path(app.path) / 'template').exists():
                self.template_dirs.add(tmpl_dir)

        #for path in getattr(settings, 'STATICFILES_DIRS', []):
        #    paths.add(Path(path))

        paths = set(itertools.chain(
            getattr(settings, 'STATICFILES_DIRS', []),
            paths,
        ))

        paths.update(*[tmpl['DIRS'] for tmpl in settings.TEMPLATES])
        return paths

    def is_ignored_pattern(self, path):
        path = Path(path)
        if path.suffix.endswith('~'):  # temporary file
            return True
        elif '.pyc' in path.suffixes:  # compiled python file
            return True

        return False

    def on_modified(self, event):
        if self.is_ignored_pattern(event.src_path):
            return

        super().on_modified(event)

    def on_moved(self, event):
        if self.is_ignored_pattern(event.src_path):
            return

        super().on_moved(event)

    def handle(self, event):
        module_path = event.src_path
        livesync_event.send(sender=self.__class__, event=ClientEvent(
            action='refresh',
            parameters={}
        ))
        return
        if module_path.endswith('.py'):
            for path in sys.path:
                if module_path.startswith(str(path)):
                    # /sys/path/module/path.py -> module.path
                    module_name = module_path[len(path)+1:-3].replace('/', '.')
                    livesync_event.send(sender=self.__class__, event=ClientEvent(
                        action='reload_brython_module',
                        parameters={
                            'module_name': module_name
                        }
                    ))
