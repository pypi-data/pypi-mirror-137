from browser import window

from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require


@Component(
    tag='kr-textbox',
    template=require('text.html')
)
class TextBox(CustomElement):
    DEFAULT_HEIGHT = 480

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

    def connectedCallback(self):
        window.tinymce.remove(f'#{self.props["id"]} textarea')

        window.tinymce.init({
            'target': self.querySelector('textarea'),
            'readonly': self.props['disabled'] == '1',
            'branding': False,
            'menubar': False,
            'height': self.props.get('height', self.DEFAULT_HEIGHT) or self.DEFAULT_HEIGHT
        })

    @property
    def form_data(self):
        return {self.props['name']: window.tinymce.get(f'{self.props["id"]}').getContent()}
