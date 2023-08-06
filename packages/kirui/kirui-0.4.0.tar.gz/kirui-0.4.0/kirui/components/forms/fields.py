from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-form-field',
    template=require('fields.html')
)
class FormField(CustomElement):
    @property
    def label_class(self):
        cls = 'col-form-label ' + ' '.join(f'col-{part}' for part in self.props.get('label-width', '').split(' '))
        if self.props.get('required', 'false') in ('true', True, 1):
            cls += ' required'

        return cls

    @property
    def field_class(self):
        return ' '.join(f'col-{part}' for part in self.props.get('field-width', 'col').split(' '))
