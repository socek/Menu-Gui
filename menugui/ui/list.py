# -*- encoding: utf-8 -*-
from menugui.ui.menu import Menu

class List(Menu):
    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
    
    def run_element(self):
        data = self.element.run()
        self._running = False
        return data
    
    def force_close(self, menu = None):
        self._running = False
        self._selected_element = None
    
    def add_option(self, option):
        option._set_parent(self, 'list')
        self._head_elements.append(option)

    def set_element(self, data):
        if data == None:
            self.rewind()
            return
        
        element = None
        for element_loop in self.elements:
            if element_loop._data == data:
                element = element_loop
                break
        
        if element == None:
            return
        
        self._actual_element_number = self.elements.index(element)
