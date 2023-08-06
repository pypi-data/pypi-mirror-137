from browser import document, window

from kirui.core import createElement as h, Component, render, patch_dom_with_vdom, CustomElement
from kirui.utils.http import request
from django_brython.assets import require


@Component(
    tag='kr-modal-link',
    template=require('modal_link.html')
)
class ModalLink(CustomElement):
    def _add_event_listeners(self):
        for btn in self.querySelector('kr-modal-header').querySelectorAll('.btn-close'):
            btn.addEventListener('click', self.close_modal)

        for btn in self.querySelector('kr-modal-footer').querySelectorAll('input,button'):
            btn.addEventListener('click', self.submit)

    def _init_modal(self, resp):
        data = eval(resp.responseText)
        el = render(data, component=self)
        self.appendChild(el)
        self._add_event_listeners()
        document.body.classList.add('modal-open')

    def open_modal(self, ev):
        ev.preventDefault()
        ev.stopPropagation()

        request.get(
            url=self.querySelector('a').attrs['href'],
            callback=self._init_modal
        )

    def close_modal(self, ev):
        ev.preventDefault()
        ev.stopPropagation()
        self.querySelector('kr-side-modal').remove()
        document.body.classList.remove('modal-open')

    def _submit_complete(self, resp):
        if resp.status == 403:
            data = eval(resp.responseText)
            el = render(data, component=self)
            patch_dom_with_vdom(self.querySelector('kr-side-modal'), el)
            self._add_event_listeners()
        elif resp.status == 200:
            self.close_modal(window.CustomEvent.new())

    def submit(self, ev):
        ev.preventDefault()
        ev.stopPropagation()

        form = self.querySelector('kr-form')
        request.post(
            url=form.attrs['action'],
            data=form.form_data,
            callback=self._submit_complete
        )


@Component(
    tag='kr-side-modal',
    template=require('side_modal.html')
)
class SideModal(CustomElement):
    @property
    def css_style(self):
        return {
            'width': self.attrs.get('width', '50%')
        }


@Component(
    tag='kr-modal-header',
    template=require('modal_header.html')
)
class ModalHeader(CustomElement):
    pass


@Component(
    tag='kr-modal-body',
    template=require('modal_body.html')
)
class ModalBody(CustomElement):
    pass


@Component(
    tag='kr-modal-footer',
    template=require('modal_footer.html')
)
class ModalFooter(CustomElement):
    pass
