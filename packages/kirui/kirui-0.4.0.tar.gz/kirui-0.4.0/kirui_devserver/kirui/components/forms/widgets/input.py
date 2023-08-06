from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-input',
    template=require('input.html')
)
class Input(CustomElement):
    @property
    def css_class(self):
        retval = {'form-control': True}
        if self.props.get('error', '') != '':
            retval['is-invalid'] = True

        return retval

    @property
    def is_readonly(self):
        if int(self.props['disabled']) == 1:
            return 'true'

        return ''

    @property
    def input_type(self):
        if self.props['widget'] == 'kr-number-input':
            return 'number'

        return 'input'

    @property
    def form_data(self):
        field = self.querySelector('input')
        return {field.attrs['name']: field.value}
