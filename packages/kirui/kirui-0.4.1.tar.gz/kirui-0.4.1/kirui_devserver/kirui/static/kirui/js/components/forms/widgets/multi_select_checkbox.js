import { Component, html, render } from "../../../core/component.js";


class MultiSelectCheckboxField extends Component {
    css_class() {
        let retval = 'parent';

        if (this.disabled.toString() == '1') {
            retval += ' readonly';
        }

        if (this.error !== null) {
            retval += ' is-invalid'
        }

        return retval
    }

    update_labels(ev) {
        let values = []
        for (let cb of this.querySelectorAll('input[type=checkbox]')) {
            if (cb.checked) {
                values.push(cb.parentElement.textContent.trim())
            }
        }
        let el = this.querySelectorAll('.select-value')[0]
        el.textContent = values.join(', ') || 'Kérlek válassz...'
    }

    toggle_dropdown(ev) {
        ev.stopPropagation();
        if (['INPUT', 'LABEL'].indexOf(ev.target.tagName) > -1) {
            return
        }

        $(this).find('.dropdown').toggleClass('show')
    }

    form_data() {
        let retval = {}
        retval[this.name] = []

        for (let option of this.querySelectorAll('input[type=checkbox]')) {
            if (option.checked === true) {
                retval[this.name].push(option.value);
            }
        }

        return retval
    }

    async connectedCallback() {
        super.connectedCallback();
        await this.updateComplete;
        if (this.disabled.toString() != '1') {
            this.querySelector('.parent').addEventListener('click', this.toggle_dropdown);
            $(this).find('input[type=checkbox]').on('change', (ev) => this.update_labels(ev));
        }
        this.update_labels(null);
    }

    render() {
        return html`
          <div class="${this.css_class()}">
            <div class="header">
              <div class="select-value">Kérlek válassz...</div>
            </div>
            <div class="dropdown">${this.$children}</div>
          </div>`
    }
}
customElements.define("kr-multi-select-checkbox", MultiSelectCheckboxField);


class OptionCheckbox extends Component {
    css_class() {
        let retval = 'form-select'
        if (this.error !== undefined) {
            retval += ' is-invalid'
        }

        return retval
    }

    form_data() {
        let retval = {}
        retval[this.name] = this.querySelector('select').value
        return retval
    }

    render() {
        return html`
          <div class="row">
            <label class="form-check-label">
              <input type="checkbox" class="form-check-input" .value="${this.getAttribute('value') || ''}" ?checked="${this.getAttribute('selected') !== null}" />
              ${this.$children}
            </label>
          </div>
        `
    }
}
customElements.define("kr-option-checkbox", OptionCheckbox);


export { MultiSelectCheckboxField, OptionCheckbox }
