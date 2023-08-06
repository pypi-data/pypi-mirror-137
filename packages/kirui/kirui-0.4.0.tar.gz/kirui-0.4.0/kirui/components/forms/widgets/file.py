from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-file',
    template=require('input.html')
)
class FileUpload(CustomElement):
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
        return 'file'

    @property
    def form_data(self):
        field = self.querySelector('input[type=file]')
        retval = {field.attrs['name']: ''}
        if len(field.files) > 0:
            retval[field.attrs['name']] = field.files[0]

        return retval
