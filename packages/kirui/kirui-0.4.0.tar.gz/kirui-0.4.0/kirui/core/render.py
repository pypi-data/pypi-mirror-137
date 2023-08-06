from browser import document

from .elements import createElement


def render(vel: 'createElement', slot_content=[], component=None, fix_component=False):
    return vel.render()

    """element = document.createElement(vel.tag)

    if hasattr(element, 'component_config') and component is None:
        component = element

    for k, v in vel.props.items():
        if k.startswith('{https://doculabs.io/2020/xtmpl#data-binding}'):
            k = k.replace('{https://doculabs.io/2020/xtmpl#data-binding}', '')
            if k not in {'onclick', 'onsubmit',}:
                v = v(component)

        if k == 'class' and isinstance(v, dict):
            v = ' '.join(ck for ck, cv in v.items() if cv is True)
        elif k == 'style' and isinstance(v, dict):
            v = ';'.join(f'{ck}: {cv}' for ck, cv in v.items())
        elif k == 'text':
            element.appendChild(document.createTextNode(v))

        if (isinstance(v, str) and len(v) <= 0) or k.startswith('{https://doculabs.io/2020/xtmpl#control}'):
            continue

        if k in {'onclick', 'onsubmit',}:
            def handle_wrapper(fn, component):
                def handler(ev):
                    fn2 = fn(self=ev.target)
                    if callable(fn2):
                        return fn2(ev)
                    else:
                        return fn2

                return handler

            element.addEventListener(k.replace('on', ''), handle_wrapper(v, component))
        else:
            if v is None:  # None érték -> üres stinrg
                v = ''
            element.setAttribute(k, v)

    # Ha a komponenst fixáltam, akkor nem szeretném lecserélni
    if hasattr(element, 'component_config') and fix_component is False:
        component = element

    if hasattr(element, 'component_config'):  # it is a custom component
        slot_content = slot_content or vel.children
        rendered = render(element.component_config.template, slot_content=slot_content, component=component)
        for child in rendered.children:
            element.appendChild(child)
    else:
        if vel.tag == 'slot':
            for child in slot_content:
                if isinstance(child, str):
                    element.appendChild(document.createTextNode(child))
                else:
                    element.appendChild(render(child, slot_content=[], component=component))
        else:
            for child in vel.children:
                if isinstance(child, str):
                    element.appendChild(document.createTextNode(child))
                else:
                    if v := child.props.get('{https://doculabs.io/2020/xtmpl#control}if', None):
                        v = v(component)
                        if v is False:
                            continue

                    rendered = render(child, slot_content=slot_content, component=component)
                    if rendered.tagName == 'SLOT':
                        for child2 in rendered.childNodes:
                            element.appendChild(child2)
                    else:
                        element.appendChild(rendered)

    return element"""
