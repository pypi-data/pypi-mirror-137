from browser import document, window
from kirui.core import createElement as h, Component, CustomElement
from django_brython.assets import require

jq = window.jQuery


@Component(
    tag='kr-multi-select-checkbox',
    template=require('multi_select_checkbox.html')
)
class MultiSelectCheckbox(CustomElement):
    def toggle_dropdown(self, ev):
        ev.stopPropagation()
        if (ev.target.tagName in {'INPUT', 'LABEL'}):
            return

        jq(self).find('.dropdown').toggleClass('show')

    def update_labels(self, ev):
        values = ', '.join(cb.parent.text for cb in self.querySelectorAll('input[type=checkbox]') if cb.checked)
        el = self.querySelectorAll('.select-value')[0]
        el.text = values or 'Kérlek válassz...'

    def connectedCallback(self):
        if self.props['disabled'] != '1':
            jq(self).find('.parent').on('click', self.toggle_dropdown)
            jq(self).find('input[type=checkbox]').on('change', self.update_labels)

        self.update_labels(None)

    @property
    def css_class(self):
        retval = {'parent': True, 'readonly': self.props['disabled'] == '1'}
        if self.props.get('error', '') != '':
            retval['is-invalid'] = True

        return retval

    @property
    def form_data(self):
        retval = {self.props['name']: []}
        options = self.querySelectorAll('input[type=checkbox]')

        for option in options:
            if getattr(option, 'checked', 'true'):
                retval[self.props['name']].append(option.attrs['value'])

        return retval


@Component(
    tag='kr-option-checkbox',
    template=require('option_checkbox.html')
)
class OptionCheckbox(CustomElement):
    def connectedCallback(self):
        #print(self.props)
        pass