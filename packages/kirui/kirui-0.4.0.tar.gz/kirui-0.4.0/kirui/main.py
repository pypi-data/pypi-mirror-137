from browser import ajax, webcomponent, window, document
from django_brython.assets import require
from kirui.application import Application
from kirui.components.layout.sidebar import SidebarLayout, SidebarMain, SidebarHeader, SidebarNavigation
from kirui.components.forms import Form, FormField, Select, Input, CheckboxSwitch, OptionCheckbox, DatePicker, TextBox, FileUpload
from kirui.components.modal import ModalLink, SideModal, ModalHeader, ModalBody, ModalFooter
from kirui.components.table import KrTable, KrFilteredTable

from kirui.core import createElement as h, patch_dom_with_vdom, render  # NOQA


def entrypoint(is_pwa, template, **kwargs):
    app = Application(is_pwa=bool(int(is_pwa)))
    for component in [SidebarLayout, SidebarMain, SidebarHeader, SidebarNavigation]:
        app.register_component(component)

    for component in [Form, FormField, Select, Input, CheckboxSwitch, OptionCheckbox, DatePicker, TextBox, FileUpload]:
        app.register_component(component)

    for component in [ModalLink, SideModal, ModalHeader, ModalBody, ModalFooter]:
        app.register_component(component)

    for component in [KrTable, KrFilteredTable]:
        app.register_component(component)

    patch_dom_with_vdom(document.getElementById('app'), template.render())
