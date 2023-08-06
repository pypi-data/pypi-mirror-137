from browser import window, document
from kirui.core import createElement as h, Component, patch_dom_with_vdom, CustomElement
from kirui.utils.http import request
from django_brython.assets import require


@Component(
    tag='kr-filtered-table',
    template=require('filtered_table.html')
)
class KrFilteredTable(CustomElement):
    def submit(self, ev):
        print('filtered-table-submit')
        print(ev.target)
