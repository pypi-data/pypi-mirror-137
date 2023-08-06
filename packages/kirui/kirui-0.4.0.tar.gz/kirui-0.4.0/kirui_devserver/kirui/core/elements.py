from browser import document, webcomponent
from kirui.core import constants
from kirui.core.events import event_handler


class CustomElement:
    def render(self, children=[]):
        return self.component_config.template.render(component=self, slot_content=children)

    def connectedCallback(self):
        pass


class createElement:
    def __init__(self, tag, props, children):
        self.tag = tag
        self.props = props
        self.children = children

    def __repr__(self):
        attrs = ' '.join(f'{k}="{v}"' for k, v in self.props.items())
        return f'<{self.tag} {attrs}>'

    def render(self, slot_content=[], component=None):
        klass = webcomponent.get(self.tag)
        component_config = getattr(klass, 'component_config', None)
        if component_config is None:
            element = document.createElement(self.tag)

            for k, v in self.props.items():
                if self.tag == 'template':  # TODO: ennél robosztusabb megoldást a komponens sablon felismerésre
                    continue

                if k.startswith('{https://doculabs.io/2020/xtmpl#data-binding}'):
                    k = k.replace('{https://doculabs.io/2020/xtmpl#data-binding}', '')
                    if k in constants.JAVASCRIPT_EVENT_NAMES:
                        element.addEventListener(k.replace('on', ''), event_handler(v))
                        continue
                    else:
                        v = v(component or element)

                if k == 'class' and isinstance(v, dict):
                    v = ' '.join(ck for ck, cv in v.items() if cv is True)
                elif k == 'style' and isinstance(v, dict):
                    v = ';'.join(f'{ck}: {cv}' for ck, cv in v.items())
                elif k == 'text':
                    element.appendChild(document.createTextNode(v))

                if (isinstance(v, str) and len(v) <= 0) or k.startswith('{https://doculabs.io/2020/xtmpl#control}'):
                    continue

                if v is None:  # None érték -> üres stinrg
                    v = ''
                element.setAttribute(k, v)

            for vchild in self.children:
                if isinstance(vchild, str):
                    element.appendChild(document.createTextNode(vchild))
                elif vchild.tag == 'slot':
                    for vc in slot_content:
                        if isinstance(vc, str):
                            element.appendChild(document.createTextNode(vc))
                        else:
                            element.appendChild(vc.render(component=component, slot_content=[]))
                else:
                    if v := vchild.props.get('{https://doculabs.io/2020/xtmpl#control}if', None):
                        v = v(component)
                        if v is False:
                            continue

                    element.appendChild(vchild.render(component=component, slot_content=slot_content))
        else:
            element = document.createElement(self.tag)

            # evaluate properties
            element.props = {}
            for k, v in self.props.items():
                if k.startswith('{https://doculabs.io/2020/xtmpl#data-binding}'):
                    k = k.replace('{https://doculabs.io/2020/xtmpl#data-binding}', '')
                    v = v(component or element)

                element.props[k] = v

            # set element attributes according to template
            for k, v in component_config.template.props.items():
                if k.startswith('{https://doculabs.io/2020/xtmpl#data-binding}'):
                    k = k.replace('{https://doculabs.io/2020/xtmpl#data-binding}', '')

                element.setAttribute(k, element.props.get(k, v))

            root = element.render(children=slot_content or self.children)  # template
            for child in root.childNodes:
                element.appendChild(child)

        return element
