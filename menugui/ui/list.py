# -*- encoding: utf-8 -*-
from menugui.ui.menu import Menu

class List(Menu):
    def __init__(self, *args, **kwargs):
        self._selected_element = None
        super(List, self).__init__(*args, **kwargs)
    
    def run_element(self):
        data = self.element.run()
        self._selected_element = self.element._data
        self._running = False
        return data
    
    def force_close(self, menu = None):
        self._running = False
        self._selected_element = None
    
    def add_option(self, option):
        option._set_menu(self, 'list')
        self._menu_list.append(option)
