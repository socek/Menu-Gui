# -*- encoding: utf-8 -*-
from menugui.ui.window import Window

class Form(Window):
    class NoElementsInForm(Exception): pass
    
    class NameAlreadyExists(Exception):
        def __init__(self, name):
            self._name = name
        
        def __str__(self):
            return self._name
        
        def __unicode__(self):
            return self._name
    #--------------------------------------
    
    def __init__(self, title, parent = None, pos_x = None, pos_y = None, width = None, height = None):
        super(Form, self).__init__(title, parent, pos_x, pos_y, width, height)
        self._elements = {}
        self._dynamic_elements = []
        self._static_elements = []
        self.rewind()
    
    def add_element(self, name, element, type):
        if self._elements.has_key(name):
            raise Form.NameAlreadyExists(name)
        self._elements[name] = element
        if type == 'static':
            self._static_elements.append(element)
        elif type == 'dynamic':
            self._dynamic_elements.append(element)
    
    @property
    def height(self):
        if self._height == None:
            pos_y = 0
            
            for key, element in self._elements.items():
                if pos_y < element._pos_y:
                    pos_y = element._pos_y
            return pos_y + 2
        else:
            return self._height
    
    @property
    def width(self):
        if self._width == None:
            elements_width = len(self._title)
            pos_x = 0
            for key, element in self._elements.items():
                if elements_width < element.width + element._pos_x:
                    elements_width = element.width + element._pos_x
            return elements_width + 1
        else:
            return self._width

    @property
    def active_element(self):
        try:
            return self._dynamic_elements[self._active_element]
        except IndexError:
            return None
    
    def rewind(self):
        self._active_element = 0
        if len(self._dynamic_elements) == 0:
            return
        
        self.active_element._on_get_focus()
        
        self.refresh()
    
    def _change_active_element(self, fun):
        if len(self._dynamic_elements) == 0:
            raise NoElementsInForm()
        
        self.active_element._on_lost_focus()
        
        fun()
        
        self.active_element._on_get_focus()
        self.refresh()

    def next_active_element(self, rewind_after_end=False):
        def next_element():
            self._active_element += 1
            if self._active_element >= len(self._dynamic_elements):
                self._active_element = len(self._dynamic_elements) -1
        def next_element_with_rewind():
            self._active_element += 1
            if self._active_element >= len(self._dynamic_elements):
                self._active_element = 0
        #------------------------
        try:
            if rewind_after_end:
                self._change_active_element(next_element_with_rewind)
            else:
                self._change_active_element(next_element)
        except Form.NoElementsInForm:
            return None
    
    def previous_active_element(self):
        def previous_element():
            self._active_element -= 1
            if self._active_element < 0:
                self._active_element = 0
        #------------------------
        try:
            self._change_active_element(previous_element)
        except Form.NoElementsInForm:
            return None
    
    def refresh(self, window_refresh=True):
        super(Form, self).refresh(False)
        
        for key, element in self._elements.items():
            if element == self.active_element:
                element.set_active(True)
            else:
                element.set_active(False)
            element.refresh()
        
        if window_refresh:
            self._c_window.refresh()

    def run(self):
        self._running = True
        self.active_element._on_get_focus()
        self.refresh()
        
        while self._running:
            key = self.active_element.processed_character()
            if key == None:
                pass
            else:
                if key[0] in(258, 10, 261): #cursor down or enter
                    self.next_active_element()
                elif key[0] == 9: #tab
                    self.next_active_element(True)
                elif key[0] in (259, 260):
                    self.previous_active_element()
                else:
                    pass
                    #print key
    
    def peacful_close(self):
        self._running = False
    
    def get_values(self):
        tab = {}
        for key, element in self._elements.items():
            try:
                tab[key] = unicode(element.data)
            except AttributeError:
                pass
        return tab

    def set_values(self, tab):
        for key, value in tab.items():
            self._elements[key].data = value
