import datetime

from browser import document, window
from kirui.core import createElement as h, Component, render, patch_dom_with_vdom, CustomElement
from kirui.utils.relativedelta import relativedelta
from django_brython.assets import require


@Component(
    tag='kr-date-picker',
    template=require('date_picker.html')
)
class DatePicker(CustomElement):
    @property
    def day_names(self):
        return ['Hét', 'Ked', 'Sze', 'Csü', 'Pén', 'Szo', 'Vas']

    @property
    def month_names(self):
        return ['Január', 'Február', 'Március', 'Április', 'Május', 'Június', 'Július', 'Augusztus', 'Szeptember', 'Október', 'November', 'December']

    @property
    def css_class(self):
        retval = {'parent': True, 'disabled': self.props['disabled']}
        if self.props.get('error', '') != '':
            retval['is-invalid'] = True

        return retval

    @property
    def is_readonly(self):
        if int(self.props['disabled']) == 1:
            return 'true'

        return ''

    @property
    def date_format(self):
        return self.props.get('date-format', '%Y-%m-%d')  # TODO: app beállításokból is kellene olvasni

    def step_month_backward(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.picker_date -= relativedelta(months=1)
        self._update_calendar_content()

    def step_month_forward(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.picker_date += relativedelta(months=1)
        self._update_calendar_content()

    def set_date(self, ev):
        ev.stopPropagation()
        ev.preventDefault()
        self.querySelector(f"input[name={self.props['name']}]").value = ev.target.getAttribute('data-value')
        self.value = datetime.datetime.strptime(ev.target.getAttribute('data-value'), self.date_format).date()
        self.hide_calendar(ev=None)

    def _generate_picker_content(self):
        iter_day = datetime.date(self.picker_date.year, self.picker_date.month, 1)

        content = h('div', {'class': 'date-picker-box', 'style': 'display: block'}, [
            h('div', {'class': 'paging'}, [
                h('div', {'class': 'material-icons', '{https://doculabs.io/2020/xtmpl#data-binding}onclick': lambda this: this.step_month_backward},
                  ['navigate_before']),
                h('div', {'class': 'month'}, [self.month_names[self.picker_date.month - 1]]),
                h('div', {'class': 'year'}, [str(self.picker_date.year)]),
                h('div', {'class': 'material-icons', '{https://doculabs.io/2020/xtmpl#data-binding}onclick': lambda this: this.step_month_forward},
                  ['navigate_next']),
            ]),
            h('div', {'class': 'day-names'}, [])
        ])

        for day_name in self.day_names:
            content.children[-1].children.append(h('div', {'class': 'day day-name'}, [day_name]))

        content.children.append(h('div', {'class': 'week'}, []))

        while True:
            v = iter_day.strftime(self.date_format)
            klass = {
                'day': True,
                'workday': iter_day.weekday() in [0, 1, 2, 3, 4],
                'weekend': iter_day.weekday() in [5, 6],
                'day-selected': v == self.querySelector(f"input[name={self.props['name']}]").value
            }

            # A naptár elején üres napok vannak, amik az előző hónapból "nyúlnak át"
            if iter_day.day == 1:
                style = {'margin-left': f'{44*iter_day.weekday()+2}px'}
            else:
                style = {}

            content.children[-1].children.append(
                h('div', {
                    'class': klass,
                    'data-value': v,
                    '{https://doculabs.io/2020/xtmpl#data-binding}onclick': lambda this: this.set_date,
                    'style': style
                }, [str(iter_day.day)]))
            if iter_day.weekday() == 6:
                content.children.append(h('div', {'class': 'week'}, []))
            iter_day = iter_day + datetime.timedelta(days=1)
            if self.picker_date.month != iter_day.month:
                break

        return content

    def _update_calendar_content(self):
        content = self._generate_picker_content()
        content = content.render(component=self)
        patch_dom_with_vdom(self.querySelector('.date-picker-box'), content)

    def show_calendar(self, ev):
        if ev:
            ev.stopPropagation()
            ev.preventDefault()

        # ha le van tiltva a mező, akkor ne is jelenítsük meg a naptárat
        if self.props.get('disabled', '0') == '1':
            return

        self.picker_date = self.value or datetime.date.today()
        self.picker_date = datetime.date(self.picker_date.year, self.picker_date.month, 1)
        self._update_calendar_content()
        self.querySelector('.date-picker-box').style['display'] = 'block'

    def hide_calendar(self, ev):
        if ev:
            parent = ev.target
            while True:
                if parent == document.body or parent == self:
                    break

                try:
                    parent = parent.parent
                except AttributeError:
                    break

            if parent == self:
                return

        # Ha a felhasználó kitörölte a mező tartalmát, akkor nullázzuk az értéket
        if len(self.querySelector(f"input[name={self.props['name']}]").value.strip()) == 0:
            self.value = ''

        self.querySelector('.date-picker-box').style['display'] = 'none'

    def connectedCallback(self):
        self.querySelector('input').addEventListener('click', self.show_calendar)
        document.addEventListener('click', self.hide_calendar)

        self.value = self.props.get('value', '')
        if len(self.value):
            self.value = datetime.datetime.strptime(self.value, self.date_format).date()

    @property
    def form_data(self):
        field = self.querySelector('input')
        return {field.attrs['name']: field.value}
