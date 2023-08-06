
def event_handler(fn):
    def handler(ev):
        el = ev.target
        while True:
            if hasattr(el, 'component_config'):
                break

            el = el.parent
            if el is None:
                break

        if el is not None:
            return fn(el)(ev)
        else:
            raise RuntimeError('No component parent')

    return handler
