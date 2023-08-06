const originalDefineFn = CustomElementRegistry.prototype.define;
CustomElementRegistry.prototype.define = function (elementName, impl, options) {
    const registeredCustomElement = customElements.get(elementName);
    if (!registeredCustomElement) {
        originalDefineFn.apply(this, [elementName, impl, options]);
    } else {
        let el = document.getElementsByTagName(elementName)[0]
        if (el !== undefined) {
            Object.setPrototypeOf(el, impl.prototype);
        }

        // registeredCustomElement.$cls = impl.prototype;
        /*for (let el of document.getElementsByTagName(elementName)) {
            el.render();
        }*/

        // Object.setPrototypeOf(el, CustomElement2.prototype)
    }
}

class AdoptedStyle extends HTMLElement {
    connectedCallback() {
        if (document.adoptedStyleSheets === undefined) {
            let el = document.createElement('link');
            el.setAttribute('rel', "stylesheet");
            el.setAttribute('href', this.getAttribute('src'));
            this.appendChild(el);
        } else {
            fetch(this.getAttribute('src'))
                .then(function (resp) {
                    if (resp.status === 200) {
                        return resp.text()
                    } else {
                        console.log('Fetch Error', resp.statusText);
                        return null
                    }
                }).then(
                function (resp) {
                    if (resp != null) {
                        let stylesheet = new CSSStyleSheet();
                        stylesheet.replaceSync(resp);
                        document.adoptedStyleSheets = [...document.adoptedStyleSheets, stylesheet];
                    }
                }
            ).catch(function(err) {
                console.log('Fetch Error :-S', err);
            });
        }
    }
}

customElements.define('kr-adopted-style', AdoptedStyle);
