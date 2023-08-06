import { LitElement, html, render } from "./lit-element.js";

class Component extends LitElement {
    createRenderRoot() {
        this.innerHTML = '';  // TODO: remove childrens
        return this;
    }
}

export { Component, html, render };
