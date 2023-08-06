from browser import window

from kirui.core import createElement as h, Component, render, patch_dom_with_vdom, CustomElement
from kirui.utils.http import request
from django_brython.assets import require


@Component(
    tag='kr-form',
    template=require('form.html')
)
class Form(CustomElement):
    @property
    def form_data(self):
        form_data = window.FormData.new()
        form_data.append('csrfmiddlewaretoken', self.attrs['csrfmiddlewaretoken'])
        for field in self.querySelectorAll('[data-form-field]'):
            for k, v in field.form_data.items():
                if isinstance(v, (list, tuple)):
                    for v1 in v:
                        form_data.append(k, v1)
                else:
                    form_data.append(k, v)

        return form_data

    def _submit_complete(self, resp):
        if resp.status == 403:
            vel = eval(resp.responseText)
            patch_dom_with_vdom(self, vel.render())

    def submit(self, ev):
        ev.preventDefault()
        ev.stopPropagation()

        request.post(
            url=self.attrs['action'],
            data=self.form_data,
            callback=self._submit_complete
        )
