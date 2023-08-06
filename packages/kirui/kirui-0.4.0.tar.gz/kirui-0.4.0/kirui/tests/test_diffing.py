from io import StringIO

from django.test import TestCase

from kirui.core import createElement as h, render, Component, patch_dom_with_vdom
from kirui.components.forms.widgets.date import DatePicker


class DiffingTest(TestCase):
    def _r_pprint(self, element, out, indent):
        if indent is None:
            s = ''
            end=''
        else:
            s = indent * '  '
            end = '\n'
            indent += 1
        if hasattr(element, 'tagName'):
            attrs = ' '.join(f'{k}="{v}"' for k, v in element._attributes.items())
            print(f'{s}<{element.tagName} {attrs}>', file=out, end=end)
            for child in element.children:
                self._r_pprint(child, indent=indent, out=out)
            print(f'{s}</{element.tagName}>', file=out, end=end)
        else:
            print(f'{s}{element.content}', file=out, end=end)

    def pprint(self, element, indent=0):
        s = StringIO()
        self._r_pprint(element, out=s, indent=indent)
        return s.getvalue()

    def test_diff_base(self):
        comp = DatePicker()
        content = comp._generate_picker_content()
        el1 = render(content, component=comp)
        el2 = render(content, component=comp)
        patch_dom_with_vdom(el1, el2)
        patch_dom_with_vdom(el1, el2)
        print(self.pprint(el1))
