from browser import ajax, window, document


class Request:
    def _on_complete(self, request, callback):
        def complete(ev):
            if request.readyState != 4:
                return

            document.querySelector('#loading').style.display = 'none'
            if request.status == 340:
                window.location.replace(request.getResponseHeader('Location'))
            elif request.status in (200, 403):
                callback(request)

        return complete

    def _prepare(self):
        document.querySelector('#loading').style.display = 'block'

    def post(self, url, data, callback):
        self._prepare()
        req = window.XMLHttpRequest.new()
        req.open('POST', url)
        req.send(data)
        req.onreadystatechange = self._on_complete(req, callback)

    def get(self, url, callback):
        self._prepare()
        req = window.XMLHttpRequest.new()
        req.open('GET', url)
        req.send()
        req.onreadystatechange = self._on_complete(req, callback)


request = Request()
