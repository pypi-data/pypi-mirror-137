from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-checkbox-switch',
    template=require('checkbox_switch.html')
)
class CheckboxSwitch(CustomElement):
    @property
    def css_class(self):
        retval = {'form-control': True, 'form-check-input': True}
        if self.props.get('error', '') != '':
            retval['is-invalid'] = True

        return retval

    @property
    def is_disabled(self):
        if int(self.props['disabled']) == 1:
            return 'disabled'

        return ''

    @property
    def is_checked(self):
        if self.props.get('value', '') in ('true', True, 1):
            return '1'

        return ''

    @property
    def form_data(self):
        return {self.props['name']: self.querySelector('input[type=checkbox]').checked}
