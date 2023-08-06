from browser import window, document
from kirui.core import createElement as h, Component, patch_dom_with_vdom, CustomElement
from kirui.utils.http import request
from django_brython.assets import require


@Component(
    tag='kr-table',
    template=require('table.html')
)
class KrTable(CustomElement):
    def paginate(self, ev):
        def finished(resp):
            if resp.status == 200:
                vel = eval(resp.responseText)
                patch_dom_with_vdom(self, vel.render())
                # self.querySelector('kr-paginator tr td').setAttribute('colspan', self.column_count)

        request.get(f"?paginate_to={ev.target.getAttribute('data-page-to')}", callback=finished)

    def connectedCallback(self):
        self.column_count = len(self.querySelectorAll('kr-columns kr-column'))
        self.querySelector('kr-paginator tr td').setAttribute('colspan', self.column_count)


@Component(
    tag='kr-paginator',
    template=require('paginator.html')
)
class KrPaginator(CustomElement):
    @property
    def prev_page_class(self):
        return {'page-item': True, 'disabled': self.props['prevpage'] == ''}

    @property
    def next_page_class(self):
        return {'page-item': True, 'disabled': self.props['nextpage'] == ''}
