from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-select',
    template=require('select.html')
)
class Select(CustomElement):
    @property
    def css_class(self):
        retval = {'form-select': True}
        if self.attrs.get('error', '') != '':
            retval['is-invalid'] = True

        return retval

    @property
    def form_data(self):
        return {self.props['name']: self.querySelector('select').value}
