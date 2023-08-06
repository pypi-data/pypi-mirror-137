from io import StringIO

from samon.elements import BaseElement
from samon.render import RenderedElement


class KrApp(BaseElement):
    def to_xml(self, io: StringIO, indent: int, rendered_element: RenderedElement):
        try:
            module, entrypoint = rendered_element.node_attributes.pop('entrypoint').rsplit('.', 1)
            with rendered_element.frame(io, indent):
                print('<script type="text/python">\n', file=io, end='')
                print('import importlib', file=io)
                print('from kirui.core import createElement as h', file=io)
                print(f'module = importlib.import_module("{module}")', file=io)
                print(f'entrypoint = getattr(module, "{entrypoint}")', file=io)

                call = "entrypoint("
                for k, v in rendered_element.node_attributes.items():
                    call += f'{k}="{v}", '

                call += f'template={rendered_element.serialize("psx")})'
                print(call, file=io)

                print('</script>', file=io)
                print("""<script type="text/javascript">""", file=io)
                print("""brython({debug: 0, pythonpath: ['/brython/'], 'indexedDB': true});""", file=io)  # TODO: settings.DEBUG
                print("""</script>""", file=io)
        except KeyError:  # just for backward compatibility
            with rendered_element.frame(io, indent):
                print('<script type="text/javascript">', file=io, end='')
                print(f'var ${self.xml_attrs["id"]}_data = `', file=io, end='')
                rendered_element.to_jsx(io)
                print('`;</script>', file=io)
