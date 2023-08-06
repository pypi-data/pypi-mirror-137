

class Application:
    def __init__(self, is_pwa: bool = False):
        self.is_pwa = is_pwa
        self.components = set()

    def register_component(self, component):
        self.components.add(component)
        component.component_config.application = self
