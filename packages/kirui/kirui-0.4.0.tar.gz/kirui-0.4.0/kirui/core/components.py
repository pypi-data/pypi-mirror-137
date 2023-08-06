from browser import webcomponent


class Component:
    def __init__(self, tag, template):
        self.tag = tag
        self.template = template
        self.application = None

    def __call__(self, klass):
        setattr(klass, 'component_config', self)

        if webcomponent.get(self.tag) is None:
            webcomponent.define(self.tag, klass)

        return klass
