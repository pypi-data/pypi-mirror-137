import ast
import sys

from io import StringIO

from django.test import TestCase

from browser.document import Element, AnonymusElement
from kirui.core import createElement as h, render, Component
from samon.environment import Environment
from samon.parser import DefaultParser


class RenderingTest(TestCase):
    def _r_pprint(self, element, out, indent):
        if indent is None:
            s = ''
            end=''
        else:
            s = indent * '  '
            end = '\n'
            indent += 1
        if hasattr(element, 'tagName'):
            attrs = ' '.join(f'{k}="{v}"' for k, v in element.attributes.items())
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

    def require(self, template):
        parser = DefaultParser(environment=Environment(loader=None))
        template = parser.parse(source=template, template_name='test')
        return eval(ast.unparse(template.serialize(output='psx')))

    def test_render_base(self):
        el = h('div', {'attr1': 7, 'attr2': 'example'}, ['Text content'])
        root = render(el)

        self.assertEqual(root.tagName, 'DIV')
        self.assertDictEqual(root.attributes, {'attr1': '7', 'attr2': 'example'})
        self.assertEqual(len(root.children), 1)

    def test_render_recursion(self):
        el = h('div', {}, [h('div', {}, ['Test content'])])
        root = render(el)

        self.assertEqual(len(root.children), 1)
        self.assertEqual(len(root.children[0].children), 1)

    def test_component(self):
        @Component(
            tag='kr-example',
            template=h('template', {}, [h('div', {}, [])])
        )
        class Example(Element):
            pass

        el = h('kr-example', {}, [])
        root = render(el)

        self.assertIsInstance(root, Example)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].tagName, 'DIV')

    def test_component_slot(self):
        @Component(
            tag='kr-example',
            template=h('template', {}, [h('div', {}, [h('slot', {}, [])])])
        )
        class Example(Element):
            pass

        el = h('kr-example', {}, ['slot content'])
        root = render(el)

        self.assertIsInstance(root, Example)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(root.children[0].tagName, 'DIV')
        self.assertEqual(len(root.children[0].children), 1)
        self.assertIsInstance(root.children[0].children[0], AnonymusElement)
        self.assertEqual(root.children[0].children[0].content, 'slot content')

    def test_slot_with_sibling(self):
        @Component(
            tag='kr-first',
            template=h('template', {}, [h('div', {}, ['div content']), h('slot', {}, [])])
        )
        class First(Element):
            pass

        el = h('kr-first', {}, ['slot content'])
        root = render(el)

        output = self.pprint(root, indent=None)
        self.assertEqual(output, '<KR-FIRST><DIV>div content</DIV>slot content</KR-FIRST>')

    def test_inherit_component_slot(self):
        @Component(
            tag='kr-first',
            template=h('template', {}, [h('div', {}, [h('slot', {}, [])])])
        )
        class First(Element):
            pass

        @Component(
            tag='kr-second',
            template=h('template', {}, [h('div', {}, ['div content']), h('kr-first', {}, [h('slot', {}, [])])])
        )
        class Second(Element):
            pass

        el = h('kr-second', {}, ['slot content'])
        root = render(el)

        self.assertEqual(root.tagName, 'KR-SECOND')
        self.assertEqual(len(root.children), 2)
        self.assertEqual(root.children[0].tagName, 'DIV')
        self.assertEqual(root.children[1].tagName, 'KR-FIRST')
        self.assertEqual(root.children[1].children[0].tagName, 'DIV')
        self.assertEqual(root.children[1].children[0].children[0].content, 'slot content')

    def test_inherited_slot_with_sibling(self):
        @Component(
            tag='kr-sidebar-main',
            template=self.require('''
            <template>
                <div class="container-fluid">
                    <slot />
                </div>
            </template>''')
        )
        class SidebarMain(Element):
            pass

        @Component(
            tag='kr-form-field',
            template=self.require('''<template>
                <div>
                    <label></label>
                    <kr-form-select>
                        <slot />
                    </kr-form-select>
                </div>
            </template>''')
        )
        class FormField(Element):
            @property
            def label_class(self):
                cls = 'col-form-label ' + ' '.join(f'col-{part}' for part in self.attrs.get('label-width', '').split(' '))
                if self.attrs.get('required', False):
                    cls += ' required'

                return cls

            @property
            def field_class(self):
                return ' '.join(f'col-{part}' for part in self.attrs.get('field-width', 'col').split(' '))

        sys.setrecursionlimit(500)

        el = h('kr-sidebar-main', {}, [h('kr-form-field', {'id': 'id_masodik', 'widget': 'kr-form-select', 'label-width': 'sm-4', 'field-width': 'sm-8', 'label': 'Próba választó'}, [h('option', {'value': 1}, ['One'])])])
        # root = next(render(el))
        root = render(el)
        print(self.pprint(root))
