# -*- encoding: utf-8 -*-
from menugui.ui.menu import Menu

class List(Menu):
    def __init__(self, *args, **kwargs):
        self._selected_element = None
        self._selected_element_label = None
        super(List, self).__init__(*args, **kwargs)
    
    def run_element(self):
        data = self.element.run()
        self._selected_element = self.element._data
        self._selected_element_label = self.element._name
        self._running = False
        return data
    
    def force_close(self, menu = None):
        self._running = False
        self._selected_element = None
    
    def add_option(self, option):
        option._set_parent(self, 'list')
        self._head_elements.append(option)
