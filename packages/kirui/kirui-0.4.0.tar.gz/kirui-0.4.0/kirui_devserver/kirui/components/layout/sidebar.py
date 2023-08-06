from browser import window, document
from django_brython.assets import require as req
from kirui.core import createElement as h, Component, CustomElement

jq = window.jQuery


@Component(
    tag='kr-layout-sidebar',
    template=req('sidebar.html')
)
class SidebarLayout(CustomElement):
    _is_sidebar_toggled: bool
    _is_sidebar_pinned: bool
    _sidebar_is_moving: bool
    sidebar_width: int

    def __init__(self, *args, **kwargs):
        self._sidebar_width = 256
        self._is_sidebar_pinned = True
        self._is_sidebar_toggled = False
        self._sidebar_is_moving = False
        self.counter = 10

    @property
    def sidebar_width(self):
        return f'{self._sidebar_width}px'

    def expand_menu(self, ev):
        ev.preventDefault()
        ev.stopPropagation()
        for submenu in ev.target.closest('li').querySelectorAll('ul'):
            if submenu.classList.contains('expanded'):
                submenu.classList.remove('expanded')
            else:
                submenu.classList.add('expanded')

    def navbar_pinner_clicked(self, ev):
        if self.component_config.application.is_pwa:
            if self._is_sidebar_toggled:
                jq(self).find('kr-sidebar-nav').css({'left': f'-{self.sidebar_width}'})
                jq(self).find('#navbar-overflow').css({'display': 'none'})
                self._is_sidebar_toggled = False
            else:
                jq(self).find('kr-sidebar-nav').css({'left': '0'})
                jq(self).find('#navbar-overflow').css({'display': 'block'})
                self._is_sidebar_toggled = True
        else:
            if self._is_sidebar_pinned:
                jq(self).find('kr-sidebar-nav').css({'left': f'-{self.sidebar_width}'})
                jq(self).find('kr-sidebar-main').css({'margin-left': '0'})
                self._is_sidebar_pinned = False
            else:
                jq(self).find('kr-sidebar-nav').css({'left': '0'})
                jq(self).find('kr-sidebar-main').css({'margin-left': f'{self.sidebar_width}'})
                self._is_sidebar_pinned = True

    def navbar_touch_start(self, ev):
        jq(self).find('kr-sidebar-nav').css({'transition': 'all 0s ease'})
        x_coord = ev.touches[0].pageX
        if self._is_sidebar_toggled is False and x_coord < 50:
            ev.preventDefault()
            self._sidebar_is_moving = True
        elif self._is_sidebar_toggled and self._sidebar_width - 50 <= x_coord <= self._sidebar_width + 50:
            self._sidebar_is_moving = True

    def navbar_touch_move(self, ev):
        if self._sidebar_is_moving is False:
            return

        left = int(ev.touches[0].pageX) - self._sidebar_width
        if left > 0:
            left = 0
        jq(self).find('kr-sidebar-nav').css({'left': f'{left}px'})

    def navbar_touch_end(self, ev):
        if self._sidebar_is_moving is False:
            return

        jq(self).find('kr-sidebar-nav').css({'transition': 'all 0.5s ease'})
        if ev.changedTouches[0].pageX >= 256 / 2:
            jq(self).find('kr-sidebar-nav').css({'left': '0'})
            self._is_sidebar_toggled = True
            jq(self).find('#navbar-overflow').css({'display': 'block'})
        else:
            jq(self).find('kr-sidebar-nav').css({'left': f'-{self.sidebar_width}'})
            self._is_sidebar_toggled = False
            jq(self).find('#navbar-overflow').css({'display': 'none'})

        self._sidebar_is_moving = False

    def show_navbar(self, ev):
        ev.preventDefault()
        if self._is_sidebar_pinned is False:
            jq(self).find('kr-sidebar-nav').css({'left': '0'})
            self._is_sidebar_toggled = True

    def hide_navbar(self, ev):
        ev.preventDefault()
        if self._is_sidebar_toggled:
            self._is_sidebar_toggled = False
            jq(self).find('kr-sidebar-nav').css({'left': f'-{self.sidebar_width}'})

    def dropdown_toggle(self, ev):
        ev.preventDefault()
        ev.stopPropagation()

        parent_rect = ev.target.parent.getBoundingClientRect()
        jq(ev.target).addClass('show')
        for el in ev.target.parent.getElementsByClassName('dropdown-menu'):
            if el.classList.contains('show'):
                el.classList.remove('show')
            else:
                el.classList.add('show')
                rect = el.getBoundingClientRect()
                offset_left = int(parent_rect.width - rect.width)
                el.style.left = f'{offset_left}px'
                el.style.top = f'{parent_rect.top + parent_rect.height - 7}px'

    def window_click(self, ev):
        jq('.show').removeClass('show')

    def connectedCallback(self):
        jq(self).find('kr-sidebar-main, kr-sidebar-nav').on('touchstart', self.navbar_touch_start)
        jq(self).find('kr-sidebar-main, kr-sidebar-nav').on('touchmove', self.navbar_touch_move)
        jq(self).find('kr-sidebar-main, kr-sidebar-nav').on('touchend', self.navbar_touch_end)
        jq(self).find('#navbar-pinner').click(self.navbar_pinner_clicked)
        jq(self).find('.dropdown-toggle').on('click', self.dropdown_toggle)
        jq(window).on('click', self.window_click)

        for sp in self.querySelectorAll('kr-sidebar-nav .expand'):
            sp.addEventListener('click', self.expand_menu)

        for main_menu in self.querySelectorAll('kr-sidebar-nav > ul > li > a'):
            if window.location.pathname.startswith(main_menu.attrs['href']):
                main_menu.classList.add('active')
                if sub_menu := main_menu.parent.querySelector('.collapse'):
                    sub_menu.classList.add('expanded')

        if self.component_config.application.is_pwa is False:
            jq(self).find('#navbar-toggler').on('mouseover', self.show_navbar)
            jq(self).find('kr-sidebar-nav').on('mouseleave', self.hide_navbar)



@Component(
    tag='kr-sidebar-main',
    template=req('sidebar_main.html')
)
class SidebarMain(CustomElement):
    def __init__(self):
        self.counter = 8

    def connectedCallback(self):
        pass


@Component(
    tag='kr-sidebar-header',
    template=req('sidebar_header.html')
)
class SidebarHeader(CustomElement):
    def connectedCallback(self):
        pass


@Component(
    tag='kr-sidebar-nav',
    template=req('sidebar_nav.html')
)
class SidebarNavigation(CustomElement):
    def connectedCallback(self):
        pass
