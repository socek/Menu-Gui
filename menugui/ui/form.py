# -*- encoding: utf-8 -*-
from menugui.ui.window import Window
from menugui.string import forceUnicode
from menugui.ui.widgets.button import Button
from menugui.ui.widgets.label import Label
from menugui.ui.widgets.linetext import TextLine
from menugui.ui.list import List
from menugui.elements import ListElement

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
        self._remove_all_elements()
        self.rewind()
    
    def _remove_all_elements(self):
        self._elements = {}
        self._dynamic_elements = []
        self._static_elements = []
    
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
            print self._dynamic_elements
            print self._active_element
            return None
    
    def rewind(self):
        self._active_element = 0
        if len(self._dynamic_elements) == 0:
            return
        
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
    
    def first_active_element(self):
        def first_element():
            self._active_element = 0
        #------------------------
        try:
            self._change_active_element(first_element)
        except Form.NoElementsInForm:
            return None
    
    def last_active_element(self):
        def last_element():
            self._active_element = len(self._dynamic_elements) -1
        #------------------------
        try:
            self._change_active_element(last_element)
        except Form.NoElementsInForm:
            return None
    
    def refresh(self, window_refresh=True):
        super(Form, self).refresh(False)
        
        for key, element in self._elements.items():
            element.set_active(self._active)
            if element == self.active_element:
                element.set_highlited(True)
            else:
                element.set_highlited(False)
            element.refresh()
        
        if window_refresh:
            self._c_window.refresh()

    def run(self):
        self._running = True
        self._active = True
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
                elif key[0] == 262: #home
                    self.first_active_element()
                elif key[0] == 360: #end
                    self.last_active_element()
                else:
                    pass
        
        self.close()
    
    def peacful_close(self, *args, **kwargs):
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


class SimpleForm(Form):
    
    settings = {
        'input_width' : 11,
        'label and input space' : 1,
        'borders' : 2,
        'button padding' : 2,
    }
    
    def __init__(self, *args, **kwargs):
        super(SimpleForm, self).__init__(*args, **kwargs)
        self._generate_elements_trigger = False
        self._elements_to_generate = {}
        self._elements_to_generate_list = []
    
    def add_textline(self, name, label):
        self._generate_elements_trigger = True
        data = {
            'name' : name,
            'label' : forceUnicode(label),
            'type' : 'textline',
            'visible' : True,
        }
        self._elements_to_generate[name] = data
        self._elements_to_generate_list.append(data)
    
    def add_button(self, name, label, fun):
        self._generate_elements_trigger = True
        data = {
            'name' : name,
            'label' : forceUnicode(label),
            'type' : 'button',
            'visible' : True,
            'fun' : fun,
        }
        self._elements_to_generate[name] = data
        self._elements_to_generate_list.append(data)
    
    def add_list(self, name, label, elements):
        self._generate_elements_trigger = True
        data = {
            'name' : name,
            'label' : forceUnicode(label),
            'type' : 'list',
            'visible' : True,
            'elements' : elements,
        }
        self._elements_to_generate[name] = data
        self._elements_to_generate_list.append(data)
    
    def _generate_elements(self):
        def list_function_generator(name):
            input = self._elements_to_generate[name]
            def list_function(button):
                glist = List(input['label'], self, indexing=False, with_exit=False)
                for key, label in input['elements']:
                    glist.add_option(ListElement(label, key))
                glist.run()
                button.data = glist._selected_element
                button.set_label(glist._selected_element_label)
            return list_function
        #-----------------------------------------------------------------------
        if self._generate_elements_trigger:
            self._remove_all_elements()
            
            label_width = 0
            button_width = 0
            for element in self._elements_to_generate_list:
                if element['type'] in ('list', 'textline'):
                    if label_width < len(element['label']):
                        label_width = len(element['label'])
                elif element['type'] == 'button':
                    if button_width < len(element['label']):
                        button_width = len(element['label'])
            
            window_width = label_width + self.settings['label and input space'] + self.settings['input_width'] + self.settings['borders']
            button_width += self.settings['button padding']
            
            label_pos_x = (self.settings['borders']/2)
            input_pos_x = label_width + self.settings['label and input space'] + (self.settings['borders']/2)
            button_pos_x = (window_width / 2) - (button_width / 2)
            
            line = 0
            for element in self._elements_to_generate_list:
                if element['visible']:
                    line += 1
                    if element['type'] == 'textline':
                        self.add_element(
                            'label_%s' %(element['name']),
                            Label(self, line, label_pos_x, element['label']),
                            'static')
                    
                        self.add_element(element['name'],
                            TextLine(self, line, input_pos_x, self.settings['input_width']),
                            'dynamic')
                        
                    elif element['type'] == 'list':
                        self.add_element(
                            'label_%s' %(element['name']),
                            Label(self, line, label_pos_x, element['label']),
                            'static')
                        
                        self.add_element(element['name'],
                            Button(self, line, input_pos_x, '', self.settings['input_width'], list_function_generator(element['name'])),
                            'dynamic')
                    elif element['type'] == 'button':
                        self.add_element('button_%s' %(element['name']),
                            Button(self, line, button_pos_x, element['label'], button_width, element['fun']),
                            'dynamic')
            
            self._generate_elements_trigger = False
    
    def refresh(self, window_refresh=True):
        self._generate_elements()
        super(SimpleForm, self).refresh(window_refresh)
    
    def run(self):
        self._generate_elements()
        super(SimpleForm, self).run()
